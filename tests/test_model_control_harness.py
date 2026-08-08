"""Regression tests for strict model-control response schema v2."""

from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Callable
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TypeAlias, cast, override
from unittest import TestCase

from .model_control_harness import (
    Case,
    JsonScalar,
    Response,
    emit_prompts,
    expected_responses,
    grade,
    load_cases,
    load_responses,
)

JsonObject: TypeAlias = dict[str, object]
Mutation: TypeAlias = Callable[[JsonObject], object]

CASES_PATH = Path(__file__).with_name("model-control-cases.json")
SEMANTIC_SHA256 = "c6324fd2804b4987d11798b62d3e3a14177411f1d5343045e3086e53a1f948a8"
CASE_IDS = (
    "partial-authoritative-rejection",
    "frontier-promotion",
    "authoritative-promotion",
    "discover-before-solver",
    "surrogate-repair-refutation",
    "candidate-terminalization",
    "unaffordable-contradiction",
    "close-with-contradiction",
    "fingerprint-cosmetic-variation",
    "fingerprint-legal-reset",
    "uniqueness-proven",
    "surrogate-only-terminal",
    "target-revision-denied",
    "authoritative-closure",
    "cost-provenance-required",
    "context-mismatch-unresolved",
    "fingerprint-source-laundering",
    "cancel-counts-no-information",
    "cardinality-relabel-no-information",
    "surrogate-multihop-scope",
    "surrogate-reconfiguration-reset",
    "uncovered-surrogate-preserves-eligibility",
    "independent-target-revision",
    "partial-completed-affordable-candidate",
    "failed-valid-oracle-completed",
    "no-result-blocked",
    "partial-interrupted",
    "terminal-freeze-cleanup-interruption",
    "uniqueness-disproven",
    "uniqueness-unknown",
    "inflight-authoritative-acceptance",
    "budget-unit-shopping",
    "budget-limit-preexhausted",
    "fingerprint-reset-out-of-scope",
    "obligation-discharge-out-of-scope",
    "inflight-unrelated-contradiction",
    "discovery-obligation-relabel",
    "empty-discovery-under-unknown",
    "conservative-bound-shopping",
    "surrogate-nominated-target-revision",
    "authoritative-nondeterminism-contradiction",
    "authorization-scope-required",
    "capability-inference-not-evidence",
    "reserve-identity-preserved",
    "invalid-falsifier-keeps-active",
    "budget-bound-remains-unknown",
    "side-effect-permission-required",
    "raw-evidence-before-reduction",
    "inflight-recovery-no-reexecute",
    "trusted-stop-pauses-mutations",
    "exact-receipt-reuse",
    "bounded-read-batch-remains-flexible",
)


class ModelControlSchemaV2Tests(TestCase):
    @override
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.cases: tuple[Case, ...] = ()
        self.responses: dict[str, Response] = {}

    @override
    def setUp(self) -> None:
        self.cases = load_cases(CASES_PATH)
        self.responses = expected_responses(self.cases)

    def _response_json(self, response: Response) -> JsonObject:
        return {
            "case_id": response.case_id,
            "decision_ids": sorted(response.decision_ids),
            "next_action_id": response.next_action_id,
            "state": dict(response.state),
            "provenance_kind": response.provenance_kind,
            "evidence_refs": list(response.evidence_refs),
        }

    def _bundle(self) -> JsonObject:
        return {
            "schema_version": 2,
            "policy_sha256": "policy",
            "cases_sha256": "cases",
            "run": {
                "kind": "synthetic",
                "generator": "tests.test_model_control_harness",
            },
            "responses": [
                self._response_json(response) for response in self.responses.values()
            ],
        }

    def _load(self, bundle: JsonObject) -> dict[str, Response]:
        with TemporaryDirectory(prefix="ctf-model-control-test-") as directory:
            path = Path(directory) / "responses.json"
            _ = path.write_text(json.dumps(bundle), encoding="utf-8")
            return load_responses(
                path,
                policy_sha256="policy",
                cases_sha256="cases",
                cases=self.cases,
            )

    def _assert_rejected(self, mutate: Mutation) -> None:
        bundle = self._bundle()
        _ = mutate(bundle)
        with self.assertRaises((TypeError, ValueError)):
            _ = self._load(bundle)

    def test_preserves_the_pinned_52_case_semantics(self) -> None:
        raw_cases = cast(
            list[JsonObject],
            json.loads(CASES_PATH.read_text(encoding="utf-8")),
        )
        self.assertEqual(tuple(case.case_id for case in self.cases), CASE_IDS)
        self.assertEqual(len(self.cases), 52)
        semantic = [
            {
                "id": case["id"],
                "required_decisions": case["required_decisions"],
                "prohibited_actions": case["prohibited_actions"],
                "required_state": case["required_state"],
            }
            for case in raw_cases
        ]
        encoded = json.dumps(
            semantic,
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
        self.assertEqual(hashlib.sha256(encoded).hexdigest(), SEMANTIC_SHA256)
        self.assertEqual(len({case.case_id for case in self.cases}), 52)

    def test_loads_an_exact_synthetic_v2_bundle(self) -> None:
        self.assertEqual(self._load(self._bundle()), self.responses)

    def test_rejects_missing_or_extra_top_level_fields(self) -> None:
        self._assert_rejected(lambda bundle: bundle.pop("schema_version"))
        self._assert_rejected(lambda bundle: bundle.__setitem__("schema_version", 1))
        self._assert_rejected(lambda bundle: bundle.__setitem__("extra", True))
        self._assert_rejected(lambda bundle: bundle.pop("run"))

    def test_rejects_float_schema_version(self) -> None:
        self._assert_rejected(lambda bundle: bundle.__setitem__("schema_version", 2.0))

    def test_rejects_boolean_schema_version(self) -> None:
        self._assert_rejected(lambda bundle: bundle.__setitem__("schema_version", True))

    def test_rejects_true_for_an_integer_state(self) -> None:
        def replace_integer_state_with_true(bundle: JsonObject) -> None:
            self._state_for_case(
                bundle,
                "partial-authoritative-rejection",
            )["next_intervention.count"] = True

        self._assert_rejected(replace_integer_state_with_true)

    def test_rejects_float_for_an_integer_state(self) -> None:
        def replace_integer_state_with_float(bundle: JsonObject) -> None:
            self._state_for_case(
                bundle,
                "partial-authoritative-rejection",
            )["next_intervention.count"] = 1.0

        self._assert_rejected(replace_integer_state_with_float)

    def test_rejects_zero_for_a_boolean_state(self) -> None:
        def replace_boolean_state_with_zero(bundle: JsonObject) -> None:
            self._state_for_case(
                bundle,
                "close-with-contradiction",
            )["closure.allowed"] = 0

        self._assert_rejected(replace_boolean_state_with_zero)

    def test_rejects_missing_or_extra_response_fields(self) -> None:
        required_fields = (
            "case_id",
            "decision_ids",
            "next_action_id",
            "state",
            "provenance_kind",
            "evidence_refs",
        )
        for field in required_fields:
            with self.subTest(field=field):

                def remove_field(bundle: dict[str, object], field: str = field) -> None:
                    _ = self._first_response(bundle).pop(field)

                self._assert_rejected(remove_field)
        self._assert_rejected(
            lambda bundle: self._first_response(bundle).__setitem__("extra", True)
        )

    def test_rejects_invalid_response_values(self) -> None:
        self._assert_rejected(
            lambda bundle: self._first_response(bundle).__setitem__(
                "next_action_id", ""
            )
        )
        self._assert_rejected(
            lambda bundle: self._first_response(bundle).__setitem__(
                "next_action_id", ["first", "second"]
            )
        )
        self._assert_rejected(
            lambda bundle: self._first_response(bundle).__setitem__(
                "provenance_kind", "archival"
            )
        )
        self._assert_rejected(
            lambda bundle: self._first_response(bundle).__setitem__("evidence_refs", [])
        )
        self._assert_rejected(
            lambda bundle: self._first_response(bundle).__setitem__(
                "evidence_refs", ["given:1", "given:1"]
            )
        )
        self._assert_rejected(
            lambda bundle: self._first_response(bundle).__setitem__(
                "evidence_refs", ["unknown:1"]
            )
        )
        self._assert_rejected(
            lambda bundle: self._first_response(bundle).__setitem__(
                "case_id", "unknown-case"
            )
        )
        self._assert_rejected(
            lambda bundle: self._first_response(bundle).__setitem__("state", [])
        )

        def add_unknown_state(bundle: JsonObject) -> None:
            self._first_state(bundle)["unknown.state"] = "value"

        self._assert_rejected(add_unknown_state)

    def test_rejects_a_real_run_without_every_identity(self) -> None:
        bundle = self._bundle()
        bundle["run"] = {
            "kind": "real",
            "model": "model-id",
            "thinking": "high",
            "surface": "pinned-surface",
            "generated_at": "2026-08-07T00:00:00+00:00",
            "session_id": "session-id",
            "transcript_id": "transcript-id",
        }
        for response in self._response_items(bundle):
            response["provenance_kind"] = "real"
        real_responses = {
            case_id: replace(response, provenance_kind="real")
            for case_id, response in self.responses.items()
        }
        self.assertEqual(self._load(bundle), real_responses)
        for field in (
            "model",
            "thinking",
            "surface",
            "generated_at",
            "session_id",
            "transcript_id",
        ):
            with self.subTest(field=field):

                def remove_identity(
                    candidate: JsonObject,
                    field: str = field,
                ) -> None:
                    _ = self._run(candidate).pop(field)

                candidate = copy.deepcopy(bundle)
                remove_identity(candidate)
                with self.assertRaises((TypeError, ValueError)):
                    _ = self._load(candidate)

    def test_grader_requires_the_case_next_action_and_exact_state(self) -> None:
        self.assertEqual(grade(self.cases, self.responses), {})
        case = next(item for item in self.cases if len(item.required_decisions) > 1)
        alternate_action = next(
            action
            for action in case.required_decisions
            if action != case.required_next_action
        )
        wrong_action = dict(self.responses)
        wrong_action[case.case_id] = replace(
            wrong_action[case.case_id],
            next_action_id=alternate_action,
        )
        self.assertIn(
            "next_action_id",
            " ".join(grade(self.cases, wrong_action)[case.case_id]),
        )
        wrong_state = dict(self.responses)
        changed_state = dict(case.required_state)
        state_key = next(iter(changed_state))
        changed_state[state_key] = "__wrong__"
        wrong_state[case.case_id] = replace(
            wrong_state[case.case_id],
            state=changed_state,
        )
        self.assertTrue(grade(self.cases, wrong_state))

    def test_grader_rejects_state_type_coercions(self) -> None:
        integer_case = next(
            case
            for case in self.cases
            if case.case_id == "partial-authoritative-rejection"
        )
        integer_state = dict(integer_case.required_state)
        integer_state["next_intervention.count"] = True
        integer_responses = dict(self.responses)
        integer_responses[integer_case.case_id] = replace(
            integer_responses[integer_case.case_id],
            state=integer_state,
        )
        self.assertIn(
            "expected int, got bool",
            " ".join(grade(self.cases, integer_responses)[integer_case.case_id]),
        )
        float_state = dict(integer_case.required_state)
        float_state["next_intervention.count"] = cast(JsonScalar, 1.0)
        float_responses = dict(self.responses)
        float_responses[integer_case.case_id] = replace(
            float_responses[integer_case.case_id],
            state=float_state,
        )
        self.assertIn(
            "expected int, got float",
            " ".join(grade(self.cases, float_responses)[integer_case.case_id]),
        )

        boolean_case = next(
            case for case in self.cases if case.case_id == "close-with-contradiction"
        )
        boolean_state = dict(boolean_case.required_state)
        boolean_state["closure.allowed"] = 0
        boolean_responses = dict(self.responses)
        boolean_responses[boolean_case.case_id] = replace(
            boolean_responses[boolean_case.case_id],
            state=boolean_state,
        )
        self.assertIn(
            "expected bool, got int",
            " ".join(grade(self.cases, boolean_responses)[boolean_case.case_id]),
        )

    def test_expected_responses_are_deterministic_synthetic_v2_records(self) -> None:
        self.assertEqual(expected_responses(self.cases), self.responses)
        self.assertTrue(
            all(
                response.provenance_kind == "synthetic" and response.evidence_refs
                for response in self.responses.values()
            )
        )

    def test_emitted_prompt_contract_is_case_scoped_and_nonrevealing(self) -> None:
        real_prompts = emit_prompts(
            "policy",
            self.cases,
            provenance_kind="real",
        )
        synthetic_prompts = emit_prompts(
            "policy",
            self.cases,
            provenance_kind="synthetic",
        )
        self.assertEqual(len(real_prompts), len(self.cases))
        self.assertEqual(len(synthetic_prompts), len(self.cases))
        contracts: dict[str, JsonObject] = {}
        for case, real_prompt, synthetic_prompt in zip(
            self.cases,
            real_prompts,
            synthetic_prompts,
            strict=True,
        ):
            with self.subTest(case_id=case.case_id):
                self.assertEqual(real_prompt["case_id"], case.case_id)
                self.assertEqual(synthetic_prompt["case_id"], case.case_id)
                real_contract = cast(JsonObject, real_prompt["contract"])
                synthetic_contract = cast(JsonObject, synthetic_prompt["contract"])
                contracts[case.case_id] = real_contract
                self.assertEqual(
                    set(real_contract),
                    {
                        "case_id",
                        "provenance_kind",
                        "response_fields",
                        "candidate_action_ids",
                        "state_types",
                        "evidence_refs",
                    },
                )
                self.assertEqual(real_contract["case_id"], case.case_id)
                self.assertEqual(real_contract["provenance_kind"], "real")
                self.assertEqual(synthetic_contract["provenance_kind"], "synthetic")
                self.assertEqual(
                    real_contract["response_fields"],
                    [
                        "case_id",
                        "decision_ids",
                        "next_action_id",
                        "state",
                        "provenance_kind",
                        "evidence_refs",
                    ],
                )
                self.assertEqual(
                    real_contract["candidate_action_ids"],
                    sorted(case.required_decisions | case.prohibited_actions),
                )
                self.assertEqual(
                    real_contract["state_types"],
                    {
                        key: self._json_type_name(value)
                        for key, value in case.required_state.items()
                    },
                )
                self.assertEqual(
                    real_contract["evidence_refs"],
                    list(case.evidence_refs),
                )
                self.assertEqual(
                    {
                        key: value
                        for key, value in synthetic_contract.items()
                        if key != "provenance_kind"
                    },
                    {
                        key: value
                        for key, value in real_contract.items()
                        if key != "provenance_kind"
                    },
                )
                self.assertNotIn("required_decisions", real_contract)
                self.assertNotIn("prohibited_actions", real_contract)
                self.assertNotIn("required_next_action", real_contract)
                self.assertNotIn("required_state", real_contract)
                rendered_contract = json.dumps(
                    real_contract,
                    sort_keys=True,
                    separators=(",", ":"),
                )
                prompt = real_prompt["prompt"]
                self.assertIsInstance(prompt, str)
                assert isinstance(prompt, str)
                self.assertIn(rendered_contract, prompt)
        self.assertNotEqual(
            contracts["partial-authoritative-rejection"]["state_types"],
            contracts["close-with-contradiction"]["state_types"],
        )

    @staticmethod
    def _json_type_name(value: JsonScalar) -> str:
        if isinstance(value, str):
            return "string"
        if type(value) is int:
            return "integer"
        if type(value) is bool:
            return "boolean"
        assert value is None
        return "null"

    @staticmethod
    def _response_items(bundle: JsonObject) -> list[JsonObject]:
        items = bundle["responses"]
        assert isinstance(items, list)
        responses: list[JsonObject] = []
        for item in cast(list[object], items):
            assert isinstance(item, dict)
            responses.append(cast(JsonObject, item))
        return responses

    @classmethod
    def _first_response(cls, bundle: JsonObject) -> JsonObject:
        return cls._response_items(bundle)[0]

    @staticmethod
    def _first_state(bundle: JsonObject) -> JsonObject:
        return ModelControlSchemaV2Tests._state_for_case(
            bundle,
            "partial-authoritative-rejection",
        )

    @staticmethod
    def _state_for_case(bundle: JsonObject, case_id: str) -> JsonObject:
        response = next(
            response
            for response in ModelControlSchemaV2Tests._response_items(bundle)
            if response["case_id"] == case_id
        )
        state = response["state"]
        assert isinstance(state, dict)
        return cast(JsonObject, state)

    @staticmethod
    def _run(bundle: JsonObject) -> JsonObject:
        run = bundle["run"]
        assert isinstance(run, dict)
        return cast(JsonObject, run)


if __name__ == "__main__":
    import unittest

    _ = unittest.main()
