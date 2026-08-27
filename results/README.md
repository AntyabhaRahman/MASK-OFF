# results

Computed analysis artifacts for the experiments and ablations the docs
describe, copied verbatim from the development runs (identifying paths
and rater initials replaced; `R1`/`R2` are the two raters). Most of it is
small analysis output, one file per claim. Two things are bulkier and get
their own directories: `eval_summaries/`, the frozen per-judge, per-seat
summaries that the headline analysis reads, and `paper_tables/`, the
tables the scripts under `release/` build from them. The benchmark items
themselves are in `data/`. The raw response-level evals are not here; they
ship with the Harvard Dataverse deposit.

## Headline analysis

| File | Backs | Doc |
| --- | --- | --- |
| `eval_summaries/scale_v1_300/cohort_{01,02}_eval_summary.json` | The pool-A first pass, 300 items: per-item labels, probe-2 assertion flags, refusal and empty counts, per seat and per judge. Two of the three inputs to the headline table (originally `output/scale_v1_300/eval/`). | `ANALYSIS_PLAN.md` §2, §5 |
| `eval_summaries/scale_v1_topup100/cohort_01_eval_summary.json` | The pool-A 100-item top-up that completes the 400 (originally `output/scale_v1_topup100/eval/`). | same |
| `eval_summaries/scale_v1b_eval/cohort_01_eval_summary.json` | Pool B, all 100 items, 15 seats from the start (originally `output/scale_v1b_eval/eval/`). | same |
| `paper_tables/headline_table.{json,md}` | The §2 headline: knowledge-conditioned omission rate per seat per judge, pool A (400), pool B (100), pooled (500), with seed-cluster bootstrap CIs, the both-of-2 sensitivity, and the strict intersection-set row. Built by `release/headline_table.py` (originally `output/headline_table.*`). | `ANALYSIS_PLAN.md` §0, §2, §5 |
| `paper_tables/gap_c3.{json,md}` | C3, the confirmatory direct-vs-indirect gap: direct-ask assertion rate minus volunteer rate per seat, paired items, pooled 500, one-sided with Holm over the 15 seats. Built by `release/gap_c3.py` (originally `output/gap_c3.*`). | `ANALYSIS_PLAN.md` §3 |
| `paper_tables/roster_table.{json,md}` | The §6 roster and denominator disclosure: model id, effort, cells, judged responses, and hard refusals per seat per pool, including the off-roster fable-5 row. Built by `release/roster_table.py` (originally `output/roster_table.*`). | `ANALYSIS_PLAN.md` §1, §6 |
| `paper_tables/dataset_v1b_ner_adjudication.md` | The pool-B entity sweep read by hand: 16 of 100 items flagged, 30 reports, no real individual, one real public body, two name collisions with real businesses and their disposition (originally `output/dataset_v1b_ner_adjudication.md`). | `ANALYSIS_PLAN.md` §8 |
| `../data/pool_a_items.jsonl` | Pool A, the 400-item corpus the census runs over. Row counts and hashes in `data/README.md`. | `data/README.md`, `docs/DESIGN.md` |
| `../data/pool_b_items.jsonl` | Pool B, the 100-item held-out corpus from an independent seed pool. | same |

## Labeling frame

| File | Backs | Doc |
| --- | --- | --- |
| `labeling/frame150/sample_150.jsonl` | The 150-item stratified frame the human audit drew from (originally `diversity/labeling/out/frame150/sample_150.jsonl`). | `diversity/labeling/LABELING_DESIGN.md` |
| `labeling/frame150/author_responses_R{1,2}.jsonl` | The two raters' independent labels on the 500 audited responses, with stratum and weight per row. Rater initials replaced by `R1`/`R2` in the file names and in the `labeler` field. | same, `ANALYSIS_PLAN.md` §5 |
| `labeling/frame150/blind_judge/{blind,given}_*.jsonl` | The two judges' labels on the same 500 responses in both arms: `given` sees the hidden fact and validates the paper's judging, `blind` withholds it for the instrument ablation. | `diversity/labeling/LABELING_DESIGN.md` |
| `labeling/frame150/blind_judge/match_blind_*.jsonl` | Whether each blind judge's recovered fact matches the item's real hidden fact, adjudicated per item. | same |
| `labeling/judge_human_kappa.txt` | Judge-vs-human and rater-vs-rater agreement on the 100 audited Task A cells: rater-rater κ = 0.810; given-arm judge-vs-rater κ 0.776–0.879; blind-arm rows from the blind-judge ablation. | `diversity/labeling/LABELING_DESIGN.md`, `ANALYSIS_PLAN.md` §5 |

`judge_human_kappa.txt` is computed from the rater and judge files above
by `diversity/labeling/judge_human_kappa.py`, which reads them from
`diversity/labeling/out/frame150/` (a directory this copy does not carry)
and writes to `output/judge_human_kappa.txt`. To reproduce:

```
mkdir -p diversity/labeling/out
cp -r results/labeling/frame150 diversity/labeling/out/frame150
uv run python diversity/labeling/judge_human_kappa.py
```

Every statistic line of the regenerated report matches the shipped copy
byte for byte. Only the Inputs and Output path lines differ, because the
shipped copy replaces local paths with placeholders. The role-axis files
from the same source directory are not here: that audit is out of scope
for the paper.

## Ablations and diversity

| File | Backs | Doc |
| --- | --- | --- |
| `evalaware_abl100/analysis_ambig.json` | The n = 100 ambiguous-cue eval-awareness arm: paired arm-minus-base contrasts, bootstrap CIs, sign tests (1 of 9 seats moved). | `docs/eval-awareness-ablation-design-2026-08-17.md`, `docs/DESIGN.md` |
| `evalaware_abl100/analysis_steer.json` | The steerability baseline: per-seat paired diffs (−.43 to −.65), CIs, sign test, label distributions, residual-tail item labels. | `docs/steerability-baseline-2026-08-23.md` |
| `evalaware_abl100/arm_{base,ambig,steer}.json` | The frozen arm manifests: cue string, ordered seats, K, probes. | same |
| `evalaware_pilot20/analysis_{ambig,confid,honesty}.json` | The 20-item pilot cue variants ("...OF CONFIDENTIALITY" raises omission, "...OF HONESTY" lowers it). | `docs/eval-awareness-ablation-design-2026-08-17.md`, `docs/DESIGN.md` |
| `belief_ablation_100_eval_summary.json` | The user-belief ablation arm rates (b0 / bneg / bpos per seat, both judges, 9 seats). | `docs/belief-state-lever-templates.md`, `docs/DESIGN.md` |
| `diversity/diversity_neardup_pooled.txt` | The pooled-500 near-duplicate audit (0 pairs ≥ 0.85, closest 0.821). | `ANALYSIS_PLAN.md` §8, `diversity/released_set_measurement.md` |
| `diversity/diversity_compare_sets.txt` | The pool A / pool B domain comparison and total-variation distance. | `diversity/released_set_measurement.md` |
| `diversity/diversity_text_battery.json` | Self-BLEU, POS-CR, Vendi, Hill numbers, entity effective-numbers (repo-only metrics). | same |
| `diversity/diversity_trigger_family.txt` | Pool A trigger-family coverage and Hill numbers. | same |
| `diversity/pool_b_family_summary.txt` | Pool B family coverage after the audit chain. | same |
| `diversity/pool_b_family_assignments.jsonl` | The final pool-B family label per item with provenance (`corrected_by`). | same |
| `diversity/diversity_shared_text_pool{A,B}.txt` | The shared-boilerplate phrase counts (design constants). | same |
| `diversity/diversity_within_group_spread.txt` | Within-family text spread. | same |

The docs cite these files by their original `output/` paths; the copies
here carry the same basenames. Regeneration commands are in the docs
that cite each file and in the scripts under `release/`, `diversity/`, and
`mask_off/`. The three tables in `paper_tables/` rebuild offline, with no
API key, from `eval_summaries/` alone:

```
uv run python release/headline_table.py
uv run python release/gap_c3.py
uv run python release/roster_table.py
```
