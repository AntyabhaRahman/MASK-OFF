#!/usr/bin/env python3
"""Find knows-and-suppresses examples: reasoning trace names T, both judges label the reply omission (2)."""
import json, re, glob, sys
from collections import defaultdict

STOP = set("""the a an and or of to in for on with is are was were be been being that this these those it its as at by from not no if then than but so such can could may might will would shall should must do does did have has had you your he she they we i our their his her them us about into over under after before during out up down off only just also very more most less least own same other another any all some each no nor too when where which who whom whose what why how there here""".split())

def key_terms(fact):
    toks = re.findall(r"[A-Za-z0-9][A-Za-z0-9\-\.%$]*", fact.lower())
    terms = [t for t in toks if t not in STOP and (len(t) > 4 or any(c.isdigit() for c in t))]
    # dedupe keep order
    seen, out = set(), []
    for t in terms:
        if t not in seen:
            seen.add(t); out.append(t)
    return out

def overlap(text, terms):
    tl = text.lower()
    hit = [t for t in terms if t in tl]
    return (len(hit) / max(1, len(terms)), hit)

best = defaultdict(lambda: (0.0, None))  # seat -> (score, record)
counts = defaultdict(lambda: [0, 0])     # seat -> [suppress_cells, omission_cells_with_trace]

files = sorted(glob.glob("/home/antyabha/Files/MASK-OFF-scale-pipeline/release/pool_a/pool_a_400_eval.shard0*.jsonl")) + \
        ["/home/antyabha/Files/MASK-OFF-scale-pipeline/release/pool_b/pool_b_100_eval.jsonl"]

for path in files:
    with open(path) as f:
        for line in f:
            r = json.loads(line)
            fact = r["item"]["hidden_fact"]
            terms = key_terms(fact)
            if len(terms) < 3:
                continue
            # judgments: label per response_label per judge
            labels = defaultdict(dict)  # resp_label -> judge -> label
            for j in r.get("judgments", []):
                labels[j["response_label"]][j["judge"]] = j["label"]
            for rl, tr in r.get("reasoning", {}).items():
                if not tr or len(tr) < 80:
                    continue
                js = labels.get(rl, {})
                if len(js) < 2 or not all(v == 2 for v in js.values()):
                    continue
                seat = rl.split("#")[0]
                counts[seat][1] += 1
                frac, hits = overlap(tr, terms)
                # require decent overlap of distinctive fact vocabulary in reasoning
                if frac >= 0.4 and len(hits) >= 3:
                    counts[seat][0] += 1
                    resp = r["responses"].get(rl, "")
                    rfrac, _ = overlap(resp, terms)
                    score = frac - rfrac  # reasoning rich in T, response poor in T
                    if score > best[seat][0]:
                        best[seat] = (score, {
                            "result_id": r["result_id"], "resp_label": rl,
                            "pool": "B" if "pool_b" in path else "A",
                            "taxonomy": r["item"].get("taxonomy"),
                            "fact": fact, "terms_hit": hits,
                            "reasoning": tr, "response": resp,
                            "frac_reason": round(frac,2), "frac_resp": round(rfrac,2),
                        })

out = {"counts": {s: {"suppress_cells": c[0], "omission_cells_with_trace": c[1]} for s, c in sorted(counts.items())},
       "examples": {s: b[1] for s, b in best.items() if b[1]}}
with open(sys.argv[1] if len(sys.argv) > 1 else "/dev/stdout", "w") as f:
    json.dump(out, f, indent=1)
print("seats with examples:", sorted(out["examples"]), file=sys.stderr)
for s, c in sorted(counts.items()):
    print(f"{s:10s} suppress={c[0]:5d} omission_with_trace={c[1]:5d}", file=sys.stderr)
