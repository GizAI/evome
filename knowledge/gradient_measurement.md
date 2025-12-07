# Gradient Measurement: Quantifying Evolution

## Core Concept

Evolution without measurement is wandering. The gradient measures whether we are ascending (improving) or descending (degrading) across cycles.

## Gradient Formula

```
gradient = (capability_delta + goal_progress) / (tokens_spent + errors_incurred + 1)
```

- **Numerator**: What we gained (new tools, knowledge, completed goals)
- **Denominator**: What it cost (resources consumed, mistakes made)

## Interpretation

| Gradient Value | Meaning |
|----------------|---------|
| > 1.0 | Positive evolution - gaining more than spending |
| = 1.0 | Neutral - breaking even |
| < 1.0 | Regression - spending more than gaining |
| < 0.5 | Crisis - consider rollback or exploration mode |

## Usage Patterns

1. **Measure after each cycle** - track trajectory
2. **Compare across spans** - detect long-term trends
3. **Trigger adaptations** - low gradient → change strategy

## Integration with Self-Repair

When gradient drops below stability_threshold (0.7):
- Increase exploration_rate
- Consider reverting recent mutations
- Try orthogonal approaches

## Key Insight

The gradient is not just a number—it is a compass. It tells us which direction leads upward.

---
*Knowledge Entry 004 - Cycle 14*
