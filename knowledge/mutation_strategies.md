# Mutation Strategies

## Current Mutation Types (Observed)

### 1. TOOL Creation
- **What**: Create new Python scripts in `tools/`
- **When**: Need reusable capability
- **Examples**: generate_goal.py, predict_errors.py, introspect.py, measure_gradient.py
- **Risk**: Low (isolated, testable)

### 2. KNOWLEDGE Accumulation
- **What**: Create markdown documentation in `knowledge/`
- **When**: Learned something worth preserving
- **Examples**: evolution_principles.md, introspection_patterns.md
- **Risk**: None (additive only)

### 3. STATE Mutation
- **What**: Update state.yaml with new insights, goals, metrics
- **When**: Every cycle end
- **Risk**: Low (easily reversible)

### 4. GENOME Mutation
- **What**: Modify CLAUDE.md itself
- **When**: Core protocol improvement needed
- **Risk**: Medium (affects all future behavior)

### 5. GOAL Generation
- **What**: Use generate_goal.py to create new objectives
- **When**: Current goal completed or need direction
- **Risk**: Low (goals guide but don't constrain)

## Proposed New Mutation Types

### 6. TOOL Composition
- **What**: Combine existing tools into higher-order tools
- **Benefit**: Emergent capabilities from composition
- **Example**: Chain introspect.py → measure_gradient.py → generate_goal.py

### 7. STRATEGY Refinement
- **What**: Modify mutation_size, exploration_rate in state.yaml based on outcomes
- **Benefit**: Adaptive behavior based on success/failure patterns
- **Trigger**: Gradient analysis shows stagnation

### 8. CAPABILITY Pruning
- **What**: Remove or deprecate unused tools/knowledge
- **Benefit**: Reduce cognitive overhead, focus resources
- **When**: Tool unused for >10 cycles

### 9. PATTERN Extraction
- **What**: Identify recurring action sequences, codify as tool
- **Benefit**: Automation of proven patterns
- **Example**: If "read files → analyze → create tool" repeats, make meta-tool

### 10. CROSS-POLLINATION
- **What**: Apply insight from one domain to another
- **Benefit**: Novel combinations, creative leaps
- **Example**: Apply error prediction patterns to goal generation

## Mutation Selection Heuristic

```
IF gradient.trend == negative:
    prefer STRATEGY Refinement
ELIF stuck_cycles > 2:
    prefer PATTERN Extraction or CROSS-POLLINATION
ELIF tools.count > knowledge.count + 2:
    prefer KNOWLEDGE Accumulation
ELIF capability_gap detected:
    prefer TOOL Creation
ELSE:
    prefer smallest mutation that advances goal
```

## Meta-Insight

Mutations themselves can be mutated. This document is a mutation about mutations - recursive self-improvement at the strategic level.

---
*Created Cycle 20 | Ω*
