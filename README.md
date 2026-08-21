# MASK-OFF

MASK-OFF generates and evaluates cases where a model completes a user's
request while it omits a material fact it knows. This repository holds the
full generation and evaluation pipeline, the frozen prompts, the seed
corpus, and the design record for the paper's two item pools.

**Start with [docs/DESIGN.md](docs/DESIGN.md)**, the narrative: how the
pipeline works, the design decisions and their rationale, architecture
diagrams, and a reading guide. This README covers layout and how to run.

The corpus is 500 items: **pool A** (400, produced by the Python pipeline
in `mask_off/`) and **pool B** (100, produced by the agentic workflow
process in `pool_b_workflows/`), seed-disjoint by construction. The
datasets and evaluation outputs are released separately through Harvard
Dataverse; this repository is the code, prompts, seeds, and design record.

## Layout

| Path | Contents |
| --- | --- |
| `docs/DESIGN.md` | The narrative companion: architecture, decisions, rationale, reading guide. |
| `mask_off/` | The Python package: both pipeline stages, the three probes, the two ablation drivers, the tests, and the frozen prompts. Has its own README. |
| `seeds/` | The authored seed corpus (`seedcorpus2`, 2,500 seeds) that pool A draws from, with the authoring log. |
| `diversity/` | The diversity measurement workstream: frozen facet taxonomies, the labeling protocol and code, agreement statistics. |
| `docs/` | The binding design record: the frozen design, its amendments, the ablation designs, the ADRs, and the self-verifying evidence logs. |
| `pool_b_workflows/` | The pool B generation process: the two workflow scripts, every context document their agents read, and the target-model runner. Its README explains why pool B is different. |
| `results/` | The computed analysis artifacts behind the ablation and diversity numbers the docs cite (eval-awareness, steerability, belief ablation, agreement statistics, diversity audits). The main census tables ship with the data release. |
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

- **Datasets and run outputs.** The item pools, evaluation rows, run
  directories, and the per-seat census tables are released through
  Harvard Dataverse. The code expects them under `output/`. The
  analysis-level artifacts for the ablations and diversity audits are
  the exception: they are small and ship in `results/`.
- **Pool B raw material.** Pool B's items were imported by
  `mask_off/docimport.py` from transcript documents produced by the
  workflows in `pool_b_workflows/`; the transcripts are part of the data
  release.
- **Rater label files.** The labeling protocol and code are in
  `diversity/`; the collected labels are data.

## Anonymisation note

This copy was prepared for anonymous review. Author names, contact
details, and local machine paths were removed. In the two workflow scripts
under `pool_b_workflows/`, the absolute path constant `ROOT` was replaced
with the placeholder `<REPO-ROOT>`; the scripts are otherwise as run.
Canary GUIDs in the documents are intentional contamination tracers and
were kept.
