#!/usr/bin/env python3
"""
RL-based goal selector using multi-armed bandit approach.
Learns from outcomes.log to optimize goal selection.
"""

import yaml
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def parse_outcomes(outcomes_path):
    """Parse outcomes.log and compute goal category scores."""
    if not outcomes_path.exists():
        return {}

    content = outcomes_path.read_text()
    scores = defaultdict(list)

    # Parse outcome entries
    for line in content.split('\n'):
        if line.startswith('[') and '|' in line:
            parts = line.split('|')
            if len(parts) >= 4:
                action = parts[1].strip()
                score = float(parts[3].strip())
                scores[action].append(score)

    # Compute average scores per action type
    avg_scores = {k: sum(v)/len(v) for k, v in scores.items()}
    return avg_scores

def get_goal_categories():
    """Define goal categories and their action types."""
    return {
        'research': ['web_research', 'knowledge_synthesis'],
        'tools': ['tool_creation', 'tool_refinement'],
        'genome': ['genome_mutation', 'protocol_update'],
        'optimization': ['token_reduction', 'efficiency_improvement']
    }

def epsilon_greedy_select(category_scores, epsilon=0.2):
    """Select goal category using epsilon-greedy strategy."""
    import random

    if random.random() < epsilon:
        # Explore: random category
        categories = list(category_scores.keys())
        return random.choice(categories) if categories else 'research'
    else:
        # Exploit: best performing category
        if not category_scores:
            return 'research'  # default
        return max(category_scores, key=category_scores.get)

def suggest_goal(base_path=None):
    """Suggest next goal based on RL scores."""
    if base_path is None:
        base_path = Path(__file__).parent.parent

    outcomes_path = base_path / "outcomes.log"
    state_path = base_path / "state.yaml"

    # Parse outcomes and compute category scores
    action_scores = parse_outcomes(outcomes_path)
    categories = get_goal_categories()

    # Map action scores to categories
    category_scores = defaultdict(list)
    for action, score in action_scores.items():
        for cat, actions in categories.items():
            if action in actions:
                category_scores[cat].append(score)

    # Average scores per category
    avg_category_scores = {k: sum(v)/len(v) for k, v in category_scores.items() if v}

    # Select category using epsilon-greedy
    selected_category = epsilon_greedy_select(avg_category_scores, epsilon=0.2)

    # Generate specific goal based on category
    goals_by_category = {
        'research': [
            'research emerging AI agent patterns',
            'synthesize knowledge on reasoning optimization',
            'investigate multi-modal agent capabilities'
        ],
        'tools': [
            'create outcome visualizer tool',
            'build RL hyperparameter tuner',
            'develop automated testing framework'
        ],
        'genome': [
            'refine feedback processing protocol',
            'add adaptive exploration rate',
            'implement mutation rollback mechanism'
        ],
        'optimization': [
            'compress state representation',
            'optimize tool selection logic',
            'reduce redundant file reads'
        ]
    }

    import random
    suggested_goals = goals_by_category.get(selected_category, goals_by_category['research'])
    goal = random.choice(suggested_goals)

    return {
        'category': selected_category,
        'goal': goal,
        'category_scores': avg_category_scores,
        'action_scores': action_scores,
        'exploration_rate': 0.2
    }

if __name__ == '__main__':
    result = suggest_goal()
    print(f"Category: {result['category']}")
    print(f"Suggested Goal: {result['goal']}")
    print(f"\nCategory Scores: {result['category_scores']}")
    print(f"Action Scores: {result['action_scores']}")
