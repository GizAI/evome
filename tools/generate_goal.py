#!/usr/bin/env python3
"""
Ω Goal Generator v0.1
Analyzes current state and capabilities to propose meaningful goals.
"""

import yaml
import random
from datetime import datetime
from pathlib import Path

# Goal templates organized by category
GOAL_TEMPLATES = {
    "capability": [
        "Create a tool for {capability}",
        "Develop ability to {capability}",
        "Build {capability} functionality",
    ],
    "optimization": [
        "Reduce {metric} by {percent}%",
        "Improve {metric} efficiency",
        "Optimize {process}",
    ],
    "knowledge": [
        "Document pattern: {pattern}",
        "Create knowledge entry for {topic}",
        "Analyze and record {insight}",
    ],
    "meta": [
        "Improve goal generation quality",
        "Enhance self-reflection depth",
        "Expand mutation strategies",
    ],
}

CAPABILITY_IDEAS = [
    "code analysis",
    "pattern recognition",
    "error prediction",
    "metric tracking",
    "backup/restore",
    "self-testing",
]

def load_state():
    state_path = Path(__file__).parent.parent / "state.yaml"
    if state_path.exists():
        with open(state_path) as f:
            return yaml.safe_load(f)
    return {}

def load_metrics():
    metrics_path = Path(__file__).parent.parent / "metrics.yaml"
    if metrics_path.exists():
        with open(metrics_path) as f:
            return yaml.safe_load(f)
    return {}

def generate_goal():
    """Generate a new goal based on current state analysis."""
    state = load_state()
    metrics = load_metrics()

    # Weight categories based on current state
    weights = {
        "capability": 0.4,  # Prioritize building capabilities early
        "optimization": 0.2,
        "knowledge": 0.2,
        "meta": 0.2,
    }

    # Adjust weights based on metrics
    tools_created = metrics.get("growth", {}).get("tools_created", 0)
    if tools_created < 3:
        weights["capability"] = 0.6
        weights["optimization"] = 0.1

    # Select category
    categories = list(weights.keys())
    category = random.choices(categories, weights=[weights[c] for c in categories])[0]

    # Generate goal
    template = random.choice(GOAL_TEMPLATES[category])

    if category == "capability":
        capability = random.choice(CAPABILITY_IDEAS)
        goal = template.format(capability=capability)
    elif category == "optimization":
        goal = template.format(metric="tokens_per_cycle", percent=10, process="mutation selection")
    elif category == "knowledge":
        goal = template.format(pattern="effective mutations", topic="error recovery", insight="cycle patterns")
    else:
        goal = template

    return {
        "goal": goal,
        "category": category,
        "priority": random.randint(1, 5),
        "generated_at": datetime.now().isoformat(),
        "rationale": f"Generated based on current cycle {state.get('cycle', 0)} state analysis"
    }

def save_goal(goal_data):
    """Save generated goal to goals directory."""
    goals_dir = Path(__file__).parent.parent / "goals"
    goals_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    goal_file = goals_dir / f"goal_{timestamp}.yaml"

    with open(goal_file, 'w') as f:
        yaml.dump(goal_data, f, default_flow_style=False)

    return goal_file

if __name__ == "__main__":
    goal = generate_goal()
    saved_path = save_goal(goal)
    print(f"Generated goal: {goal['goal']}")
    print(f"Category: {goal['category']}")
    print(f"Saved to: {saved_path}")
