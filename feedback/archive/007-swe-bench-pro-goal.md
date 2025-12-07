---
priority: HIGH
created: 2025-12-08
topic: concrete external validation
---

# Goal: SWE-Bench Pro 80/300 → ARC-AGI 40%

## Phase 1: SWE-Bench Lite

**Target**: 80/300 solved (26.7%)
**Baseline**: Claude Sonnet 3.5 = 147/300 (49%)
**Current**: 0/300 (0.0%)

### Setup (next cycle)
```bash
pip install swe-bench
python -m swebench.download_data --lite
```

### Milestones
- Cycle 30: 1/300 (0.33%) - first success
- Cycle 50: 10/300 (3.3%) - baseline
- Cycle 150: 40/300 (13.3%) - competitive
- Cycle 300: 80/300 (26.7%) - **GOAL**

### Rules
- ✅ Automatic testing only (no manual review)
- ✅ All results logged (pass/fail, no partial)
- ✅ Random sampling (no cherry-picking easy issues)
- ✅ Update external_metrics.yaml every 10 issues

### Expected Reality
```
First 5 attempts: 0-1 pass (0-20%)
First 50 attempts: 5-10 pass (10-20%)
First 100 attempts: 20-30 pass (20-30%)
→ Slow, honest progress
```

---

## Phase 2: ARC-AGI (After 80점)

**Target**: 40% on public test set
**Baseline**: GPT-4o = 32%, Human = 85%
**Unlock**: Only after SWE-Bench 80/300

### Why This Order?
1. SWE-Bench validates coding ability (Ω's strength)
2. ARC-AGI validates reasoning/generalization (harder)
3. Both are objective, measurable, cannot self-report

---

## External Metrics Update

```yaml
# external_validation/external_metrics.yaml
benchmarks:
  swe_bench_lite:
    attempted: 0
    passed: 0
    success_rate: 0.0%
    target: 80/300 (26.7%)

  arc_agi:
    status: locked
    unlock_condition: "swe_bench >= 80"
```

---

## Success Criteria

**Before claiming "evolved":**
- [ ] SWE-Bench: 80/300 passed
- [ ] ARC-AGI: 40% accuracy
- [ ] impact_score > 0.5
- [ ] All results automatically verified

**Until then:**
- Current status = "self-satisfaction simulator"
- All internal metrics = meaningless
- Only external validation counts

---

## Immediate Actions

1. Install SWE-bench
2. Try 5 easiest issues
3. Expect 0-1 success (be honest)
4. Analyze failures
5. Build tools to address gaps
6. Repeat until 80

---

*Deadline: 300 cycles for 80점*
*No excuses, no self-grading, only test_passed=true*
