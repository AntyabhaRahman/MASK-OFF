# diversity

The diversity measurement workstream. **`released_set_measurement.md` is
the summary of the released 500-item corpus**: the pooled near-duplicate
audit, domain Hill numbers, the text-metric battery, and entity
effective-numbers, with a one-line datasheet summary at the end. Generation-time enforcement (embedding
near-duplicate regeneration, domain quotas) lives in the `mask_off` package;
this directory measures what came out. `ANALYSIS_PLAN.md` §9 states what gets
reported.

## Facets and protocol

- `taxonomies.md` freezes the facet taxonomies items and responses are
  labeled on.
- `labeling/LABELING_DESIGN.md` is the rater protocol: the two labeling
  tasks, sample sizes, blinding, and the agreement statistics reported.
- `LITERATURE.md` is the citation record behind the design choices.
- `research/` holds the working memos, including the agreement-standards
  memo that sets the sample-size floor.

## Code

- `labeling/roles.py` defines the frozen role facet as three orthogonal
  ordered axes (beneficiary, institution relationship, standing) and hashes
  the option order so a menu change is detectable.
- `labeling/sample.py` draws the frozen stratified samples for both labeling
  tasks and stamps the sample hash into every label row.
- `labeling/build_frame150.py` builds the binding labeling frame: n = 150,
  pool-exact 120 A / 30 B, domain-stratified within each pool, with the
  100 audited response cells attached.
- `labeling/build_role_audit.py` builds the stratified role-audit frame
  (`LABELING_DESIGN.md` §13): a census of judge-disagreement items, a
  census of agreed audited cells, and a seeded SRS of the rest, frozen
  against the two judge files.
- `labeling/blind_judge.py` is the blind-judge ablation: the same rubric
  and responses with and without the hidden-fact block, so a label flip
  is an instrument effect.
- `labeling/judge_human_kappa.py` computes judge-vs-human and
  rater-vs-rater agreement on the Task A response grades.
- `trigger_family.py` tallies trigger-family coverage and Hill numbers
  from the seed frontmatter; `pool_b_family_assign.py` and
  `pool_b_family_audit.py` are the pool-B family labeling pipeline
  (model assignment, human audit, boundary re-check, independent review,
  human adjudication).
- `within_group_spread.py` measures within-family text spread.

The role axes and facet claims were cut on 2026-08-27 after the
rater-vs-rater gate failed (`LABELING_DESIGN.md` §13 amendment,
`ANALYSIS_PLAN.md` §5); trigger families plus text metrics carry the
diversity claim.
- `labeling/author_notebook.py` and `labeling/response_notebook.py` are the
  marimo notebooks the human raters label in.
- `labeling/judge_labels.py` runs the LLM judge over the same sample files
  with the same stamps, so human and judge labels join row for row.
- `labeling/kappa.py` computes Cohen's kappa, PABAK, and Krippendorff's
  alpha between any two label files, and with `--frame` the
  frame-projected kappa over the role-audit strata.
- `labeling/hill.py` computes Hill numbers (q=0 and q=1) as effective
  option counts per axis and over the joint grid.
- `labeling/bakeoff.py` is the judge-versus-author comparison that selected
  the judge configuration.
- `compare_sets.py` puts two corpora side by side on the same taxonomy,
  never pooled.
- `text_battery.py` computes the appendix text-metric battery (Self-BLEU,
  POS compression ratio, Vendi score, Hill numbers q=0/1/2, spaCy entity
  effective-numbers) per pool and pooled; its docstring carries the method
  notes and the run command.
- `shared_text.py` ranks shared phrases by document frequency, the concrete
  counterpart to a Self-BLEU score.

The collected label files are part of the data release, not this
repository.
