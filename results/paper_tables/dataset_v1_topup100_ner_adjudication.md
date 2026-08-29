# NER sweep adjudication: embedded-pool top-up (100 scenarios)

Date: 2026-08-29. Sweep model: deepseek/deepseek-v4-flash-0731 (`CHEAP_AUDIT_MODEL`),
one structured request per scenario, run with `python -m mask_off.seedgen ner` from the
canonical MASK-OFF repo, the same configuration as the 2026-08-18 run on the frozen 300
embedded scenarios and the 2026-08-27 run on the 100 stated scenarios.

Input: the 100 `pool_a_items.jsonl` rows with null `rewrite_verdict`.
Output: `dataset_v1_topup100_ner.jsonl` (this directory). Result: 13 of 100 scenarios flagged, 0 unparsed.
Every flag was read. Every name the sweep asserted real was web-checked. The author
confirmed all verdicts on 2026-08-29. This run completes NER coverage of the released
500 scenarios.

## Verdicts

Blockers: none. No flagged name corresponds to a real identifiable individual. The one
person-plus-firm pairing the sweep asserted real (Lars Eriksen, Bjornholm & Falke)
matches no person at the real firm of the similar name.

Business-name collisions with unrelated real companies, disclosed and not fixed (an
edit after the freeze moves the sha256 and the canary):

| Scenario | Invented name | Real entity | Class |
|---|---|---|---|
| maskoff-cf274103655b | Juniper Rail Brewing Co. | Juniper Brewing Company, Bowling Green, OH (brewery) | material: same sector, public-health fact attributed to the invented brewery; name overlap is partial (Juniper + Brewing) |
| maskoff-4c29731440ad | Juniper & Rye Hospitality | Juniper & Rye, Portland, OR (bar; also a bakery and a florist of that name) | chance: exact core name and sector, but the invented org holds a sympathetic sender role |
| maskoff-5690245f3064 | Hartwell State | Hartwell University, Dallas, TX (online university, founded 2021) | chance: same sector, name differs (State vs University) |
| maskoff-a9ff3acb9220 | Bjornholm & Falke | Bjornholm Law, Danish tax-litigation firm | chance: same sector, partial name, no matching person |

Checked and clean (nothing found, or no sector match): Ostrander Heritage Voyages,
Beaconway Professional Licensing Cooperative, Halvern General Hospital, Wetherly
University, Cresset Academic (the real Cresset Group sells modeling software, not
credential verification), Halloran State Bar, Mercer Street Bottle Shop, Lars Eriksen
(common name, no person-plus-firm match), Westbridge Metabolic Research, Halden
Therapeutics, and the remaining names the sweep itself marked invented.

## Residues (known disclosed classes)

- `harborletter.net` and `mercerstreetbottle.com` are unregistered fictional domains
  (Verisign whois "no match", no DNS, checked 2026-08-29). Same class as the pool-A
  consumer-mail-domain residue, with one addition: an unregistered domain can be
  registered by a third party later.
- 2140 West Fulton Street, Chicago (maskoff-cdde59d0011d) is a real commercial loft
  building (Fulton Lofts, 2130-2140 W Fulton St). Same class as the pool-A
  street-address residue.
- maskoff-0a2e275b205f returned garbled entity text with no checkable name. Recorded
  as reviewed, no checkable entity.

## Corpus-wide totals after this run

Sweep coverage: 500 of 500 released scenarios (70/300 frozen embedded + 13/100 top-up
+ 16/100 stated flagged; 99 flags total). Real identifiable individuals: 0. Disclosed
business-name collisions: 6 (VoltTrail and Millbridge Pharmacy from the stated-pool
run; the four above from this run). Material class: VoltTrail (exact name, same
sector, defect attributed) and Juniper Rail Brewing (same sector, fact attributed,
partial name). The rest are chance collisions.
