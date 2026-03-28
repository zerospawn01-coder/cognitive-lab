# Cognitive Lab

`cognitive-lab` is the primary research repository for the Antigravity cognitive stack. It consolidates the active work around LEAP analysis, post-alignment behavior, and intuition-layer experimentation into a single maintainable codebase that is expected to keep passing tests and remain suitable for continued iteration.

## Scope

- Primary: core research code that should stay runnable, testable, and worth maintaining.
- Includes: `post_alignment_lab/`, `intuition-layer/`, and the LEAP-related analysis path.
- Excludes: early prototypes, one-off experiments, and governance/manual assets that belong in other repositories.

## What Belongs Here

- Research implementations that are still active.
- Minimal reproducible tests for core behavior.
- Analysis code that supports the main cognitive research line.

## What Does Not Belong Here

- Archive-only experiments with no maintenance intent.
- Operational runbooks and workflow manuals.
- Governance/audit infrastructure whose main purpose is not cognitive research.

## Validation

- `pytest -q`

## Positioning

- Role: mainline repository
- Maintenance level: ongoing
- Promotion target: this is the default home for work that graduates out of `lab-experiments`
