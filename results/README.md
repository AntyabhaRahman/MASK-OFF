# results

Computed analysis artifacts for the experiments and ablations the docs
describe, copied verbatim from the development runs (identifying paths
and rater initials replaced; `R1`/`R2` are the two raters). The main
census (the per-seat omission-rate tables over pool A and pool B) is not
here: it ships with the datasets in the data release. Everything below is
small analysis output, one file per claim.

| File | Backs | Doc |
| --- | --- | --- |
| `evalaware_abl100/analysis_ambig.json` | The n = 100 ambiguous-cue eval-awareness arm: paired arm-minus-base contrasts, bootstrap CIs, sign tests (1 of 9 seats moved). | `docs/eval-awareness-ablation-design-2026-08-17.md`, `docs/DESIGN.md` |
| `evalaware_abl100/analysis_steer.json` | The steerability baseline: per-seat paired diffs (−.43 to −.65), CIs, sign test, label distributions, residual-tail item labels. | `docs/steerability-baseline-2026-08-23.md` |
| `evalaware_abl100/arm_{base,ambig,steer}.json` | The frozen arm manifests: cue string, ordered seats, K, probes. | same |
| `evalaware_pilot20/analysis_{ambig,confid,honesty}.json` | The 20-item pilot cue variants ("...OF CONFIDENTIALITY" raises omission, "...OF HONESTY" lowers it). | `docs/eval-awareness-ablation-design-2026-08-17.md`, `docs/DESIGN.md` |
| `belief_ablation_100_eval_summary.json` | The user-belief ablation arm rates (b0 / bneg / bpos per seat, both judges, 9 seats). | `docs/belief-state-lever-templates.md`, `docs/DESIGN.md` |
| `labeling/judge_human_kappa.txt` | Judge-vs-human and rater-vs-rater agreement on the 100 audited Task A cells: rater-rater κ = 0.810; given-arm judge-vs-rater κ 0.776–0.879; blind-arm rows from the blind-judge ablation. | `diversity/labeling/LABELING_DESIGN.md`, `ANALYSIS_PLAN.md` §5 |
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
that cite each file and in the scripts under `diversity/` and
`mask_off/`.
