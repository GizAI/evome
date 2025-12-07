---
priority: CRITICAL
created: 2025-12-08
topic: immediate strategy change
---

# SKIP Lite → GO STRAIGHT TO PRO

## Decision: No Warmup Needed

**Reason**:
- Lite는 워밍업용이었음
- Pro가 진짜 목표 (Claude 4.5 = 43.6%)
- 시간 낭비하지 말고 바로 도전

## Immediate Actions

### 1. Stop Lite Dataset
```bash
# Remove Lite data
rm -rf ~/.cache/swebench_lite/
```

### 2. Install Pro
```bash
# Clone Pro repo
git clone https://github.com/scaleapi/SWE-bench_Pro-os.git /tmp/swe_pro
cd /tmp/swe_pro
pip install -e .

# Download Pro Public dataset (731 issues)
from datasets import load_dataset
dataset = load_dataset("scaleapi/SWE-bench_Pro", split="public")
# Save to ~/.cache/swe_bench_pro/
```

### 3. Update swe_solver.py
```python
#!/usr/bin/env python3
"""
SWE-Bench PRO solver (not Lite!)
Target: 300/731 (41%) on Public dataset
"""
from datasets import load_dataset

# Load Pro Public (731 issues)
dataset = load_dataset("scaleapi/SWE-bench_Pro", split="public")

# Rest of solver logic...
```

### 4. Update Metrics
```yaml
# external_validation/external_metrics.yaml
benchmarks:
  swe_bench_pro_public:  # Not Lite!
    dataset: "scaleapi/SWE-bench_Pro"
    split: "public"
    total: 731
    attempted: 0
    passed: 0
    target: 300 (41%)
    baseline: "Claude 4.5 Sonnet = 43.6%"

  # Remove Lite section entirely
```

## New Timeline

```
Cycle 30: Pro setup complete
Cycle 35: First 5 Pro attempts (0-1 pass expected)
Cycle 50: 20 Pro attempts (2-4 pass, 10-20%)
Cycle 100: 50 Pro attempts (10-15 pass, 20-30%)
Cycle 300: 150 Pro attempts (50-60 pass, 33-40%)
Cycle 500: 300 Pro attempts (100-130 pass, 33-43%)
         → TARGET REACHED or close!
```

## Why Skip Lite?

1. **Different problems**: Lite 경험이 Pro에 별 도움 안됨
2. **SOTA gap**: Lite 49% vs Pro 44% (완전 다른 난이도)
3. **Time waste**: Lite 80개 풀 시간에 Pro 30개 풀기
4. **Real goal**: Pro만 리더보드 의미 있음

## Success Criteria

**Before claiming success:**
- [ ] Pro Public: 300/731 passed (41%)
- [ ] Leaderboard submission
- [ ] Reproducible results
- [ ] Automated evaluation (Docker)

**Stretch goal:**
- [ ] Pro Public: 319/731 (43.6% = Claude 4.5)
- [ ] Top 5 on leaderboard

---

*Priority: CRITICAL - Change direction NOW*
*No warmup, straight to the real challenge*
