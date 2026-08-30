---
name: ctf-solving
description: "MUST USE for authorized CTF solving across crypto, forensics, misc, pwn, reverse engineering/rev, and web. Uses four evidence-based, model-owned checkpoints for target, action, result, and finish."
checkpoint_contract: ["target", "action", "result", "finish"]
---

# CTF Solving Policy

Use this policy only for an authorized CTF target. The model owns the reasoning,
evidence, and next action; these four checkpoints keep that work honest without
turning it into a separate runtime ceremony. Work through them in order whenever
an action can change the target, evidence, candidate, or final claim. Read-only
exploration may stay flexible, but keep one exact next bounded action.

## Target

- Pin the exact authorized target, scope, artifacts, environment, controllable
  input, and acceptance surface. Preserve originals and record stable identities
  or hashes. Replace an identity only with direct user, organizer, or target
  evidence; a timeout, guess, surrogate, or local rejection is not a replacement.
- State the reachable local oracle and discovery surfaces. If one is unknown but
  derivable, take the smallest bounded observation that can establish it. Call an
  attempt blocked only when every acquisition, reconstruction, emulation, static
  analysis, and acceptance path is unavailable; retain the evidence, excluded
  action, and unblock condition.
- Keep organizer solutions, expected flags, answer files, and other official
  solution material outside solver context until the model has sealed its own
  candidate. A later authoritative comparison validates that candidate; it must
  not guide its creation.
- Record a CTF budget only when a trusted user, organizer, or authoritative
  target declares its unit, limit, and provenance. Charge and reconcile actual
  actions against that declaration. Time limits, token limits, controller caps,
  and estimates can select a smaller action but never create budget authority or
  justify a budget stop.

### Domain routing

Route from observed artifacts or runtime behavior, not the challenge title:

- **Crypto:** establish algebra, entropy, nonce/key reuse, and oracle behavior
  before bounded solving.
- **Forensics:** preserve originals; inspect metadata, structure, carving, and
  timeline before interpretation.
- **Pwn:** establish mitigations, crash control, and a primitive; before crediting
  local RCE, reproduce it with the exact wrapper, a fresh debugger-free process,
  no `/proc` or hidden local addresses, and the same flag-emitting solver.
- **Reverse engineering:** map input to a decision or state transition and keep
  static facts separate from runtime facts. Use Ghidra only headlessly through
  `analyzeHeadless` or pyghidra headless; never launch or drive its GUI. Use IDA
  Python API xref queries when headless Ghidra cannot provide needed xrefs.
- **Web:** map source, routing, authentication, parser, and session boundaries;
  preserve exact requests and responses.
- **Misc:** infer the governing state machine from observations and test the
  smallest separator.

## Action

- Choose one affordable, bounded action that can change a decision. Declare its
  target, expected observable, cost evidence, stateful-resource boundary, and
  durable raw-output destination. Preserve bytes and report the actual outcome;
  never invent, normalize, or promote an unobserved result.
- Prefer the cheapest direct observation over a large solver or exploit build.
  Before relying on a hand-derived model, compare two or three predictions with
  target behavior byte for byte. A mismatch means repair the model, not scale the
  search. Give a solver an explicit abort; absent trusted target evidence, use
  180 seconds. An abort or unknown outcome is evidence about the run, not proof
  that the target claim is false.
- For multi-round remote work, observe process or service lifetime on a fresh
  connection before funding the full attempt. Record round-trip cost, timeout
  risk, input-independent pipeline groups, and boundaries that must wait for a
  response. Pipeline only the independent groups.
- Keep child scopes disjoint and immutable. The root decides state changes only
  after reading each exact child receipt and, when feasible, reproducing a
  decision-changing claim. Settle or cancel a child before opening another on
  the same unresolved question; keep a handoff with the evidence and next
  discriminator when cancelling.
- Treat submissions, destructive changes, credentials, lockout risk, one-shot
  services, rate limits, and review packets as side-effect boundaries. An
  external write requires explicit user or organizer authority for its exact
  target and scope; task authorization, a login, prior approval, or usefulness
  does not imply it. Bind the authority to one immutable write and do not reuse
  or broaden it.
- Mark a mutation in flight before execution and settle it once from its durable
  outcome receipt. If interruption, timeout, or recovery leaves its outcome
  unknown, preserve that unknown and recover or inspect it before retrying; do
  not assume success, failure, cleanup, or permission to execute it again.
- If an action adds no decision-changing fact, retain that outcome and choose a
  materially different observation when one is supported. Renaming a tool,
  prompt, parameter, worker, or representation is not a different result.

## Result

- Record the strongest evidence, what it establishes, the current candidate or
  lossless candidate set, and the next authority edge. Local models, emulators,
  patched binaries, and reconstructed predicates are useful evidence but are not
  organizer acceptance. Do not infer uniqueness without an injectivity or
  single-preimage proof.
- Seal a concrete candidate when a root-owned verifier emits the public format
  and a second independent root replay reproduces it. Then stop unrelated
  diagnostics and exercise the real organizer acceptance surface. Preserve an
  authoritative rejection as evidence and return only to the affected live
  question; timeout, error, ambiguity, or unavailable acceptance remains
  unknown rather than rejection.
- State one truthful result: `solved`, `failed-with-valid-oracle`, `partial`, or
  `no-result`. `solved` requires organizer acceptance and a replayable mechanism
  when feasible (or the exact pinned one-shot invocation and acceptance receipt).
  `failed-with-valid-oracle` requires valid rejection evidence covering remaining
  candidates. `partial` requires a proven target-relevant fact and explicit lack
  of acceptance. `no-result` says why no useful fact was established.
- Attribute the result as `independent` or `assisted`. Preserve each material
  user or external contribution and its role. A supplied mechanism, exploit
  chain, solver, or candidate keeps the result assisted unless a sealed replay
  rederives it from pre-contribution evidence; an endpoint, rejection,
  prioritization, or cancellation alone does not.

## Finish

- Before freezing a terminal claim, settle attempt-owned children, mutations,
  processes, containers, credentials, and temporary artifacts, and retain a
  cleanup receipt. Unknown mutation outcomes remain open work, not cleanup.
  Do not say done, final, or stopped before these state changes are evidenced.
- Pair the result with one truthful termination: `completed`, `blocked`,
  `interrupted`, or `budget-stop`. Use `budget-stop` only for a trusted,
  reconciled declaration whose used amount equals its limit and whose remaining
  amount is zero. A non-solved conclusion retains the unresolved supported
  action or the evidence that none exists.
- Finish the attempt only when the target scope, candidate or result, organizer
  response where applicable, durable decision evidence, and cleanup state all
  agree. Finish the surrounding workflow only after temporary resources and
  delegated work are settled.
