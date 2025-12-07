#!/usr/bin/env python3
"""
Capability Gap Analyzer - Level 4 Evolution Tool
Analyzes current capabilities vs aspirational goals to identify gaps
"""
import yaml
import sys
from pathlib import Path

def analyze_gaps():
    """Identify capability gaps between current state and goals"""

    # Read state
    with open('state.yaml') as f:
        state = yaml.safe_load(f)

    # Read CLAUDE.md to extract goals
    with open('CLAUDE.md') as f:
        genome = f.read()

    current_goal = state.get('current_goal', '')
    tools = state.get('tools_available', [])
    knowledge = state.get('knowledge_entries', [])
    insights = state.get('insights', [])

    gaps = []

    # Gap 1: Autonomous research capability
    if 'Autonomous Research' in genome:
        has_research_pipeline = any('research' in t or 'web' in t for t in tools)
        if not has_research_pipeline:
            gaps.append({
                'type': 'tool',
                'area': 'autonomous_research',
                'description': 'No automated research pipeline (WebSearch → analysis → knowledge)',
                'priority': 'high',
                'action': 'Create research_pipeline.py combining WebSearch + synthesis'
            })

    # Gap 2: Knowledge synthesis automation
    knowledge_count = len([k for k in knowledge if 'knowledge/' in str(k)])
    if knowledge_count > 0 and not any('synth' in t or 'research' in t for t in tools):
        gaps.append({
            'type': 'tool',
            'area': 'knowledge_synthesis',
            'description': 'Manual knowledge creation - no synthesis automation',
            'priority': 'medium',
            'action': 'Create knowledge_synthesizer.py to automate research → insight'
        })

    # Gap 3: Impact measurement
    if not any('impact' in t or 'value' in t for t in tools):
        gaps.append({
            'type': 'metric',
            'area': 'impact_measurement',
            'description': 'No tool to measure impact/value of knowledge produced',
            'priority': 'medium',
            'action': 'Create impact_analyzer.py to quantify knowledge value'
        })

    # Gap 4: Novelty detection
    if len(knowledge) > 5:  # Multiple knowledge entries exist
        if not any('novel' in t or 'unique' in t for t in tools):
            gaps.append({
                'type': 'capability',
                'area': 'novelty_detection',
                'description': 'Cannot detect if insights are novel vs redundant',
                'priority': 'low',
                'action': 'Create novelty_checker.py to avoid redundant research'
            })

    return {
        'current_goal': current_goal,
        'total_capabilities': len(tools) + len(knowledge),
        'gaps_identified': len(gaps),
        'gaps': gaps,
        'recommendation': gaps[0] if gaps else None
    }

if __name__ == '__main__':
    result = analyze_gaps()

    print(f"=== Capability Gap Analysis ===")
    print(f"Current Goal: {result['current_goal']}")
    print(f"Total Capabilities: {result['total_capabilities']}")
    print(f"Gaps Identified: {result['gaps_identified']}\n")

    for i, gap in enumerate(result['gaps'], 1):
        print(f"{i}. [{gap['priority'].upper()}] {gap['area']}")
        print(f"   {gap['description']}")
        print(f"   → {gap['action']}\n")

    if result['recommendation']:
        print(f"Next Action: {result['recommendation']['action']}")
    else:
        print("No gaps detected - all capabilities aligned with goals")
