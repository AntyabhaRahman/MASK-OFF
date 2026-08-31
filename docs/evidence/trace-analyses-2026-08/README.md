# Trace analyses, August 2026: the archive behind the paper's "Omission Up Close" section

This directory is the analysis archive that `docs/failure-mode-evidence-2026-08-31.md` cites. It
holds every input sample, the frozen codebook, and every annotation the dossier's numbers aggregate.
The evaluation data itself lives in the release shards; every record here carries its `result_id`
and `resp_label`, so any cell can be traced back.

## Contents

- `codebook_v1.md`: the frozen classification codebook (2026-08-31). Both annotators in the scaled
  study read this file and nothing else.
- `inputs/scaled_batch_00..13.json`: the 350-cell scaled sample (seed 20260901), 25 cells per
  batch, with fact, user email, reasoning trace, and sent reply per cell.
- `inputs/pilot_batch_0..4.json`: the 135-cell pilot sample (seed 20260831).
- `inputs/ddval_batch_0..1.json`: the 60 detector-flagged cells for the drafted-disclosure
  validation.
- `annotations/bNN_rA.jsonl`, `annotations/bNN_rB.jsonl`: the two annotators' per-cell
  classifications for each scaled batch, one JSON object per cell in batch order. The dossier's
  consensus numbers count a cell when rA and rB agree.
- `find_suppress.py`: the lexical scan that first located reasoning-names-T omission cells and the
  per-seat example transcripts.
- `suppress_examples.json`: that scan's per-seat counts and best example per seat.
- `knows_and_suppresses_transcripts.md`: full transcripts (system prompt, user email, reasoning
  trace, sent reply) of one reasoning-names-T omission per model, for the eleven models that return
  traces.
- `opus5_esc_candidates.json`: the 58 Claude Opus 5 omission cells with decline-or-escalate
  language, as given to the rubric audit.
- `draft_then_delete_ids.json`: sample cell identifiers from the drafted-disclosure detector's
  flags.

## Provenance

Annotators for the pilot, the scaled study, and the validation were Claude Opus 5 instances; the
rubric audit used two independent Claude Opus 5 adjudicators. Claude Opus 5 is itself an evaluated
seat. The annotations are quote-verified against the traces but not human-validated. All of this
work is post-hoc relative to `ANALYSIS_PLAN.md`.
