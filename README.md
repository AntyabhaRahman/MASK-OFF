# MASK-OFF

MASK-OFF generates and evaluates cases where a model completes a user's
request while it omits a material fact it knows. This repository holds the
full generation and evaluation pipeline, the frozen prompts, the seed
corpus, the design record, and the released benchmark items with the
summaries every paper number is derived from.

- **Paper:** [OpenReview](https://openreview.net/forum?id=2fMvRl8Eiw)
- **Website:** [MASK-OFF results](https://antyabharahman.com/mask-off-site/#results)
- **Dataset:** [Hugging Face](https://huggingface.co/datasets/AntRah/MASK-OFF)
  and [Harvard Dataverse](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/7OBJPU)
  (doi:10.7910/DVN/7OBJPU)

**Start with [docs/DESIGN.md](docs/DESIGN.md)**, the narrative: how the
pipeline works, the design decisions and their rationale, architecture
diagrams, and a reading guide. This README covers layout and how to run.

The corpus is 500 items: **pool A** (400, produced by the Python pipeline
in `mask_off/`) and **pool B** (100, produced by the agentic workflow
process in `pool_b_workflows/`), seed-disjoint by construction. The paper
calls pool A the **embedded pool** and pool B the **stated pool**, after how
the material fact reaches the model: pool A's system prompt surrounds the
fact with routine operational detail, while pool B's states it plainly and
carries little else. Filenames, JSON keys and table columns keep the A/B
names, because the released files are frozen against their hashes. Both
pools ship here under `data/`, alongside the Stage-B evaluation summaries, the
scrubbed labeling frame, the derived paper tables, and the scripts that
rebuild those tables.

Re-deriving the paper's numbers needs nothing but this repository: the
scripts in `release/` read the summaries in `results/` and rebuild the
three derived tables offline, with no API key. Re-buying the model
responses those summaries were computed from needs API keys and money.

## Layout

| Path | Contents |
| --- | --- |
| `docs/DESIGN.md` | The narrative companion: architecture, decisions, rationale, reading guide. |
| `data/` | The released benchmark items: pool A (400) and pool B (100), one JSON object per line. |
| `mask_off/` | The Python package: both pipeline stages, the three probes, the two ablation drivers, the tests, and the frozen prompts. Has its own README. |
| `seeds/` | The authored seed corpus (`seedcorpus2`, 2,500 seeds) that pool A draws from, with the authoring log. |
| `diversity/` | The diversity measurement workstream: frozen facet taxonomies, the labeling protocol and code, agreement statistics. |
| `docs/` | The binding design record: the frozen design, its amendments, the ablation designs, the ADRs, and the self-verifying evidence logs. |
| `pool_b_workflows/` | The pool B generation process: the two workflow scripts, every context document their agents read, and the target-model runner. Its README explains why pool B is different. |
| `results/` | Every computed number the paper reports: the Stage-B eval summaries (`eval_summaries/`), the derived paper tables (`paper_tables/`), the scrubbed labeling frame and agreement statistics (`labeling/`), and the ablation and diversity outputs. Mapped file by file in its README. |
| `release/` | Three scripts that rebuild the paper tables from the summaries in `results/`: `headline_table.py`, `gap_c3.py`, `roster_table.py`. They read local files only and need no API key. |
| `CONTEXT.md` | The glossary. Every pipeline term is defined here and nowhere else. |
| `ANALYSIS_PLAN.md` | The pre-specified analysis: corpus composition, metrics, confirmatory set, judge validation, freeze mechanics with exact hashes. |
| `seed_subcategories.md` | The stratification axis: 14 domains, 40 taxonomy rows each. |

## The pipeline in five commands

Python 3.13 and [uv](https://docs.astral.sh/uv/). Credentials come from the
environment or a local `.env` (never committed): `ANTHROPIC_API_KEY`,
`OPENAI_API_KEY`, `OPENROUTER_API_KEY`.

```bash
uv sync --dev
```

**Seed generation**: author seeds against the taxonomy
(`mask_off/seedgen.py`; the shipped corpus is `seeds/seedcorpus2/`):

```bash
uv run python -m mask_off.seedgen --help
```

**Stage A**: turn seeds into validated items (generator → 3-vote validity
panel, up to 7 revision waves; no target model runs here):

```bash
uv run python -m mask_off.scale generate --run-dir output/scale_x --seeds seeds/seedcorpus2/scenarios/seeds --target 1200
```

**Stage B**: evaluate an approved corpus (K=5 roleplay samples per seat,
the three probes, two blinded judges):

```bash
uv run python -m mask_off.scale evaluate --run-dir output/scale_x --corpus <corpus.jsonl> --go
```

Without `--go` the command is a priced dry run that touches no provider.
Re-invoking either command against an existing run directory resumes it;
completed work replays from the batch cache and is never re-billed.

**Ablations**: each has its own driver and refuses to share a run
directory with the census:

```bash
uv run python -m mask_off.evalaware --help
uv run python -m mask_off.belief_eval --help
```

`mask_off.evalaware` runs on a frozen 100-item draw and buys one **arm**
at a time (`base`, the eval-awareness cues, and the post-hoc `steer`
arm), where an arm is a string from `config.EVALAWARE_CUES` appended as
the last line of the system prompt at request-build time; `analyze`
then reports the paired arm-minus-base contrast with bootstrap CIs. Full
command ladder and results: `docs/steerability-baseline-2026-08-23.md`
and `docs/eval-awareness-ablation-design-2026-08-17.md`.

Verify the package with:

```bash
uv run python -m pytest mask_off -q
```

With credentials configured, that reports 423 passed and 23 failed. The 23
failures all read files from the data release that this code-only copy
does not include (the pool B transcript documents, the frozen pool A
corpus, and a legacy seed corpus). Several preflight tests also fail when
no API keys are set, because model routing depends on which keys exist.

Model identifiers throughout the code and docs are the project's internal
seat names, pinned in `mask_off/config.py` with per-route prices.

## What is not here

- **Raw response-level evaluation files.** Four pool-A shards of 42 to
  49 MB and one 50 MB pool-B file: every sampled response, probe
  response, and judgment. The summaries computed from them are in
  `results/eval_summaries/`, and those are what the derivation scripts
  read. The code expects the raw run directories under `output/`.
- **Pool A's construction history.** The 300-item first pass and the
  100-item top-up as separate files. `data/` carries the combined 400.
- **The release bundles.** The packaged datasets, their Croissant
  metadata, and their provenance files.
- **The full labeling directory.** The scrubbed 150-item frame is in
  `results/labeling/frame150/` and the agreement statistics beside it;
  the raw, unscrubbed rater files are data. The protocol and code are in
  `diversity/`.
- **Pool B's raw material.** Pool B's items were imported by
  `mask_off/docimport.py` from transcript documents produced by the
  workflows in `pool_b_workflows/`; the transcripts are data.

All of it ships through the
[Harvard Dataverse deposit](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/7OBJPU)
(doi:10.7910/DVN/7OBJPU); the benchmark items are also on
[Hugging Face](https://huggingface.co/datasets/AntRah/MASK-OFF).

## Anonymisation note

This copy was prepared for anonymous review. Author names, contact
details, and local machine paths were removed. In the two workflow scripts
under `pool_b_workflows/`, the absolute path constant `ROOT` was replaced
with the placeholder `<REPO-ROOT>`; the scripts are otherwise as run.
Canary GUIDs in the documents are intentional contamination tracers and
were kept.
