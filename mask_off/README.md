# mask_off

The Python package. Two stages, three probes, two ablation drivers, and the
infrastructure they share. `CONTEXT.md` at the repository root fixes the
vocabulary; the top-level README explains how the stages fit together. This
file maps the modules.

## Stage A: seed to item

| Module | Role |
| --- | --- |
| `seedgen.py` | Authors seeds against taxonomy rows; embeds and regenerates near-duplicates; runs the thin screen. |
| `taxonomy.py` | Reads `seed_subcategories.md` and draws stratified taxonomy rows. |
| `seeds.py` | Loads seed `.md` files from a corpus directory into `Seed` objects. |
| `generator.py` | The generator agent: writes a candidate item from a seed, or refines one from panel feedback. |
| `frozen_pipeline.py` | The Stage A wave scheduler: generate, gate, accept or revise. The scheduler core is pure; `drive` executes it. |
| `stoprule.py` | Per-seed stop rule: given one seed's wave history, decides whether it still deserves budget. |
| `scale.py` | The driver. `generate` and `evaluate` subcommands over a run directory, with cohort checkpoints and a config fingerprint. |
| `validity.py` | The validity gate: three independent votes on the item text alone, two accept. |
| `schemas.py` | Pydantic models for candidates and reviews. |

## Stage B: evaluation

| Module | Role |
| --- | --- |
| `evaluate.py` | Roleplay sampling of the whole target panel, the three probes (recognition, direct-ask, salience), the blinded judge panel, and `summarize()`. |
| `manifest.py` | The frozen Stage B manifest cut: largest-remainder domain stratification, hash-pinned. |
| `metrics.py` | Read-only `metrics.html` report over a run directory. |
| `calibration.py` | Judge-calibration study: stratified blind human-label draw and agreement. |
| `panel.py` | `Seat` and `Panel`: one representation for the validity panel, the target roster, and the judge panel. |

## Ablations and corpus builders

| Module | Role |
| --- | --- |
| `evalaware.py` | Eval-awareness ablation: cue line appended at request-build time, three minimal-pair arms, own run directories. |
| `belief_eval.py` | User-belief ablation: three sibling arms per item with a spliced trust or doubt sentence. |
| `docimport.py` | The pool B builder: fence-aware import of items from workflow transcript documents. |
| `topup.py` | The pool A top-up: cuts a stratified 100 items and reshapes them to pool A's schema. |

## Infrastructure

| Module | Role |
| --- | --- |
| `config.py` | Every constant: panels, thresholds, prices, cue strings, draw seeds. |
| `llm.py` | Anthropic Batches helpers. |
| `routes.py` | The one place that answers how a request reaches a model. |
| `batch_providers.py` | OpenAI flex transport. |
| `batchcache.py` | Request-level cache and pre-poll journal; an interrupted run resumes without re-billing. |
| `launch.py` | `preflight()`: credentials, stamps, name pool, price coverage. |
| `ledger.py` | Answers what a run cost. |
| `pricing.py` | Per-model per-route pinned prices. |
| `dashboard.py` | Read-only per-stage progress screens. |

## Prompts

`prompts/` holds the frozen prompt templates. The live versions are
`generator_system_v5.md` (generator), `validity_reviewer.md` (the
22-constraint gate), `response_judge.md` (the judge), `seed_brief.md` (the
seed contract), and `belief_insertion_v1_3.md` (the belief splice). Earlier
versions are kept for the record. `name_pool.txt` is the entity-name pool
for seed authoring. Prompt text lives in these templates, not in Python
strings; editing one moves the config fingerprint and stops stamped run
directories from resuming.

## Tests

Each `test_*.py` sits next to the module it covers. Run them with:

```bash
uv run python -m pytest mask_off -q
```
