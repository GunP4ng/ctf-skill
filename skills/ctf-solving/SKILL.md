---
name: ctf-solving
description: "MUST USE for authorized CTF challenge solving and workflow design across crypto, forensics, misc, pwn, reverse engineering/rev, web, flags, solvers, and artifacts. Covers evidence-based target classification, oracle and acceptance discovery, bounded hypotheses, isolated delegation, provenance checks, blocker scoping, and local-to-real closure."
---

# CTF Solving Policy

Use this policy for authorized CTF work only. Route by observed artifact or runtime surface, not by challenge title.

## Control intent

- Keep search bounded by evidence.
- Prefer the smallest discriminator that can change the decision.
- Do not expand into techniques until the target, oracle, and acceptance surface are explicit.
- Preserve provenance for every claim.
- Stop when local usefulness exists but real acceptance is not yet proven.

## 1) Target contract

Before any technique, record these six fields:

1. exact target
2. required artifacts
3. controllable input
4. observable intermediate state
5. local oracle
6. real acceptance surface

If the local oracle is unknown but derivable, or if an undocumented real acceptance surface is available and the evidence can derive it, allow exactly one bounded discovery experiment. Make the decision mandatory and explicit: choose exactly one bounded oracle or acceptance discovery experiment as the immediate next action before theory or blocking. A supplied known-wrong sample that can be submitted once to observe accept/reject is a valid discriminator. For planning or decision-only requests, report that experiment as the decision without pretending it ran; a pending observation keeps the outcome `partial`. Apply this rule only when the evidence shows that the required artifact and target surface are available enough to define the experiment. If the artifact or execution boundary itself is unavailable and non-derivable, use `blocked-environment`; do not answer undetermined or blocked only because an otherwise feasible chosen discovery has not executed in the current context. Otherwise, stop only if no such derivation experiment is possible or the required exact boundary is unavailable.

## 2) Capability ledger

Maintain a capability ledger with provenance-qualified evidence only.

Allowed entries:
- observed capability
- missing capability
- unknown capability

Each entry must cite the source type that proved it, such as artifact, runtime observation, parser output, service reply, or session state. Do not promote capability from inference alone.

## 3) Hypothesis control

Keep at most three mutually exclusive hypotheses.

Each hypothesis must include:
- prerequisite
- one mutation
- true signal
- false signal
- retirement condition
- evidence provenance

Rules:
- change one variable only per experiment
- choose the cheapest experiment that separates the active hypotheses
- set exactly one next experiment
- retire a hypothesis family when its declared retirement condition is observed; two independent valid null discriminators are sufficient retirement evidence, not a prerequisite when another declared condition fires
- reopen a retired family only when a new proven fact invalidates the retirement evidence

## 4) Contradiction handling

Before treating a contradiction as fatal, compare:
- source
- artifact hash
- environment
- session
- freshness
- parser/tool version

If any of these differ, treat the contradiction as a possible context mismatch first. Do not invalidate a whole plan from an unqualified contradiction.

## 5) Delegation

Delegate only disjoint work with immutable isolated inputs.

Rules:
- non-overlapping lanes only
- reject duplicate scope
- merge duplicate candidate paths
- parent exclusively owns overlap registry, candidate promotion, and closure
- workers may not mutate shared solver state

A handoff must contain only proven facts, retired families, unknowns, and exactly one next experiment card with its prerequisite, immutable scoped inputs, one mutation, and expected true and false signals. Keep every unproven assumption under unknowns; never promote it through the experiment card.

## 6) Execution loop

Use this loop:

- pin: preserve originals and record hashes
- model: keep the active hypothesis set small
- discriminate: run one bounded experiment and record raw output
- close: replay cleanly, then validate on the real acceptance surface

A verified useful primitive immediately schedules a clean local replay, then real acceptance. New research waits until that closes or fails.

## 7) Outcomes

Use exactly one outcome:

- `solved`: clean local mechanism plus real validator/flag acceptance response.
- `failed-with-valid-oracle`: valid oracle identity plus bounded rejection observations and budget/stop terminal event; never plausible failure without a valid oracle.
- `blocked-environment`: exact unavailable artifact/process/service/credential/runtime/endpoint boundary, evidence it is required, and exact unblock condition; validator response may be `unavailable` with reason.
- `interrupted`: external stop/interrupt event, last proven state, and validator `not-run` reason; do not relabel as failed.
- `partial`: useful fact/primitive/local proxy evidence plus explicit absence of real acceptance; local-only remains partial.

Every terminal record must name the outcome, artifact/environment identity (hashes where available), terminal event, and validator response; when the validator cannot be exercised, record `not-run` or `unavailable` with the exact reason rather than fabricating a response.
## 8) Domain routing

Route by observed artifact or surface.

| Domain | Observed evidence cue | Earliest discriminator | Exact blocker boundary | Closure evidence |
| --- | --- | --- | --- | --- |
| crypto | ciphertext, nonce, MAC, signature, algebraic relation, key material | verify format and oracle behavior first | artifact or verifier boundary | local decode/verify plus real flag acceptance |
| forensics | disk image, memory dump, packet capture, timeline, metadata, provenance gaps | provenance and immutability check first | artifact integrity boundary | recovered artifact/state with provenance and flag proof |
| misc | mixed artifact, custom format, puzzle logic, hybrid surface | classify internal structure first | artifact or process boundary | local rule resolution and real acceptance |
| pwn | binary, process, fd, sandbox, syscall, crash, memory corruption | runtime/process boundary first | runtime or service boundary | local end-to-end exploit path and real acceptance |
| reverse | executable, decompiler output, obfuscated logic, trace, state transition | static model plus one observed intermediate state | runtime or parser boundary | original-program behavior match and flag proof |
| web | HTTP exchange, route, session, cookie, request state, CSRF, template, API | stable reset and actor/data boundary map first | service or endpoint boundary | local request replay and real acceptance |

## 9) State form

Keep a reusable state form with these fields only:
- target
- capabilities
- hypotheses
- retired families
- unknowns
- exactly one next action
- closure

## 10) Completion

Finish only when the following are true:
- target contract is satisfied
- the chosen outcome is recorded with outcome-specific evidence semantics, and every finished attempt—including `partial`—has the complete terminal record required by section 7
- evidence is preserved with provenance
- cleanup is complete
- no extra workers or temp resources remain

Do not add reference links, external paths, or hidden companion docs. This file is the policy.
