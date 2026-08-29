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
- Report observed evidence, the current candidate, and the next bounded action
  plainly. Apply machine formatting only when the active runtime supplies its
  contract; never invent a response schema.
- Keep organizer/reference solutions, expected flags/results, and official
  solution material outside solver context until candidate sealing; perform
  authoritative validation only afterward.

## Operational kernel

Keep one canonical next bounded action and advance the attempt through these
operational phases:

- **DISCOVERY** — pin the target, oracle, discovery surface, and acceptance
  surface; use the cheapest discriminator to establish a target-relevant fact.
- **BRIDGE** — convert a proven capability into the next replayable mechanism or
  candidate. Freeze unrelated discovery until that authority edge is completed
  or evidence falsifies it.
- **ACCEPTANCE** — after two independent root replays reproduce one candidate,
  stop solver and delegation work, preserve the candidate, and exercise the real
  acceptance surface.
- **CLEANUP** — settle children, mutations, processes, containers, credentials,
  and temporary artifacts before freezing result and termination.

A target-relevant capability creates closure debt: name its evidence and next
authority edge, then resolve that edge before opening another decision-changing
lane. A reproducible candidate latches acceptance work; an authoritative
rejection returns it to the appropriate live frontier without discarding the
rejection evidence.

The root disposition barrier is absolute. After every child wave, settle and
classify each completed child against its exact evidence before starting another
wave. At every phase, report the strongest evidence reference, changed state,
next bounded action, and next authority edge. Read-only exploration remains
flexible, but bookkeeping, renamed lanes, and equivalent retries are not
progress.

## 1) Target contract

Before an intervention, record these eight fields: (1) exact target and
authorized scope, (2) required artifacts, (3) controllable input, (4) observable
intermediate state, (5) local oracle, (6) discovery surface, (7) real acceptance
surface, and, only when a trusted authority declares one, (8) authoritative
budget and stop condition. A trusted budget declaration identifies its unit,
limit, and provenance from the user, organizer, or authoritative target. The
discovery surface names the artifact, runtime, instrumentation, reconstruction,
emulation, static analysis, or bounded acquisition path on which facts can still
be proven. Acceptance unavailability affects closure only; it does not erase a
reachable discovery surface.

Before a multi-round remote interaction, materialize one execution-boundary
card from observed target behavior:

```text
process/service lifetime:
estimated round trips and elapsed cost:
projected timeout risk:
pipeline-safe input-independent steps:
boundary-wait steps that consume binary or stateful input:
```

If lifetime is unknown, measure it on a fresh connection before funding the
full exploit. Pipeline only input-independent protocol groups; continue to wait
at every boundary where a short read, binary payload, parser state, or response
changes the next input.

If a local oracle or reachable acceptance surface is unknown but
evidence-derivable, choose one bounded discovery experiment before theorizing
or blocking. A planning-only request may name the experiment but must not claim
that it ran. An unexecuted observation keeps terminal fields null.

Pin target and acceptance identities. Revisions are append-only: retain prior
identities and require direct user, organizer, or authoritative target evidence
for the replacement. A surrogate, guess, timeout, or local rejection cannot
nominate a new target.

After each decision-changing intervention and before closure, record one compact
**Authority Closure Checkpoint**: the original target surface, local-oracle
surface, real acceptance surface, current candidate or lossless candidate set,
strongest evidence reference, capability just proven or ruled out, and the next
authority edge. A primitive closes only the surface on which it was proven. If
the next authority edge is still live, preserve it explicitly instead of
treating a local read, write, crash, decode, or replay as end-to-end closure.

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

A family is identified by what it predicts, not by who proposed it. Each active
family states six fields: `family_id`, the predicted observation, the cheapest
discriminator that can produce it, the accept signal, the reject signal, and the
prerequisite coverage required for a valid falsifier. A family missing any of
the six is not active; complete it or hold it in reserve.

Use stable machine identifiers for `family_id`, representation identity,
semantic subject, intervention, and predicate contract. They are identities,
not prose: use letters, digits, `.`, `_`, or `-`, with the explanation kept in
the accompanying reason. A family and a representation are independent. A
family predicts an outcome; a representation determines which properties are
visible. Never reuse one identifier as both merely because one experiment
mentions both.

A material representation pivot requires referenced source evidence, a
reproducible transform or model, observed output, and the newly visible property
or decision change. Announcing a new identifier, tool, backend, or parameter is
not representation progress. Credit progress only when that property changes
target capability, prerequisite coverage, a candidate, contradiction, bound, or
next decision. Preserve unrelated background decodes as raw observations, but
do not promote them to target progress or `partial`.

After the first no-information result in an active family, test representation
fitness before scaling or pivoting: name which target variable or boundary the
current representation exposes, which discriminator can observe it, and what
decision the observation would change. Prefer a smaller semantic probe at that
boundary over another whole solver. Deepen the current family when such a probe
exists; pivot only when referenced evidence shows the current representation
cannot expose the needed property.

- group proposals that share one predicted observation under the same discriminator
  into one `family_id`, regardless of how many workers or labels produced them;
- separate one label into distinct `family_id`s when it carries distinct predicted
  observations, so every active slot keeps exactly one prediction;
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
  tested in matching context and the observed reject signal distinguishes its
  states;
- retire dependents only when the covered refutation makes their prerequisites
  impossible, and preserve every dependent that independent evidence still
  supports; and
- reopen a retirement by `family_id` when new evidence invalidates its coverage
  receipt, restoring the family's declared prediction as untested.

Counting proposals, workers, or lanes is not modeling; only distinct predicted
observations create distinct families.

Before a costly solver, full-state search, or exploit build, name the cheapest
feasible discriminator and its family-dependent signals. If bypassing it,
record evidence showing why each cheaper separator cannot decide. When one
affordable direct observation can falsify a solver prerequisite, run it before
the solver; enough budget for both is not evidence to reverse that order.

Create an authoritative budget only when a trusted user, organizer, or
authoritative target declaration supplies its unit, limit, and provenance.
Record the declared unit, limit, used, remaining, and immutable provenance for
every action charged to that budget. An action is proven affordable only when a
credible upper bound fits the declared remainder; it is proven unaffordable only
when a credible lower bound exceeds that remainder. Otherwise its cost is
unknown and needs a bounded audit. Reconcile after a charged action and before
a terminal affordability decision.

Without that trusted declaration, omit budget state entirely and do not use
`budget-stop`. A controller quota, evaluator resource cap, elapsed time,
internal intervention count, agent estimate, or model-authored value is not
budget authority. Cost evidence can still choose the smaller bounded action,
but it cannot manufacture a budget remainder, an affordability conclusion, or a
terminal stop. Never alter authoritative accounting merely to justify
continuation or stopping.

`budget-stop` is available only when the declared unit, limit, used, remaining,
and provenance are present, trusted, and reconciled with `used == limit` and
`remaining == 0`. Any response that asserts or infers budget exhaustion while
terminalizing, stopping, or closing an attempt - through an action, a composite
of actions, or a termination state - requires that same authoritative,
reconciled record. If any condition is absent, keep the attempt live or use the
actual non-budget termination reason; never request, infer, or synthesize a
budget record merely to stop.

Before committing a large or staged search to a hand-derived model, execute two
or three of its predictions directly against the target and compare outputs byte
for byte. Any mismatch invalidates the model; fix the semantics first. A search
over a falsified model produces only negative information at full cost.

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
output schema, and stop condition. Include an authoritative budget only when it
is inherited unchanged from trusted user, organizer, or authoritative target
evidence, including its unit, limit, used, remaining, and immutable provenance.
Internal worker limits, controller quotas, evaluator caps, and parent scheduling
limits remain hidden controller constraints: they are not budget authority and
cannot authorize `budget-stop`. The parent owns hypothesis promotion, canonical
state changes, and closure. Worker prose is evidence input, not authority.

After each child wave, record one compact root disposition per child with five
fields: `child_id`, the evidence reference it is judged on, the `family_id` it
affects, `accepted`, `rejected`, or `pending`, and the changed modeled state or
`none`. A child result without a disposition changes nothing, and a child claim
whose cited evidence does not meet this policy's requirement for that state
change is `rejected` with `none` as its state change; the affected family keeps
its current eligibility. Only an `accepted` disposition may carry a non-`none`
modeled state change. Child, external oracle, and external review output stays
advisory until the root reproduces it.

**Child lease.** Each semantic frontier owns at most one unresolved child lease.
Before opening another child on that frontier, the root must read the exact
receipt, replay decisive observations when required, retain or discard it, and
close or explicitly transfer the lease. A pending, missing, or guessed receipt
never authorizes a second lease on that frontier. Independent frontiers may run
parallel children. A transferred lease names its recipient and unresolved
question; an unclosed lease remains owned by its original frontier.

When multiple children return no decision-changing evidence, merge their shared
blocked variables and observables into one root no-progress record before
another wave. Sibling labels, prompts, or implementations do not create new
families and do not reset the semantic no-information count.

Use this exact child sequence:

1. wait for or fetch the terminal child result;
2. use the harness-projected evidence ID bound to that child, never a guessed
   or nearby receipt;
3. reproduce any decision-changing claim at the root when feasible;
4. record the child's `accepted`, `rejected`, or `pending` disposition;
5. only then spawn another child or request external review.

If the harness reports an unresolved child, settle or cancel that exact child.
If it reports a completed undispositioned child, classify the exact projected
child/evidence pair. Never pair one child's output with another receipt.
Before cancelling a lane, preserve one handoff artifact with `family_id`,
representation identity, last evidence reference, unresolved question, and the
next bounded discriminator or `none`. Cancellation without that handoff changes
no modeled state.

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
3. **Model** — keep active families small, one prediction per `family_id`, and
   preserve reserve identities.
4. **Discriminate** — run the cheapest discriminator that separates active
   predictions, as one bounded decision-changing intervention.
   Record its prerequisite coverage with the observed signal; an uncovered
   observation settles nothing about eligibility.
5. **Settle** — retain raw output, record the actual outcome, then update state.
6. **Close** — replay when feasible and use the real acceptance surface.

**Decision Compression.** After every decision-changing result, before any next
action, internally refresh exactly these four lines:
`Current frontier`
`Last semantic result`
`Cheapest unresolved discriminator`
`Exact next action`
This is state control, not a new research thread or progress result. Each
refresh names one frontier and one exact action; a menu or bundle is not exact.
Do not open a new family, child, research thread, or representation until that
exact next action has executed to a semantic outcome or been proven impossible.
If it becomes impossible, record the proof and refresh these four lines before
selecting closure or another frontier.

**Final-mile freeze.** When one capability is runtime-proven and one concrete
execution remains whose success yields a candidate or decisive rejection, do
that edge next. Runtime-proven requires an observed target-runtime receipt, not
an inference from a local model or a control-plane success. The remaining
execution must be named as the next bounded action. Further discovery, new
children, extra research, new wrappers, re-implementations of the same bridge
in another tool or language, and relabeled pivots earn zero progress credit.
Resume discovery only after the edge yields its candidate, decisive rejection,
or proof of impossibility and the frontier is refreshed.

When native CTF controls are active, every decision-changing intervention is a
four-phase transaction:

1. **Prepare** — declare stable family, current representation, semantic
   subject, and machine predicate. Do not include an evidence ID: result
   evidence does not exist yet.
2. **Execute** — run exactly one native call only after prepare is accepted.
3. **Settle** — use only the exact harness-minted receipt from that execution.
   Never invent a future `tool-result-*` identity.
4. **Decide** — retain or discard the evidence, update family or
   representation state, request review, or begin closure before another
   decision-changing intervention.

An authority rejection is a state-repair request, not a reason to resume broad
exploration. Follow a safe machine `requiredAction` exactly once:

- `retry_without_future_evidence`: repeat prepare without any result receipt;
- `retry_with_documented_schema`: rebuild only the rejected request from the
  active tool schema;
- `settle_child_disposition`: complete the child sequence above;
- `material_pivot_or_review`: register a genuinely different representation
  or activate review when its preconditions hold;
- `call_ctf_attempt_status`: refresh canonical state, then repair only the
  rejected phase.

Control-plane failures and semantic no-information are disjoint. A rejection
before the target call executes changes no family fingerprint, representation,
candidate, or no-information count. Preserve its exact code and blocker, then
use this bounded recovery loop:

1. read the blocker and its machine-supplied next action;
2. execute only that repair once, without rerunning the target call;
3. if the same blocker repeats unchanged, preserve the pending receipt or
   resource identity and refresh status once instead of opening another lane;
4. classify semantic progress only after the target call actually executed and
   its exact receipt was settled.

Do not infer hidden validator facts from a generic rejection.

**One-repair rule.** A control-plane rejection permits exactly one repair using
the returned recovery action. The repair may address only the rejected phase
and must not rerun the target call. Otherwise leave the control lane and continue
only with an orthogonal target-semantic experiment or closure steps. Renaming
families or representations, repackaging the same command through another tool
or child, and repeating unchanged status reads are not progress. Settle the
repair's exact receipt and classify it; a second control repair is forbidden
even when status remains stale.

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
tool, engine, prompt, parameter, implementation, intervention ID, or predicate
label does not reset the count. If the harness returns
`material_pivot_or_review`, do not rename and retry the same lane.

At the second no-information result, publish one soft warning before another
ordinary action:

```text
same semantic family and repetition count:
new capability/candidate/bound: none
unused observed source surfaces:
cheapest material alternative:
```

The warning never blocks read-only work or a genuinely changed experiment.
Hard refusal remains reserved for narrow authority, duplicate external-write,
terminal, and lifecycle invariants.

Treat solver `unknown`, timeout, interruption, and backend error as the same
no-information outcome when semantic subject, unresolved variables, and
observable predicate are unchanged. Changing solver, backend, or parameters
alone is not a pivot. Do not credit an equivalent timeout as progress unless it
produces a new candidate, contradiction, bound, or newly visible property.

Give every solver invocation a hard wall-clock abort declared up front. When an
abort fires, the default conclusion is that the constraint model misencodes the
target's semantics, not that the search needs more resources: re-derive the
model from primitive behavior before scaling compute. Re-running the same model
in more engines, wider budgets, or staged searches does not satisfy the pivot.
Unless trusted target evidence or the user declares a different bound, use 180
seconds as the default abort for a solver that produces no useful candidate,
contradiction, bound, or newly visible property. Reaching that default is one
no-information outcome, never evidence that the family is false or that more
compute is the next authority edge.

## 6a) Bounded external review escalation

Activate a separately installed external review skill only when all four hold:
two completed no-information rounds share one fingerprint, no justified
discriminator remains pending, no viable material representation pivot remains,
and no prior review proposal remains untested. Difficulty, slowness, or an
inconclusive round alone is not a precondition. If any precondition fails,
continue the cheapest local discriminator instead.

| Not a semantic no-information round | Semantic no-information round |
|---|---|
| mediator/preflight/schema rejection | target executed and predicate observed no distinction |
| missing path/directory failure | solver returned the same-fingerprint `unknown` twice |
| timeout before target execution | |
| output-visibility failure | |

Immediately before requesting review, quote both rounds' exact receipts and the
identical fingerprint. The quoted receipts must show target execution and the
same semantic predicate; cite the fingerprint beside each receipt. A review
request without those quotations and the matching fingerprint is premature. Do
not count either column's left-hand failures toward review eligibility.

When an authoritative budget exists, after one completed no-information deep
round protect a provenance-backed lower-bound floor for one review lifecycle,
root replay, and authoritative acceptance before funding an unrestricted second
deep round on the same fingerprint. Cap that second round to the declared
remainder above the floor while leaving a cheaper bounded discriminator
eligible. A lower bound proves only that an action which would cross the floor
knowingly makes the downstream path impossible; it does not prove the review
path affordable, so use a credible upper bound when one is available. This
reservation keeps review activation `withheld` until every activation
precondition holds and never authorizes packet preparation, approval, or
transmission. Without authoritative budget authority, do not synthesize a
review reserve or use it to stop; the review preconditions still govern.

Once two same-fingerprint no-information rounds and all four activation
conditions hold, settle and disposition every relevant child, then make
`ctf-review` activation the mandatory next action before another equivalent
worker or intervention. Preserve the protected budget for advisory conversion,
root replay, and authoritative acceptance.

When the canonical control surface requires external review after those
preconditions hold, activate `ctf-review` to verify the external environment
and prepare one exact immutable packet. Do not run another equivalent
intervention first.

When the active runtime exposes `ctf_review_check_env`, invoke that typed tool
directly for the initial environment check. Do not route the packaged bridge's
`--check-env` through bash, eval, or a reconstructed shell command.

External-write authority has exactly two explicit modes. If the current
conversation contains a user instruction to automatically submit bounded
immutable `ctf-review` packets and retrieve their responses without a
per-packet pause, treat it as standing authority only for that named review
workflow. After packing, verify and record the exact manifest scope, bind that
authority to the manifest by creating its one-shot approval receipt, then
submit it exactly once without stopping for another approval question.
Treat scope recording and authority binding as decisions in the same control
step; the next executable action is creation of the exact approval receipt, not
a separate abstract binding action.
Otherwise, present the exact packet and wait for explicit packet-specific user
approval before creating the receipt. Never submit without the manifest-bound
receipt, reuse one receipt or packet, broaden standing authority to another
external write, or infer standing authority from task authorization, package
installation, browser login, configuration, prior review use, or the fact that
review would be helpful.

Activation delegates the complete bounded packet lifecycle to the review skill.
A required authentication handoff is not external-write authority, and
packet-specific approval for a different packet or scope does not transfer.
`ctf-solving` never packs, mutates, or transmits the packet itself; the review
skill owns those actions and their receipts. Preparation or submission is not
an intervention outcome and does not change the no-information count.

A returned review answer is advisory evidence. Convert it into declared
families and discriminators, then replay any candidate through the local oracle
and the real acceptance surface. Review output alone never retires a family,
promotes capability, or populates terminal fields. If the review skill is
unavailable, record that once and make a material pivot rather than repeating
the stalled fingerprint.

Before a non-`solved` terminal transition, record one compact frontier audit.
For discovery, representation pivot, active/reserve discrimination, and
acceptance closure, name the cheapest supported action or `none`, its
prerequisites, cost evidence, expected decision change, and authoritative
budget accounting only when such a budget exists. `none` must cover the current
artifact and every supported candidate. Any action affordable under an
authoritative budget keeps the attempt live: select and schedule that action
before proposing closure. Without one, do not describe an unbounded action as
budget-affordable or budget-exhausted.

## 7) Results and terminations

**No-prose-before-state.** Do not emit closure language such as `done`, `final`,
or `I will stop` until candidate, terminal, child-disposition, or cleanup state
has actually changed through tool actions. A planned transition, prose-only
receipt, or claimed intention does not satisfy this gate. Describe the changed
state only after the action receipt is retained in canonical state. Tool actions
must precede both closure wording and the terminal proposal.

Use one result and one termination.

- Results: `solved`, `failed-with-valid-oracle`, `partial`, or `no-result`.
- Terminations: `completed`, `blocked`, `interrupted`, or `budget-stop`.
  `budget-stop` requires exhausted, reconciled authoritative budget accounting;
  controller limits and absent budget authority never authorize it.
- Legal pairs: `solved` only with `completed`;
  `failed-with-valid-oracle` with `completed` or `budget-stop`; `partial` or
  `no-result` with any termination.

Record result attribution separately as `independent` or `assisted`. For each
material user or external contribution, preserve its source and classify it as
a mechanism, exploit chain, solver, candidate, endpoint, rejection,
prioritization, or cancellation. A supplied mechanism, exploit chain, solver,
or candidate keeps the downstream result assisted unless a sealed replay
rederives it from pre-contribution evidence. Endpoint, rejection,
prioritization, or cancellation alone does not make a result assisted.

While live, result, termination, terminal event, validator response, and closure
remain null. First settle every attempt-owned native resource and retain a
complete cleanup receipt. Only then may one atomic transition populate and
freeze the terminal fields.

- `solved` requires authoritative acceptance and a clean replayable mechanism
  when feasible; for a one-shot or non-rehostable surface, retain the exact
  pinned invocation and acceptance receipt instead.
- `failed-with-valid-oracle` requires a valid oracle and bounded rejection
  evidence covering every remaining candidate.
- `partial` requires a target-relevant proven fact that changes capability,
  prerequisite coverage, a candidate, contradiction, bound, or next decision,
  plus explicit absence of acceptance.
- `no-result` records why no useful fact was proven.

Latch a reproducible exact candidate immediately. Once a root-owned verifier
emits a candidate matching the public result format and a second run reproduces
it, stop diagnostics, refactoring, optimization, and further delegation.
Durably publish the candidate, register and execute the terminal replay,
exercise the real acceptance surface, and submit the explicit terminal
proposal. Local replay alone still cannot authorize `solved`.

Every terminal record names artifact/environment identity, terminal event,
validator response, closure evidence, and for a non-solved result its frontier
audit or genuine external-interruption exception. Authoritative acceptance
remains retained evidence while cleanup is incomplete; retry or explicitly
settle cleanup before freezing the attempt.

## 8) Domain routing

- **Crypto** — algebra, entropy, nonce/key reuse, oracle behavior, then bounded
  solving.
- **Forensics** — preserve originals; inspect metadata, structure, carving, and
  timeline before interpretation.
- **Pwn** — establish mitigations, crash control, primitive, then require one
  integration receipt before crediting local RCE: exact challenge wrapper,
  debugger-free execution, no `/proc` or hidden local addresses, a fresh
  process, and the same solver emitting a flag-shaped result. Measure the
  authoritative process lifetime and compare it with round-trip cost before
  remote execution; then use the unchanged solver for remote acceptance.
- **Reverse engineering** — map input to decision or state transition; distinguish
  static facts from runtime facts.
  - Use Ghidra only headlessly (`analyzeHeadless` or pyghidra headless); never launch, wait on, drive, or use the headed Ghidra GUI, and fall back to IDA Python API xref queries when headless Ghidra cannot provide required cross-references.
- **Web** — map source, routing, auth, parser, and session boundaries; preserve
  exact requests and responses.
- **Misc** — infer the governing state machine from observed behavior and test
  the smallest separator.

Domain-specific missing tools block only when no acquisition, reconstruction,
emulation, static-analysis, or authoritative path can derive the needed fact.

## 9) State form

Maintain one compact canonical attempt containing target and authorization,
artifact/environment identity, capabilities, active/reserve/retired families,
unknowns, optional authoritative budget state, evidence references, at most one
next bounded intervention, nullable in-flight identity, and terminal fields. A
budget key appears only for a trusted user, organizer, or target declaration.

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
