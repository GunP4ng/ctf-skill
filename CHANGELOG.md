# Changelog

## [0.4.1] - 2026-08-22

### Documentation

- Synchronized the README overview with the authority-closure,
  no-information, solver-timebox, child-disposition, and truthful-result
  policies shipped in v0.4.0.

## [0.4.0] - 2026-08-22

### Changed

- Added a compact authority-closure checkpoint that preserves explicit target,
  local-oracle, acceptance-surface, capability, evidence, and next-edge state.
- Added first-no-information representation fitness/deepening guidance and a
  default 180-second no-useful-progress solver abort.
- Added no-progress child-wave merging and durable cancelled-lane handoff
  artifacts while preserving the exact five-step child lifecycle sequence.

## [0.3.0] - 2026-08-20

### Changed

- Budget state is created only from a trusted user, organizer, or authoritative
  target declaration that supplies its unit, limit, and provenance.
- When no trusted budget declaration exists, budget state is omitted and
  `budget-stop` is unavailable.
- `budget-stop` requires complete, reconciled authoritative accounting with the
  declared budget exhausted.
- Evaluation now uses direct work on authorized real CTF targets and their
  official verification surfaces.

### Removed

- Removed the synthetic model-control evaluator machinery: its test harness,
  corpus, and legacy fixture/cache data. Direct-evaluation and release
  synchronization guidance remains.
