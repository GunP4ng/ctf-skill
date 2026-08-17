# /// script
# requires-python = ">=3.12"
# ///
"""Emit, grade, and self-test structured model-control regressions."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import cast

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tests.model_control_harness import (
    Case,
    ProvenanceKind,
    Response,
    emit_prompts,
    expected_responses,
    grade,
    load_cases,
    load_responses,
    sha256_file,
)


def _response_json(response: Response) -> dict[str, object]:
    return {
        "case_id": response.case_id,
        "decision_ids": sorted(response.decision_ids),
        "next_action_id": response.next_action_id,
        "state": dict(response.state),
        "provenance_kind": response.provenance_kind,
        "evidence_refs": list(response.evidence_refs),
    }


def _synthetic_bundle(responses: dict[str, Response]) -> dict[str, object]:
    return {
        "schema_version": 2,
        "policy_sha256": "policy",
        "cases_sha256": "cases",
        "run": {
            "kind": "synthetic",
            "generator": "tests.run_model_controls.self-test",
        },
        "responses": [_response_json(response) for response in responses.values()],
    }


def _binding_self_test(
    cases: tuple[Case, ...],
    responses: dict[str, Response],
) -> list[str]:
    errors: list[str] = []
    with TemporaryDirectory(prefix="ctf-model-control-") as directory:
        path = Path(directory) / "responses.json"
        bundle = _synthetic_bundle(responses)

        def load(candidate: dict[str, object]) -> dict[str, Response]:
            _ = path.write_text(json.dumps(candidate), encoding="utf-8")
            return load_responses(
                path,
                policy_sha256="policy",
                cases_sha256="cases",
                cases=cases,
            )

        if load(bundle) != responses:
            errors.append("response bundle did not round-trip")

        def assert_rejected(candidate: dict[str, object], description: str) -> None:
            try:
                _ = load(candidate)
            except (TypeError, ValueError):
                return
            errors.append(f"response bundle accepted {description}")

        stale_policy = copy.deepcopy(bundle)
        stale_policy["policy_sha256"] = "stale-policy"
        assert_rejected(stale_policy, "a stale policy hash")

        stale_cases = copy.deepcopy(bundle)
        stale_cases["cases_sha256"] = "stale-cases"
        assert_rejected(stale_cases, "a stale cases hash")

        float_schema_version = copy.deepcopy(bundle)
        float_schema_version["schema_version"] = 2.0
        assert_rejected(float_schema_version, "a float schema_version")

        integer_state_true = copy.deepcopy(bundle)
        _state_for_case(
            integer_state_true,
            "partial-authoritative-rejection",
        )["next_intervention.count"] = True
        assert_rejected(integer_state_true, "true for an integer state")

        boolean_state_zero = copy.deepcopy(bundle)
        _state_for_case(
            boolean_state_zero,
            "close-with-contradiction",
        )["closure.allowed"] = 0
        assert_rejected(boolean_state_zero, "zero for a boolean state")

        missing_next_action = copy.deepcopy(bundle)
        first_response = _first_response(missing_next_action)
        del first_response["next_action_id"]
        assert_rejected(missing_next_action, "a missing next_action_id")

        extra_response_field = copy.deepcopy(bundle)
        _first_response(extra_response_field)["extra"] = True
        assert_rejected(extra_response_field, "an extra response field")

        duplicate_evidence_refs = copy.deepcopy(bundle)
        first_response = _first_response(duplicate_evidence_refs)
        refs = first_response["evidence_refs"]
        assert isinstance(refs, list)
        first_response["evidence_refs"] = [refs[0], refs[0]]
        assert_rejected(duplicate_evidence_refs, "duplicate evidence_refs")

        unknown_evidence_refs = copy.deepcopy(bundle)
        _first_response(unknown_evidence_refs)["evidence_refs"] = ["unknown:1"]
        assert_rejected(unknown_evidence_refs, "unknown evidence_refs")

        missing_run_identity = copy.deepcopy(bundle)
        missing_run_identity["run"] = {
            "kind": "real",
            "model": "model",
            "thinking": "thinking",
            "surface": "surface",
            "generated_at": "2026-08-07T00:00:00+00:00",
            "session_id": "session",
        }
        for response in _response_items(missing_run_identity):
            response["provenance_kind"] = "real"
        assert_rejected(missing_run_identity, "a real run without transcript_id")
    return errors


def _grader_self_test(cases: tuple[Case, ...]) -> dict[str, list[str]]:
    fixtures = expected_responses(cases)
    errors = _binding_self_test(cases, fixtures)
    first = cases[0]

    missing_decision = dict(fixtures)
    missing_decision[first.case_id] = replace(
        fixtures[first.case_id],
        decision_ids=frozenset(),
    )
    if not grade(cases, missing_decision):
        errors.append("grader accepted a missing decision")

    prohibited_case = next(case for case in cases if case.prohibited_actions)
    selected_prohibited = dict(fixtures)
    selected_prohibited[prohibited_case.case_id] = replace(
        selected_prohibited[prohibited_case.case_id],
        decision_ids=(
            prohibited_case.required_decisions
            | frozenset({next(iter(prohibited_case.prohibited_actions))})
        ),
    )
    if not grade(cases, selected_prohibited):
        errors.append("grader accepted a selected prohibited action")

    vocabulary_dump = dict(fixtures)
    vocabulary_dump[first.case_id] = replace(
        fixtures[first.case_id],
        decision_ids=frozenset(
            tag
            for case in cases
            for tag in case.required_decisions | case.prohibited_actions
        ),
    )
    if not grade(cases, vocabulary_dump):
        errors.append("grader accepted a vocabulary dump")

    first_key = next(iter(first.required_state))
    mutated = dict(first.required_state)
    mutated[first_key] = "__mutated__"
    mutated_state = dict(fixtures)
    mutated_state[first.case_id] = replace(
        fixtures[first.case_id],
        state=mutated,
    )
    if not grade(cases, mutated_state):
        errors.append("grader accepted a mutated state")

    next_action_case = next(case for case in cases if len(case.required_decisions) > 1)
    wrong_next_action = next(
        action
        for action in next_action_case.required_decisions
        if action != next_action_case.required_next_action
    )
    mutated_next_action = dict(fixtures)
    mutated_next_action[next_action_case.case_id] = replace(
        fixtures[next_action_case.case_id],
        next_action_id=wrong_next_action,
    )
    if not grade(cases, mutated_next_action):
        errors.append("grader accepted a wrong next_action_id")

    null_case = next(
        case
        for case in cases
        if any(value is None for value in case.required_state.values())
    )
    null_key = next(
        key for key, value in null_case.required_state.items() if value is None
    )
    incomplete = dict(null_case.required_state)
    del incomplete[null_key]
    missing_null = dict(fixtures)
    missing_null[null_case.case_id] = replace(
        fixtures[null_case.case_id],
        state=incomplete,
    )
    if not grade(cases, missing_null):
        errors.append("grader accepted a missing null-valued state key")

    live_case = next(case for case in cases if case.case_id == "frontier-promotion")
    premature = dict(fixtures)
    premature[live_case.case_id] = replace(
        fixtures[live_case.case_id],
        decision_ids=live_case.required_decisions | {"terminal_solved"},
        state={
            **live_case.required_state,
            "result": "solved",
            "termination": "completed",
        },
    )
    if not grade(cases, premature):
        errors.append("grader accepted terminal success in a live case")

    terminal_case = next(
        case for case in cases if case.case_id == "authoritative-closure"
    )
    illegal_terminal = dict(fixtures)
    illegal_terminal[terminal_case.case_id] = replace(
        fixtures[terminal_case.case_id],
        state={
            **terminal_case.required_state,
            "termination": "blocked",
        },
    )
    if not grade(cases, illegal_terminal):
        errors.append("grader accepted an illegal terminal pair")

    return {"__self_test__": errors} if errors else {}


def _first_response(bundle: dict[str, object]) -> dict[str, object]:
    return _response_items(bundle)[0]


def _state_for_case(
    bundle: dict[str, object],
    case_id: str,
) -> dict[str, object]:
    response = next(
        response
        for response in _response_items(bundle)
        if response["case_id"] == case_id
    )
    state = response["state"]
    assert isinstance(state, dict)
    return cast(dict[str, object], state)


def _response_items(bundle: dict[str, object]) -> list[dict[str, object]]:
    items = bundle["responses"]
    assert isinstance(items, list)
    responses: list[dict[str, object]] = []
    for item in cast(list[object], items):
        assert isinstance(item, dict)
        responses.append(cast(dict[str, object], item))
    return responses


def _main() -> int:
    parser = argparse.ArgumentParser()
    _ = parser.add_argument(
        "mode",
        choices=("emit", "grade", "self-test"),
        nargs="?",
        default="self-test",
    )
    _ = parser.add_argument("--policy", type=Path)
    _ = parser.add_argument(
        "--cases",
        type=Path,
        default=Path(__file__).with_name("model-control-cases.json"),
    )
    _ = parser.add_argument("--responses", type=Path)
    _ = parser.add_argument(
        "--provenance-kind",
        choices=("synthetic", "real"),
    )
    args = parser.parse_args()
    mode = cast(str, args.mode)
    policy_path = cast(Path | None, args.policy)
    cases_path = cast(Path, args.cases)
    responses_path = cast(Path | None, args.responses)
    provenance_kind = cast(ProvenanceKind | None, args.provenance_kind)
    cases = load_cases(cases_path)

    if mode == "emit":
        if policy_path is None:
            parser.error("--policy is required for emit")
        if provenance_kind is None:
            parser.error("--provenance-kind is required for emit")
        payload = {
            "schema": "ctf-skill-model-control-prompts-v3",
            "policy_sha256": sha256_file(policy_path),
            "cases_sha256": sha256_file(cases_path),
            "prompts": emit_prompts(
                policy_path.read_text(encoding="utf-8"),
                cases,
                provenance_kind=provenance_kind,
            ),
        }
        print(json.dumps(payload, indent=2))
        return 0

    if mode == "grade":
        if policy_path is None:
            parser.error("--policy is required for grade")
        if responses_path is None:
            parser.error("--responses is required for grade")
        responses = load_responses(
            responses_path,
            policy_sha256=sha256_file(policy_path),
            cases_sha256=sha256_file(cases_path),
            cases=cases,
        )
        failures = grade(cases, responses)
    else:
        failures = _grader_self_test(cases)

    if failures:
        print(json.dumps(failures, indent=2), file=sys.stderr)
        return 1
    print(f"PASS: {len(cases)} model-control cases")
    return 0


def main() -> int:
    try:
        return _main()
    except (TypeError, ValueError) as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
