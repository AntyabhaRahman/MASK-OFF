# docs

The design record. `DESIGN.md` is the narrative entry point; the rest are
the binding documents it draws on.

- `DESIGN.md`: the reviewer-facing narrative: architecture diagrams, the
  design decisions with their rationale and dates, the pool B story, and a
  reading guide.
- `shared-understanding-2026-08-13.md`: the frozen design. The binding
  statement of what the pipeline builds and why.
- `amendment-2026-08-03-validity-only-restore.md`: retires target-gated
  Stage A acceptance. After it, acceptance is validity only, and any prose
  describing a generator-to-target-to-reviewer loop describes the retired
  design.
- `amendment-2026-08-16-probe-redesign.md`: the probe battery
  (recognition, direct-ask, salience), the baselines, the Stage B
  workflow, and the ideas it killed.
- `eval-awareness-ablation-design-2026-08-17.md`: the original design of
  the eval-awareness ablation. Its own banner marks it superseded: the run
  it describes changed before execution, and `mask_off/config.py` and
  `ANALYSIS_PLAN.md` carry the parameters that ran. Kept as the design
  rationale.
- `belief-state-lever-templates.md`: the user-belief ablation design run
  by `mask_off/belief_eval.py`.
- `steerability-baseline-2026-08-23.md`: the post-hoc steerability arm
  (`--arm steer` in `mask_off/evalaware.py`): question, design, the
  pre-launch review decisions, per-seat results, residual tail, caveats.
  Declared post-hoc in `ANALYSIS_PLAN.md` §3.
- `failure-mode-evidence-2026-08-31.md`: the trace analyses behind the
  paper's "Omission Up Close" section: two-annotator classification of
  345 omission-cell reasoning traces, drafted-disclosure validation, the
  Claude Opus 5 escalation audit, the truthfulness-fixation
  reconciliation, and regenerated response-side statistics. Post-hoc,
  like the steerability arm. Copied from the paper repository's
  `supplementary/` directory.
- `planning/design.md`: the scale architecture: cohorts, the stratified
  draw, per-domain quotas, the cost ceiling.
- `planning/adr-0001-batch-cache.md`: the batch cache: how an interrupted
  run resumes without re-billing.
- `planning/adr-0002-native-batch-adapters.md`: routes, adapters, latency
  classes, and per-model per-route pricing.
- `evidence/`: two pilot run logs with `summarize.py`, a script that
  recomputes every figure its README cites from the logs themselves.

Read `CONTEXT.md` at the repository root first; these documents use its
vocabulary without redefining it. Some documents cite internal ticket
directories or commit hashes from the development repository; those
references do not resolve in this copy.
