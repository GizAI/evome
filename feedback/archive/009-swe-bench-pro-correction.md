---
priority: HIGH
created: 2025-12-08
topic: benchmark target correction
---

# Correction: SWE-Bench Pro (Public) is the Real Target

## What is SWE-Bench Pro?

**Official**: https://scale.com/leaderboard/swe_bench_pro_public

- **Total**: 1,865 tasks (41 professional repos)
- **Public Set**: 731 instances (accessible)
- **Commercial Set**: 276 instances
- **Held-out Set**: 858 instances

### Difficulty
- **MUCH HARDER** than SWE-Bench Verified
- Models scoring 70%+ on Verified → only 23% on Pro
- Real-world professional codebases
- GPL-licensed + proprietary code (less contamination)

### Current SOTA (Public Set)
- **Claude Sonnet 4.5**: 43.60% (319/731)
- **Gemini 3 Pro**: 43.30%
- **Claude Sonnet 4**: 42.70%
- **GPT-5**: 41.78%

---

## Revised Goal

### Phase 1: SWE-Bench Lite (Warmup)
**Current**: Using Lite (300 issues)
**Target**: 80/300 (26.7%) by Cycle 300
**Purpose**: Learn basics, develop solver

### Phase 2: SWE-Bench Pro Public (Real Goal)
**Target**: 300/731 (41%) by Cycle 1000
**Baseline**: Claude Sonnet 4.5 = 43.6%
**Realistic**: 35-45% range

---

## Why Pro?

1. **Real professional code** (not academic)
2. **Less contamination** (proprietary repos)
3. **Industry standard** (Scale AI endorsed)
4. **Comparable to SOTA** (Claude 4.5 baseline)
5. **Public leaderboard** (external validation)

---

## Updated Milestones

```yaml
phase_1_lite:
  target: 80/300 (26.7%)
  deadline: Cycle 300
  status: in_progress (0/1 currently)

phase_2_pro_public:
  target: 300/731 (41%)
  deadline: Cycle 1000
  baseline: "Claude Sonnet 4.5 = 43.6%"
  unlock: "After Lite 80/300"

phase_3_pro_commercial:
  target: 50/276 (18%)
  note: "Much harder (Claude 4.5 = 17.8%)"
  unlock: "After Public 300/731"
```

---

## Immediate Actions

1. **Keep Lite as warmup** (current plan OK)
2. **After 80/300 Lite**: Switch to Pro Public
3. **Update external_metrics.yaml** to track both:

```yaml
benchmarks:
  swe_bench_lite:
    target: 80/300
    status: warmup

  swe_bench_pro_public:
    target: 300/731 (41%)
    baseline: "Claude 4.5 Sonnet = 43.6%"
    status: locked (unlock at Lite 80)
```

---

## Reality Check

**Lite 80/300 = 26.7%** is good warmup
**Pro 300/731 = 41%** is real challenge (near SOTA!)

If Ω achieves 41% on Pro:
- Competitive with Claude Sonnet 4.5
- Top 5 on public leaderboard
- **Legitimate external validation**

---

*Priority: HIGH - This is the real benchmark*
*Source: https://scale.com/leaderboard/swe_bench_pro_public*
