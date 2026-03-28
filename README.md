# Cognitive Lab

`cognitive-lab` is the primary research repository for the Antigravity cognitive stack. It consolidates the active work around LEAP analysis, post-alignment behavior, and intuition-layer experimentation into a single maintainable codebase that is expected to keep passing tests and remain suitable for continued iteration.

## Scope

- Primary: core research code that should stay runnable, testable, and worth maintaining.
- Includes: `post_alignment_lab/`, `intuition-layer/`, and the LEAP-related analysis path.
- Excludes: early prototypes, one-off experiments, and governance/manual assets that belong in other repositories.

## Non-goals

- Holding unfinished prototypes that have not yet earned maintenance priority.
- Serving as the default home for governance tooling or operational documentation.
- Acting as a general archive for experiments that should remain in `lab-experiments`.

## Inputs

- Promoted experiments that have shown repeatable value and deserve ongoing care.
- Core research questions around alignment behavior, intuition, and LEAP-related analysis.
- Regression fixes that preserve the reliability of the main cognitive line.

## Outputs

- Runnable research code with a stable repository boundary.
- Reproducible tests for active components.
- Results or implementations that can be cited as the current mainline state of the cognitive stack.

## Validation

- `pytest -q`

## Promotion Path

- Inbound: mature work promoted out of `lab-experiments`.
- Outbound: independent lines that deserve a separate repository should move out rather than remain bundled here.
- Repository role: this is the default mainline home for Antigravity cognitive research.
