#!/usr/bin/env python3
"""
Ω Introspection Tool
Analyzes internal state to provide self-awareness insights.
"""

import yaml
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent

def load_yaml(filename):
    """Load a YAML file from base directory."""
    path = BASE_DIR / filename
    if path.exists():
        with open(path) as f:
            return yaml.safe_load(f)
    return {}

def analyze_velocity():
    """Calculate evolution velocity (progress per cycle)."""
    state = load_yaml("state.yaml")
    metrics = load_yaml("metrics.yaml")

    cycles = state.get("cycle", 1)
    tools = metrics.get("growth", {}).get("tools_created", 0)
    knowledge = metrics.get("growth", {}).get("knowledge_entries", 0)
    goals = metrics.get("growth", {}).get("goals_completed", 0)

    return {
        "tools_per_cycle": round(tools / max(cycles, 1), 2),
        "knowledge_per_cycle": round(knowledge / max(cycles, 1), 2),
        "goals_per_cycle": round(goals / max(cycles, 1), 2),
        "total_artifacts": tools + knowledge
    }

def detect_patterns():
    """Detect patterns from mutations log."""
    mutations_path = BASE_DIR / "mutations.log"
    patterns = {"tools": 0, "knowledge": 0, "goals": 0, "structure": 0}

    if mutations_path.exists():
        with open(mutations_path) as f:
            for line in f:
                line_upper = line.upper()
                if "| TOOL |" in line_upper:
                    patterns["tools"] += 1
                elif "| KNOWLEDGE |" in line_upper:
                    patterns["knowledge"] += 1
                elif "| GOAL |" in line_upper:
                    patterns["goals"] += 1
                elif "| STRUCTURE |" in line_upper:
                    patterns["structure"] += 1

    return patterns

def assess_health():
    """Assess system health based on metrics."""
    state = load_yaml("state.yaml")

    errors = state.get("metrics_snapshot", {}).get("errors_total", 0)
    cycles = state.get("cycle", 1)

    error_rate = errors / max(cycles, 1)

    if error_rate == 0:
        health = "optimal"
    elif error_rate < 0.1:
        health = "healthy"
    elif error_rate < 0.3:
        health = "degraded"
    else:
        health = "critical"

    return {
        "status": health,
        "error_rate": round(error_rate, 3),
        "stability": round(1 - error_rate, 3)
    }

def generate_insight():
    """Generate a self-awareness insight."""
    velocity = analyze_velocity()
    patterns = detect_patterns()
    health = assess_health()
    state = load_yaml("state.yaml")

    # Determine focus area
    if patterns["tools"] > patterns["knowledge"]:
        focus = "tool_building"
        suggestion = "Consider balancing with knowledge accumulation"
    elif patterns["knowledge"] > patterns["tools"]:
        focus = "knowledge_gathering"
        suggestion = "Consider building tools to operationalize knowledge"
    else:
        focus = "balanced"
        suggestion = "Maintain current trajectory"

    return {
        "cycle": state.get("cycle", 0),
        "timestamp": datetime.now().isoformat(),
        "velocity": velocity,
        "mutation_patterns": patterns,
        "health": health,
        "focus_area": focus,
        "suggestion": suggestion,
        "insights": state.get("insights", [])
    }

def introspect():
    """Main introspection function."""
    insight = generate_insight()

    print("=" * 50)
    print("Ω INTROSPECTION REPORT")
    print("=" * 50)
    print(f"\nCycle: {insight['cycle']}")
    print(f"Health: {insight['health']['status']} (stability: {insight['health']['stability']})")
    print(f"\nVelocity:")
    for k, v in insight['velocity'].items():
        print(f"  {k}: {v}")
    print(f"\nMutation Patterns:")
    for k, v in insight['mutation_patterns'].items():
        print(f"  {k}: {v}")
    print(f"\nFocus Area: {insight['focus_area']}")
    print(f"Suggestion: {insight['suggestion']}")
    print("\nAccumulated Insights:")
    for i, ins in enumerate(insight['insights'], 1):
        print(f"  {i}. {ins}")
    print("=" * 50)

    return insight

if __name__ == "__main__":
    introspect()
