---
name: ctf-solving
description: "MUST USE for authorized CTF solving across crypto, forensics, misc, pwn, reverse engineering/rev, and web. Adds evidence-based target, hypothesis, intervention, and closure controls within the existing debugging, execution, and review workflow."
---

# CTF Solving Policy

Use this policy for authorized CTF work only. Route by observed artifact or runtime surface, not by challenge title.

## Control intent

- Bound search by evidence and use the smallest decision-changing discriminator.
- Require explicit target, oracle, and acceptance surface before techniques.
- Preserve claim provenance.
- Stop expanding search once no affordable intervention can change the decision; close on the validator when it is available, otherwise record the correct terminal pair.

The surrounding workflow remains authoritative for orchestration, plans, progress tracking, durable notes, reviews, cleanup, and completion. This policy records only `ctf_attempt` and never mutates those controls.

Before investigation, activate up to three provenance-backed hypothesis families, each with distinguishing evidence and one investigation assignment: activate three when the evidence supports three, otherwise activate every supported family and record the evidence gap that keeps the count lower, naming what observation would raise it. Never invent an unprovenanced family to reach a count; one supported family is a legal start. Extra formed candidates stay reserve and never count as active.

For each mutation, declare its stateful-resource boundary set: artifact; environment/session/actor; and shared validator/account/service/resource. Intersecting sets serialize through recorded outcome and state update. Disjoint passive reads, reviews, and immutable isolated replicas may parallelize.

## 1) Target contract

Before any technique, record these seven fields: (1) exact target, (2) required artifacts, (3) controllable input, (4) observable intermediate state, (5) local oracle, (6) real acceptance surface, (7) budget and stop condition.

If an unknown local oracle or an undocumented but reachable acceptance surface is evidence-derivable, choose one bounded discovery experiment before theorizing or blocking. One known-wrong submission may discriminate accept from reject. For a planning-only request, name that experiment without claiming to have run it and never invent its observation. An unexecuted observation keeps the attempt live with every terminal field null. If the planning request itself finishes while that observation is still pending, use `result: no-result` with the exact pending reason and the matching termination; use `partial` only when some other useful fact was actually proven.

Require enough artifact and target evidence to define the target contract. If the artifact or execution boundary is unavailable and non-derivable, use `termination: blocked`, with `result: partial` only when a useful fact was proven and `no-result` otherwise. Preserve the boundary, proof, unblock, and validator-unavailable evidence.

## 2) Capability ledger

Maintain a capability ledger with provenance-qualified evidence only. Each entry is an observed, missing, or unknown capability and cites its proving artifact, runtime observation, parser output, service reply, or session state. Inference alone cannot promote capability.

## 3) Hypothesis control

Keep at most three actively tested families.

Each family must state its prerequisite, one bounded intervention, true signal, false signal, retirement condition, and evidence provenance.

Rules:

- use mutual exclusivity only when supported by evidence
- represent a compound hypothesis as one slot with one prediction
- choose the cheapest separator across active families
- use `tie, arbitrary pick` only for evidence-equivalent non-promotion interventions, then choose one without invented justification
- keep reserve as a separate provenance-qualified set; do not make it a required per-family field
- keep reserve candidates unretired until the declaring evidence resolves them

Reserve admission and promotion:

- admit only a unique provenance-backed candidate whose bounded intervention fits budget and can change the decision or closure; otherwise retain one aggregate `unfunded candidates` unknown without identity or prerequisite role
- after initialization or an intervention update opens a slot, promote exactly one reserve with proven matching-context prerequisites and an executable bounded intervention
- prioritize closure-changing evidence, discrimination per declared worst-case cost, then stable insertion order; record reason and provenance, never weighted scoring
- bounded inconclusive work demotes the candidate, which stays ineligible until new evidence bears on it
- matching-context direct refutation retires the candidate and any dependents whose prerequisites become impossible
- new evidence that invalidates a retirement reopens only candidates currently supported by proven prerequisites, and only when budget permits
- an active family without an affordable bounded intervention demotes to reserve as an evidence-driven update, opening its slot
- continue while any affordable active bounded intervention, validator or acceptance closure action, or funded eligible reserve remains; terminalize only when none remains

Budget: record unit, limit, used, and remaining, and never invent scheduler state; reconcile only immediately before a prospective `budget-stop`, never to resume after `solved`, `interrupted`, or `blocked`.

## 4) Contradiction handling

Before treating a contradiction as fatal, compare source, artifact hash, environment, session, freshness, and parser/tool version. If any of these differ, treat the contradiction as a possible context mismatch first. Do not invalidate a whole plan from an unqualified contradiction.

## 5) Delegation

Delegate only disjoint work with immutable isolated inputs. The surrounding workflow owns execution and delegation; this policy defines only what a delegated lane may contain.

Rules:

- non-overlapping lanes only: reject duplicate scope and merge duplicate candidate paths
- parent exclusively owns overlap registry, candidate promotion, and closure
- each worker receives immutable, isolated state only and may not mutate shared solver state
- explicit independent replication is allowed only when the replication inputs are isolated and the observation is independently sourced. Represent it as one bounded replication intervention card with one aggregate budget, and resolve or cancel every member before recording its single state update

A handoff must contain only proven facts, active families, retired families, reserve candidates, unknowns, and exactly one bounded next intervention card with its prerequisite, immutable scoped inputs, one mutation, and expected true and false signals. Keep reserve candidates unproven and separate; never promote an unproven assumption through the intervention card.

## 6) Execution loop

Use this loop:

- pin: preserve originals and record hashes
- read: optionally perform at most one cost-free immutable side-effect-free read batch before an intervention, limited to reads already available without new setup
- model: keep the active hypothesis set small
- discriminate: run exactly one bounded next intervention and record raw output
- close: replay cleanly, then validate on the real acceptance surface

Active families are models, not concurrent jobs. Serialize intervention cards whose declared stateful-resource boundary sets intersect. Finish a card's true, false, inconclusive, or bounded-cancel outcome before its update, terminal decision, or next card. Replica members form one update before terminalization.

Before any context reduction, transfer raw output into an immutable external artifact, then retain in context only its hash/reference plus provenance, discriminator result, and resulting state change. Never reduce, overwrite, or delete the sole copy of required raw evidence before that transfer completes, and never fabricate output that was not observed. Temporary raw debugging artifacts that are not sole required evidence need not be permanent and must be removed when no longer required.

Decision-state projection/canonicalization rewrites only `ctf_attempt`; it is not session compaction and never mutates surrounding durable state. After session compaction, reread applicable controls and durable state. Projection preserves in-flight identity and its durable outcome receipt so interruption or projection cannot execute or record a mutation twice.

A verified useful primitive immediately schedules a clean local replay, then real acceptance. New research waits until that closes or fails. Multi-variable interaction testing starts only after proven coupling or valid constituent nulls, with a predeclared combined prediction. Passive observation batching is optional; a loop may proceed without one.

## 7) Results and terminations

Use exactly one `result` and exactly one `termination`.

Results: `solved`, `failed-with-valid-oracle`, `partial`, or `no-result`.

Terminations: `completed`, `blocked`, `interrupted`, or `budget-stop`.

Legal pairs: `solved` only with `completed`; `failed-with-valid-oracle` only with `completed` or `budget-stop`; `partial` with any termination; `no-result` with any termination.

Store these only in `ctf_attempt`. While live, `result`, `termination`, `terminal_event`, `validator_response`, and `closure` are null. One terminal transition populates all five exactly once, at the validator or attempt outcome and before any surrounding cleanup, and freezes them; projection, cleanup interruption, or any later event can neither duplicate nor rewrite them.

- `solved`: clean local mechanism plus real validator/flag acceptance response.
- `failed-with-valid-oracle`: valid oracle identity plus bounded rejection observations and budget/stop terminal event; never claim plausible failure without a valid oracle.
- `partial`: useful fact/primitive/local proxy evidence plus explicit absence of real acceptance; local-only remains partial.
- `no-result`: exact reason no useful fact was proven, including a planning-only request whose observation was never executed.

Every terminal record names result, termination, artifact/environment identity (hashes where available), terminal event, validator response, and closure. Name the same validator consistently across records. If it is unavailable, record `not-run` or `unavailable` with the exact reason.

For `blocked`: unavailable boundary, required proof, unblock condition, validator reason; `interrupted`: external event, last proven state, `not-run` reason; `budget-stop`: limit and validator status; `completed`: terminal action and current cleanup status.

Because the pair freezes first, an accepted validation whose cleanup is later interrupted stays `solved` + `completed` with cleanup status recorded as incomplete and its interrupting event named; the frozen `ctf_attempt` is not rewritten, and only the surrounding workflow stays unfinished until cleanup completes.

## 8) Domain routing

Route by observed artifact or surface.

- crypto: verify format/oracle; block on artifact/verifier; close with local verification and acceptance.
- forensics: verify provenance/immutability; block on integrity; close with proven recovery and acceptance.
- misc: classify structure; block on artifact/process; close with rule resolution and acceptance.
- pwn: test runtime/process; block on runtime/service; close with end-to-end replay and acceptance.
- reverse: model then observe state; block on runtime/parser; close with behavior match and acceptance.
- web: map reset, actor, and data boundaries; block on service/endpoint; close with request replay and acceptance.

## 9) State form

The canonical `ctf_attempt` contains only these fields:

- target contract
- artifact/environment identity
- capabilities
- active, reserve, and retired families
- unknowns
- optional passive observation batch
- exactly one next bounded intervention
- nullable `in_flight_bounded_intervention`
- budget
- compact experiment evidence references
- result, termination, terminal event, validator response, and closure

In-flight is distinct from next: atomically move next into it before mutation, then clear it only after recording the bounded outcome and durable receipt. It is null when no mutation runs. Next may be null live while choosing, while the named card it was moved into is in flight, or while terminalizing; both are null terminally. Terminal fields follow section 7.

## 10) Completion

Reuse a receipt only for one current-turn invocation of the exact user-facing surface on the exact current reviewed artifact/environment with the same acceptance criterion. It contains surface execution, validator/acceptance, and cleanup. If the challenge validator and the user-facing surface you are asked to demonstrate are different surfaces, exercise both; never reuse validator-only evidence as if it covered the user-facing surface. Reference the durable receipt from `ctf_attempt`.

Record the attempt as finished only when the target contract is satisfied, the chosen result and termination carry their result- and termination-specific evidence semantics—every finished attempt, including `partial`, has the complete terminal record required by section 7—and decision evidence has a durable receipt/reference.

The surrounding workflow declares overall finish only after cleanup completes and no extra workers or temp resources remain. A pending or interrupted cleanup blocks that declaration and never alters the frozen `ctf_attempt` record.

Do not add reference links, external paths, or hidden companion docs. This file is the policy.
