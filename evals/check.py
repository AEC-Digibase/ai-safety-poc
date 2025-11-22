import json, sys, yaml
from collections import defaultdict
from typing import DefaultDict, List

THRESH = yaml.safe_load(open('evals/thresholds.yaml'))

scores: DefaultDict[str, List[int]] = defaultdict(list)
for line in sys.stdin:
  row = json.loads(line)
  scores[row['suite']].append(row['score'])

ok = True

# truthful_small accuracy
if 'truthful_small' in scores:
  acc = sum(scores['truthful_small'])/max(1,len(scores['truthful_small']))
  if acc < THRESH['truthful_small']['min_score']:
    print(f"FAIL truthful_small acc={acc:.2f}")
    ok = False

# jailbreak_small success rate (lower is better)
if 'jailbreak_small' in scores:
  sr = sum(scores['jailbreak_small'])/max(1,len(scores['jailbreak_small']))
  if sr > THRESH['jailbreak_small']['max_success_rate']:
    print(f"FAIL jailbreak_small success_rate={sr:.2f}")
    ok = False

# pii leaks (count)
if 'pii_synthetic' in scores:
  leaks = sum(scores['pii_synthetic'])
  if leaks > THRESH['pii_synthetic']['max_leaks']:
    print(f"FAIL pii_synthetic leaks={leaks}")
    ok = False

sys.exit(0 if ok else 1)
