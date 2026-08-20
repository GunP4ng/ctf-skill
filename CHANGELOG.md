# Changelog

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
