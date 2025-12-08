#!/usr/bin/env python3
"""
optimization_suite.py - Unified CLI for self-evolving agent optimization

Combines token_optimizer, prompt_distiller, and tool analysis into single interface.
Vertical: AI Agent Optimization (token efficiency + prompt compression + tool impact)

Usage:
  ./optimization_suite.py analyze           # Full optimization analysis
  ./optimization_suite.py token <file>      # Token usage breakdown
  ./optimization_suite.py compress <file>   # Prompt compression suggestions
  ./optimization_suite.py tools             # Tool impact ranking
  ./optimization_suite.py suggest           # Next optimization action
"""

import sys
import os
import yaml
import subprocess
from pathlib import Path

EVOME = Path(__file__).parent.parent

def token_analysis(file_path=None):
    """Run token optimization analysis"""
    if file_path:
        cmd = f"python3 {EVOME}/tools/token_optimizer.py {file_path}"
    else:
        cmd = f"python3 {EVOME}/tools/token_optimizer.py"
    subprocess.run(cmd, shell=True)

def compress_prompt(file_path):
    """Run prompt distillation"""
    cmd = f"python3 {EVOME}/tools/prompt_distiller.py {file_path}"
    subprocess.run(cmd, shell=True)

def tool_impact():
    """Analyze tool effectiveness from outcomes"""
    outcomes = []
    if os.path.exists(f"{EVOME}/outcomes.log"):
        with open(f"{EVOME}/outcomes.log") as f:
            for line in f:
                parts = line.strip().split(' | ')
                if len(parts) >= 5:
                    outcomes.append({
                        'action': parts[1],
                        'score': float(parts[3]),
                        'desc': parts[4] if len(parts) > 4 else ''
                    })

    # Count tool mentions
    tool_scores = {}
    for o in outcomes:
        desc = o['desc'].lower()
        for tool in ['token_optimizer', 'prompt_distiller', 'gap_analyzer',
                     'research_pipeline', 'impact_analyzer', 'rl_goal_selector',
                     'outcome_visualizer', 'auto_repair', 'tool_composer']:
            if tool in desc:
                if tool not in tool_scores:
                    tool_scores[tool] = []
                tool_scores[tool].append(o['score'])

    print("\n=== Tool Impact Rankings ===")
    ranked = sorted(tool_scores.items(),
                   key=lambda x: (sum(x[1])/len(x[1]), len(x[1])),
                   reverse=True)
    for tool, scores in ranked:
        avg = sum(scores)/len(scores)
        print(f"{tool:20s} | avg={avg:.2f} uses={len(scores)}")

def full_analysis():
    """Complete optimization analysis"""
    print("=== Ω Optimization Suite ===\n")

    # Token analysis on state
    print("--- Token Analysis (state.yaml) ---")
    token_analysis(f"{EVOME}/state.yaml")

    print("\n--- Tool Impact ---")
    tool_impact()

    # Read current metrics
    if os.path.exists(f"{EVOME}/metrics.yaml"):
        with open(f"{EVOME}/metrics.yaml") as f:
            metrics = yaml.safe_load(f)
            tokens = metrics['performance'].get('avg_tokens_per_cycle', 0)
            print(f"\nCurrent avg: {tokens} tokens/cycle")
            print(f"Target: <1000 tokens/cycle")
            if tokens > 1000:
                print(f"GAP: {tokens - 1000} tokens to target")

def suggest_optimization():
    """Suggest next optimization action based on metrics"""
    with open(f"{EVOME}/metrics.yaml") as f:
        metrics = yaml.safe_load(f)

    tokens = metrics['performance'].get('avg_tokens_per_cycle', 2000)

    print("=== Next Optimization Suggestion ===")

    if tokens > 1500:
        print("PRIORITY: Token reduction")
        print("  → Apply token_optimizer.py to evome.sh read operations")
        print("  → Use quick_state.py instead of full state.yaml reads")
    elif tokens > 1000:
        print("PRIORITY: Prompt compression")
        print("  → Run prompt_distiller on CLAUDE.md")
        print("  → Simplify state.yaml structure")
    else:
        print("PRIORITY: Capability expansion")
        print("  → Token budget available for new features")
        print("  → Consider new tool creation or knowledge synthesis")

def main():
    if len(sys.argv) < 2:
        full_analysis()
        return

    cmd = sys.argv[1]

    if cmd == 'analyze':
        full_analysis()
    elif cmd == 'token':
        file_path = sys.argv[2] if len(sys.argv) > 2 else None
        token_analysis(file_path)
    elif cmd == 'compress':
        if len(sys.argv) < 3:
            print("Usage: optimization_suite.py compress <file>")
            return
        compress_prompt(sys.argv[2])
    elif cmd == 'tools':
        tool_impact()
    elif cmd == 'suggest':
        suggest_optimization()
    else:
        print("Unknown command. Use: analyze, token, compress, tools, suggest")

if __name__ == '__main__':
    main()
