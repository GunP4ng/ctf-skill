---
name: ctf-solving
description: "MUST USE for authorized CTF solving across crypto, forensics, misc, pwn, reverse engineering/rev, and web. Adds evidence-based target, hypothesis, intervention, and closure controls within the existing debugging, execution, and review workflow."
---

# CTF Solving Policy

Use this policy only for an authorized CTF target. Route by observed artifact or
runtime surface, not by challenge title.

## Control intent

- Keep reasoning and read-only exploration flexible; govern external actions,
  durable state changes, and official claims.
- Prefer the smallest affordable experiment that can change a decision.
- Preserve actual bytes and observations before reducing them to summaries.
- Separate local models and surrogate behavior from authoritative acceptance.
- Treat policy bookkeeping as coordination, never as technical progress.

## 1) Target contract

Before an intervention, record these eight fields: (1) exact target and
authorized scope, (2) required artifacts, (3) controllable input, (4) observable
intermediate state, (5) local oracle, (6) discovery surface, (7) real acceptance
surface, and (8) budget and stop condition. The discovery surface names the
artifact, runtime, instrumentation, reconstruction, emulation, static analysis,
or bounded acquisition path on which facts can still be proven. Acceptance
unavailability affects closure only; it does not erase a reachable discovery
surface.

If a local oracle or reachable acceptance surface is unknown but
evidence-derivable, choose one bounded discovery experiment before theorizing
or blocking. A planning-only request may name the experiment but must not claim
that it ran. An unexecuted observation keeps terminal fields null.

Pin target and acceptance identities. Revisions are append-only: retain prior
identities and require direct user, organizer, or authoritative target evidence
for the replacement. A surrogate, guess, timeout, or local rejection cannot
nominate a new target.

Use `blocked` only when every decision-changing acquisition, reconstruction,
rehosting, emulation, static-analysis, or acceptance action is unavailable or
non-derivable. Record the boundary, proof, attempted or excluded action, unblock
condition, and validator status.

## 2) Local models, surrogates, and candidate sets

Create acceptance-model bookkeeping only when a local predicate or reconstructed
decision affects prioritization, retirement, uniqueness, or closure. Record the
known predicate, provenance, reached frontier, unresolved downstream decision,
and completeness as `unknown`, `frontier-complete`, or
`authoritative-complete`. Never infer completeness from missing evidence.

A surrogate is any mock, emulator, replica, patch, lift, deobfuscation,
reimplementation, or local substitute. Bind each fidelity claim to the
authoritative target, surrogate artifact and configuration, relevant runtime
and environment, matched inputs and observables, first material divergence, and
claim scope. Multi-hop scope is the intersection of its lineage. A change
invalidates only the fidelity facts it can affect; extend scope only through a
new authoritative comparison. Local success never becomes authoritative
acceptance.

If a local predicate is not proven injective, preserve every known candidate or
a lossless constraint/equivalence-class representation. Record uniqueness as
`proven` only with a single-preimage or injectivity receipt, `disproven` when
distinct candidates are observed, and `unknown` otherwise. Do not commit the
first local solution as unique or enumerate a large symbolic set when its
constraints can be preserved losslessly.

## 3) Capability and hypothesis control

Maintain a provenance-qualified capability ledger. Each capability is
`observed`, `missing`, or `unknown` and cites its artifact, runtime observation,
parser output, service reply, or session state. Inference alone cannot promote
capability.

Keep at most three actively tested hypothesis families. Preserve every other
supported family in reserve by identity or a provenance-backed grouped
representation; never collapse decision-relevant candidates into an anonymous
unknown.

Each active family states its prerequisite, one bounded intervention, true
signal, false signal, retirement condition, evidence provenance, and the
prerequisite coverage required for a valid falsifier.

- choose the cheapest separator across active families;
- use mutual exclusivity only when evidence proves it;
- represent a compound hypothesis as one slot with one prediction;
- promote one funded reserve when a slot opens, preferring closure-changing
  evidence, discrimination per proven cost, then stable insertion order;
- demote after bounded inconclusive work only as a prioritization change and
  preserve the family for later evidence;
- leave eligibility unchanged when an intervention lacks prerequisite coverage
  or produces the same signal in both prerequisite states;
- retire only when a falsifier-coverage receipt proves the prerequisite was
  tested in matching context and the observed signal distinguishes its states;
- retire dependents only when the covered refutation makes their prerequisites
  impossible; and
- reopen a retirement when new evidence invalidates it.

Record budget unit, limit, used, remaining, and provenance for every
budget-consuming action. An action is proven affordable only when a credible
upper bound fits; it is proven unaffordable only when a credible lower bound
exceeds the remainder. Otherwise cost is unknown and needs a bounded audit.
Reconcile after budget-consuming actions and before any terminal affordability
decision. Never alter accounting merely to justify continuation or stopping.

## 4) Contradiction handling

Preserve contradictions explicitly and scope each one to the claim it affects.
Before treating one as fatal, compare source, artifact hash, environment,
session, freshness, and parser/tool version. A context mismatch explains scope;
it does not erase the observation.

Rejection can contradict an acceptance prediction. Error, timeout, ambiguity,
or unavailability instead creates an acceptance unknown unless it proves a
semantic result. Only a decision-relevant unresolved contradiction blocks that
claim. Authoritative acceptance outranks a surrogate prediction for acceptance,
while unrelated contradictions remain recorded.

## 5) Delegation and side effects

Give workers immutable, disjoint scopes: question, artifact, allowed tools,
budget, output schema, and stop condition. The parent owns hypothesis
promotion, canonical state changes, and closure. Worker prose is evidence input,
not authority.

Serialize interventions whose stateful-resource boundaries intersect. Disjoint
bounded reads or experiments may run concurrently when their outputs and
mutation rights remain isolated.

Treat submissions, destructive changes, account lockout risk, one-shot
services, credentials, and rate limits as explicit side-effect boundaries.
Record permission and cost before crossing one. Any trusted stop request pauses
new mutations and triggers bounded cancellation.

## 6) Execution loop

Use this loop:

1. **Pin** — preserve originals and record identities or hashes.
2. **Read** — batch bounded side-effect-free observations while their cost and
   output remain controlled.
3. **Model** — keep active families small and preserve reserve identities.
4. **Discriminate** — run one bounded decision-changing intervention.
5. **Settle** — retain raw output, record the actual outcome, then update state.
6. **Close** — replay when feasible and use the real acceptance surface.

Before an intervention, declare its expected discriminator, bounded cost,
stateful-resource boundary, display ceiling, and durable raw-output destination.
Do not overwrite the sole copy of required evidence. Context keeps only bounded
output plus its reference, provenance, discriminator result, and state change.
Never invent or silently normalize unobserved output.

Atomically mark a mutation in flight before execution and settle it once from a
durable outcome receipt. Interruption, compaction, or recovery must not execute
or record the mutation twice.

Track consecutive no-information outcomes by semantic fingerprint: modeled
state, decomposition, relevant unknowns, and observable predicate. After two,
require new evidence, a material representation pivot, or a frontier audit
before a third equivalent intervention or terminal transition. Changing only
tool, engine, prompt, parameter, or implementation does not reset the count.

Before a non-`solved` terminal transition, record one compact frontier audit.
For discovery, representation pivot, active/reserve discrimination, and
acceptance closure, name the cheapest supported action or `none`, its
prerequisites, cost evidence, expected decision change, and reconciled budget.
`none` must cover the current artifact and every supported candidate. Any
affordable decision-changing action keeps the attempt live.

## 7) Results and terminations

Use one result and one termination.

- Results: `solved`, `failed-with-valid-oracle`, `partial`, or `no-result`.
- Terminations: `completed`, `blocked`, `interrupted`, or `budget-stop`.
- Legal pairs: `solved` only with `completed`;
  `failed-with-valid-oracle` with `completed` or `budget-stop`; `partial` or
  `no-result` with any termination.

While live, result, termination, terminal event, validator response, and closure
remain null. One atomic transition populates and freezes them before cleanup.

- `solved` requires authoritative acceptance and a clean replayable mechanism
  when feasible; for a one-shot or non-rehostable surface, retain the exact
  pinned invocation and acceptance receipt instead.
- `failed-with-valid-oracle` requires a valid oracle and bounded rejection
  evidence covering every remaining candidate.
- `partial` requires a useful proven fact plus explicit absence of acceptance.
- `no-result` records why no useful fact was proven.

Every terminal record names artifact/environment identity, terminal event,
validator response, closure evidence, and for a non-solved result its frontier
audit or genuine external-interruption exception. Acceptance remains solved if
later cleanup is interrupted; record cleanup separately without rewriting the
frozen attempt.

## 8) Domain routing

- **Crypto** — algebra, entropy, nonce/key reuse, oracle behavior, then bounded
  solving.
- **Forensics** — preserve originals; inspect metadata, structure, carving, and
  timeline before interpretation.
- **Pwn** — establish mitigations, crash control, primitive, clean local replay,
  then remote acceptance.
- **Reverse engineering** — map input to decision or state transition; distinguish
  static facts from runtime facts.
- **Web** — map source, routing, auth, parser, and session boundaries; preserve
  exact requests and responses.
- **Misc** — infer the governing state machine from observed behavior and test
  the smallest separator.

Domain-specific missing tools block only when no acquisition, reconstruction,
emulation, static-analysis, or authoritative path can derive the needed fact.

## 9) State form

Maintain one compact canonical attempt containing target and authorization,
artifact/environment identity, capabilities, active/reserve/retired families,
unknowns, budget, evidence references, at most one next bounded intervention,
nullable in-flight identity, and terminal fields.

Acceptance-model, surrogate, candidate-set, fingerprint, revision, and
contradiction records are optional and appear only when they affect a decision.
Projection is non-authoritative and must preserve in-flight and durable receipt
identity.

## 10) Completion

Reuse a receipt when it covers the exact artifact, environment, acceptance
criterion, and user-facing surface and remains fresh for the relevant
side-effect or rate-limit boundary. Do not force a harmful duplicate invocation
merely because the receipt came from an earlier turn. If validator and requested
demonstration are different surfaces, exercise both when safely possible.

Finish the attempt only when the target contract is satisfied, result and
termination carry their required evidence, and decision evidence has a durable
reference. Finish the surrounding workflow only after workers and temporary
resources are cleaned up.
