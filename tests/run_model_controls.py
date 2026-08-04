# /// script
# requires-python = ">=3.12"
# ///
"""Emit, grade, and self-test structured model-control regressions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import cast

from .model_control_harness import (
    Case,
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
        "state": response.state,
    }


def _binding_self_test(
    responses: dict[str, Response],
) -> list[str]:
    errors: list[str] = []
    with TemporaryDirectory(prefix="ctf-model-control-") as directory:
        path = Path(directory) / "responses.json"
        bundle = {
            "schema": "ctf-skill-model-control-responses-v1",
            "policy_sha256": "policy",
            "cases_sha256": "cases",
            "responses": [
                _response_json(response) for response in responses.values()
            ],
        }
        _ = path.write_text(
            json.dumps(bundle),
            encoding="utf-8",
        )
        loaded = load_responses(
            path,
            policy_sha256="policy",
            cases_sha256="cases",
        )
        if loaded != responses:
            errors.append("response bundle did not round-trip")
        try:
            _ = load_responses(
                path,
                policy_sha256="stale-policy",
                cases_sha256="cases",
            )
        except ValueError:
            pass
        else:
            errors.append("response bundle accepted a stale policy hash")
    return errors


def _grader_self_test(cases: tuple[Case, ...]) -> dict[str, list[str]]:
    fixtures = expected_responses(cases)
    errors = _binding_self_test(fixtures)
    first = cases[0]

    missing_decision = dict(fixtures)
    missing_decision[first.case_id] = Response(
        case_id=first.case_id,
        decision_ids=frozenset(),
        state=first.required_state,
    )
    if not grade(cases, missing_decision):
        errors.append("grader accepted a missing decision")

    vocabulary_dump = dict(fixtures)
    vocabulary_dump[first.case_id] = Response(
        case_id=first.case_id,
        decision_ids=frozenset(
            tag
            for case in cases
            for tag in case.required_decisions | case.prohibited_actions
        ),
        state=first.required_state,
    )
    if not grade(cases, vocabulary_dump):
        errors.append("grader accepted a vocabulary dump")

    first_key = next(iter(first.required_state))
    mutated = dict(first.required_state)
    mutated[first_key] = "__mutated__"
    mutated_state = dict(fixtures)
    mutated_state[first.case_id] = Response(
        case_id=first.case_id,
        decision_ids=first.required_decisions,
        state=mutated,
    )
    if not grade(cases, mutated_state):
        errors.append("grader accepted a mutated state")

    null_case = next(
        case
        for case in cases
        if any(value is None for value in case.required_state.values())
    )
    null_key = next(
        key for key, value in null_case.required_state.items()
        if value is None
    )
    incomplete = dict(null_case.required_state)
    del incomplete[null_key]
    missing_null = dict(fixtures)
    missing_null[null_case.case_id] = Response(
        case_id=null_case.case_id,
        decision_ids=null_case.required_decisions,
        state=incomplete,
    )
    if not grade(cases, missing_null):
        errors.append("grader accepted a missing null-valued state key")

    live_case = next(
        case for case in cases if case.case_id == "frontier-promotion"
    )
    premature = dict(fixtures)
    premature[live_case.case_id] = Response(
        case_id=live_case.case_id,
        decision_ids=live_case.required_decisions | {"terminal_solved"},
        state={
            **live_case.required_state,
            "result": "solved",
            "termination": "completed",
        },
    )
    if not grade(cases, premature):
        errors.append("grader accepted terminal success in a live case")

    return {"__self_test__": errors} if errors else {}


def main() -> int:
    parser = argparse.ArgumentParser()
    _ = parser.add_argument("mode", choices=("emit", "grade", "self-test"))
    _ = parser.add_argument("--policy", type=Path)
    _ = parser.add_argument("--cases", type=Path, required=True)
    _ = parser.add_argument("--responses", type=Path)
    args = parser.parse_args()
    mode = cast(str, args.mode)
    policy_path = cast(Path | None, args.policy)
    cases_path = cast(Path, args.cases)
    responses_path = cast(Path | None, args.responses)
    cases = load_cases(cases_path)

    if mode == "emit":
        if policy_path is None:
            parser.error("--policy is required for emit")
        payload = {
            "schema": "ctf-skill-model-control-prompts-v1",
            "policy_sha256": sha256_file(policy_path),
            "cases_sha256": sha256_file(cases_path),
            "prompts": emit_prompts(
                policy_path.read_text(encoding="utf-8"),
                cases,
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
        )
        failures = grade(cases, responses)
    else:
        failures = _grader_self_test(cases)

    if failures:
        print(json.dumps(failures, indent=2), file=sys.stderr)
        return 1
    print(f"PASS: {len(cases)} model-control cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
