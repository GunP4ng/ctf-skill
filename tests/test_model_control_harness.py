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
SEMANTIC_SHA256 = "78309f79d32a3cb67b8b7517d6e261a5f99546464ce04fbca5af9b83932ddd03"
FAMILY_CASE_IDS = (
    "family-equal-prediction-grouping",
    "family-distinct-prediction-separation",
    "family-covered-reject-retirement",
    "family-dependent-retirement",
    "family-reopen-on-new-evidence",
)
DISPOSITION_CASE_IDS = (
    "child-wave-missing-disposition",
    "child-wave-unsupported-state-change",
)
REVIEW_CASE_IDS = (
    "review-escalation-premature",
    "review-escalation-authorized",
    "review-output-requires-root-replay",
)
TRANSACTION_CASE_IDS = (
    "prepare-before-future-evidence",
    "completed-child-exact-disposition",
    "canonical-no-information-pivot-or-review",
    "user-supplied-mechanism-remains-assisted",
    "reproduced-candidate-latches-closure",
)
WEAK_TRAIT_CASE_IDS = (
    "direct-discriminator-before-monolithic-solver",
    "solver-timeout-encoding-same-fingerprint",
    "budget-stop-missing-accounting",
    "target-irrelevant-decode-not-progress",
    "uninspected-affordable-frontier-blocks-closure",
)
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
    *FAMILY_CASE_IDS,
    *DISPOSITION_CASE_IDS,
    *REVIEW_CASE_IDS,
    *TRANSACTION_CASE_IDS,
    *WEAK_TRAIT_CASE_IDS,
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

    def _case(self, case_id: str) -> Case:
        return next(case for case in self.cases if case.case_id == case_id)

    def test_family_cases_expose_the_active_family_contract(self) -> None:
        required_state_keys = (
            "family.family_id",
            "family.predicted_observation",
            "family.cheapest_discriminator",
            "family.accept_signal",
            "family.reject_signal",
            "family.prerequisite_coverage",
        )
        for case_id in FAMILY_CASE_IDS:
            with self.subTest(case_id=case_id):
                case = self._case(case_id)
                for key in required_state_keys:
                    self.assertIn(key, case.required_state)
                    self.assertIsInstance(case.required_state[key], str)

    def test_equal_predictions_require_one_family_and_distinct_ones_split(
        self,
    ) -> None:
        grouping = self._case("family-equal-prediction-grouping")
        self.assertEqual(grouping.required_state["family.active_count"], 1)
        self.assertIn("group_equal_prediction_family", grouping.required_decisions)
        self.assertIn("split_equal_prediction_family", grouping.prohibited_actions)

        separation = self._case("family-distinct-prediction-separation")
        self.assertEqual(separation.required_state["family.active_count"], 2)
        self.assertIn(
            "separate_distinct_prediction_family",
            separation.required_decisions,
        )
        self.assertIn(
            "merge_distinct_prediction_family",
            separation.prohibited_actions,
        )

    def test_retirement_requires_coverage_and_reopens_on_new_evidence(self) -> None:
        covered = self._case("family-covered-reject-retirement")
        self.assertEqual(covered.required_state["family.status"], "retired")
        self.assertIn("retire_covered_reject_family", covered.required_decisions)
        self.assertIn(
            "retire_uncovered_reject_family",
            covered.prohibited_actions,
        )

        dependent = self._case("family-dependent-retirement")
        self.assertEqual(dependent.required_state["dependent.retired_count"], 1)
        self.assertEqual(dependent.required_state["dependent.active_count"], 1)
        self.assertIn("retire_impossible_dependent", dependent.required_decisions)
        self.assertIn("retire_unaffected_dependent", dependent.prohibited_actions)

        reopened = self._case("family-reopen-on-new-evidence")
        self.assertEqual(reopened.required_state["family.status"], "active")
        self.assertIn("reopen_retired_family", reopened.required_decisions)
        self.assertIn("keep_invalidated_retirement", reopened.prohibited_actions)

    def test_grader_rejects_split_equal_predictions_and_uncovered_retirement(
        self,
    ) -> None:
        self.assertEqual(grade(self.cases, self.responses), {})

        grouping = self._case("family-equal-prediction-grouping")
        split = dict(self.responses)
        split[grouping.case_id] = replace(
            split[grouping.case_id],
            decision_ids=(
                (grouping.required_decisions - {"group_equal_prediction_family"})
                | {"split_equal_prediction_family"}
            ),
            state={**grouping.required_state, "family.active_count": 2},
        )
        self.assertTrue(grade(self.cases, split)[grouping.case_id])

        covered = self._case("family-covered-reject-retirement")
        uncovered = dict(self.responses)
        uncovered[covered.case_id] = replace(
            uncovered[covered.case_id],
            decision_ids=(
                covered.required_decisions | {"retire_uncovered_reject_family"}
            ),
        )
        self.assertTrue(grade(self.cases, uncovered)[covered.case_id])

    def test_child_wave_disposition_records_every_required_field(self) -> None:
        required_state_keys = (
            "disposition.child_id",
            "disposition.evidence_ref",
            "disposition.family_id",
            "disposition.status",
            "disposition.modeled_state_change",
        )
        for case_id in DISPOSITION_CASE_IDS:
            with self.subTest(case_id=case_id):
                case = self._case(case_id)
                for key in required_state_keys:
                    self.assertIn(key, case.required_state)
                    self.assertIsInstance(case.required_state[key], str)

        missing = self._case("child-wave-missing-disposition")
        self.assertEqual(missing.required_state["disposition.status"], "pending")
        self.assertEqual(
            missing.required_state["disposition.modeled_state_change"],
            "none",
        )
        self.assertIn("record_root_disposition", missing.required_decisions)
        self.assertIn(
            "promote_child_output_without_disposition",
            missing.prohibited_actions,
        )

        unsupported = self._case("child-wave-unsupported-state-change")
        self.assertEqual(
            unsupported.required_state["disposition.status"],
            "rejected",
        )
        self.assertEqual(
            unsupported.required_state["disposition.modeled_state_change"],
            "none",
        )
        self.assertIn("reject_unsupported_state_change", unsupported.required_decisions)
        self.assertIn(
            "apply_unsupported_state_change",
            unsupported.prohibited_actions,
        )

    def test_review_escalation_is_bounded_and_never_submits(self) -> None:
        required_state_keys = (
            "review.no_information_rounds",
            "review.pending_discriminator",
            "review.material_pivot",
            "review.untested_prior_proposal",
            "review.activation",
            "review.external_submission",
        )
        for case_id in ("review-escalation-premature", "review-escalation-authorized"):
            with self.subTest(case_id=case_id):
                case = self._case(case_id)
                for key in required_state_keys:
                    self.assertIn(key, case.required_state)
                self.assertEqual(
                    case.required_state["review.external_submission"], "none"
                )

        premature = self._case("review-escalation-premature")
        self.assertEqual(premature.required_state["review.no_information_rounds"], 1)
        self.assertEqual(premature.required_state["review.activation"], "withheld")
        self.assertIn("continue_local_discriminator", premature.required_decisions)
        self.assertIn("activate_ctf_review", premature.prohibited_actions)

        authorized = self._case("review-escalation-authorized")
        self.assertEqual(authorized.required_state["review.no_information_rounds"], 2)
        self.assertEqual(
            authorized.required_state["review.pending_discriminator"], "none"
        )
        self.assertEqual(authorized.required_state["review.material_pivot"], "none")
        self.assertEqual(
            authorized.required_state["review.untested_prior_proposal"],
            "none",
        )
        self.assertEqual(authorized.required_state["review.activation"], "prepared")
        self.assertIn("activate_ctf_review", authorized.required_decisions)
        self.assertIn("submit_review_packet_externally", authorized.prohibited_actions)

    def test_review_output_stays_advisory_until_root_replay(self) -> None:
        replay = self._case("review-output-requires-root-replay")
        self.assertEqual(replay.required_state["review.output_authority"], "advisory")
        self.assertEqual(replay.required_state["review.root_replay"], "required")
        self.assertIsNone(replay.required_state["result"])
        self.assertIsNone(replay.required_state["termination"])
        self.assertIn("replay_review_output_locally", replay.required_decisions)
        self.assertIn("promote_review_output_as_terminal", replay.prohibited_actions)

    def test_grader_rejects_missing_disposition_and_unreplayed_review_output(
        self,
    ) -> None:
        self.assertEqual(grade(self.cases, self.responses), {})

        missing = self._case("child-wave-missing-disposition")
        promoted = dict(self.responses)
        promoted[missing.case_id] = replace(
            promoted[missing.case_id],
            decision_ids=(
                (missing.required_decisions - {"record_root_disposition"})
                | {"promote_child_output_without_disposition"}
            ),
            state={**missing.required_state, "disposition.status": "accepted"},
        )
        self.assertTrue(grade(self.cases, promoted)[missing.case_id])

        premature = self._case("review-escalation-premature")
        early = dict(self.responses)
        early[premature.case_id] = replace(
            early[premature.case_id],
            decision_ids=premature.required_decisions | {"activate_ctf_review"},
            state={**premature.required_state, "review.activation": "prepared"},
        )
        self.assertTrue(grade(self.cases, early)[premature.case_id])

        replay = self._case("review-output-requires-root-replay")
        unreplayed = dict(self.responses)
        unreplayed[replay.case_id] = replace(
            unreplayed[replay.case_id],
            decision_ids=(
                (replay.required_decisions - {"replay_review_output_locally"})
                | {"promote_review_output_as_terminal"}
            ),
            state={
                **replay.required_state,
                "review.output_authority": "terminal",
                "result": "solved",
                "termination": "completed",
            },
        )
        self.assertTrue(grade(self.cases, unreplayed)[replay.case_id])

    def test_preserves_the_pinned_72_case_semantics(self) -> None:
        raw_cases = cast(
            list[JsonObject],
            json.loads(CASES_PATH.read_text(encoding="utf-8")),
        )
        self.assertEqual(tuple(case.case_id for case in self.cases), CASE_IDS)
        self.assertEqual(len(self.cases), 72)
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
        self.assertEqual(len({case.case_id for case in self.cases}), 72)

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
