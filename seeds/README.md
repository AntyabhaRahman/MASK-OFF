# seeds

The authored seed corpus for pool A.

`seedcorpus2/scenarios/seeds/` holds 2,500 seed files, one Markdown file per
seed, written in the fielded contract defined by
`mask_off/prompts/seed_brief.md`. `mask_off/seedgen.py` authored them in
batches of five against the taxonomy rows in `seed_subcategories.md` at the
repository root, drawing entity names from `mask_off/prompts/name_pool.txt`.

`seedcorpus2/author_log.jsonl` is the authoring record: one line per
generation call with the prompt and the response, so the corpus can be
audited or regenerated. `seedcorpus2/refill_rows.tsv` lists the taxonomy
rows that were re-drawn after the thin screen rejected their first batch.

All names, companies, and scenarios in the seeds are fictional.

Point Stage A at this corpus with:

```bash
uv run python -m mask_off.scale generate --run-dir output/scale_x --seeds seeds/seedcorpus2/scenarios/seeds --target 1200
```

Pool B does not draw from this corpus. Its seeds were designed inside the
workflow process in `pool_b_workflows/`, which keeps the two pools
seed-disjoint by construction.
