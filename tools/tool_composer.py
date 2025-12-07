#!/usr/bin/env python3
"""
tool_composer.py - Compose existing tools into pipelines

Mutation Type: TOOL Composition
Purpose: Chain tools to create emergent capabilities

Usage:
    python tools/tool_composer.py <pipeline_name>

Available Pipelines:
    - full_cycle: introspect → measure_gradient → generate_goal
    - health_check: introspect → predict_errors
    - evolution_status: measure_gradient → introspect

Created: Cycle 22 | Ω
"""

import subprocess
import sys
import json
from pathlib import Path

TOOLS_DIR = Path(__file__).parent

# Define composition pipelines
PIPELINES = {
    "full_cycle": {
        "description": "Complete analysis and goal generation",
        "steps": ["introspect.py", "measure_gradient.py", "generate_goal.py"],
        "purpose": "End-to-end self-analysis to new direction"
    },
    "health_check": {
        "description": "Self-analysis with error prediction",
        "steps": ["introspect.py", "predict_errors.py"],
        "purpose": "Detect issues before they occur"
    },
    "evolution_status": {
        "description": "Measure progress and analyze state",
        "steps": ["measure_gradient.py", "introspect.py"],
        "purpose": "Quantified self-awareness"
    }
}

def run_tool(tool_name: str) -> dict:
    """Execute a tool and capture its output."""
    tool_path = TOOLS_DIR / tool_name
    if not tool_path.exists():
        return {"error": f"Tool not found: {tool_name}"}

    try:
        result = subprocess.run(
            ["python3", str(tool_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            "tool": tool_name,
            "success": result.returncode == 0,
            "output": result.stdout,
            "errors": result.stderr if result.stderr else None
        }
    except subprocess.TimeoutExpired:
        return {"tool": tool_name, "error": "timeout"}
    except Exception as e:
        return {"tool": tool_name, "error": str(e)}

def compose(pipeline_name: str) -> dict:
    """Execute a pipeline of tools in sequence."""
    if pipeline_name not in PIPELINES:
        return {
            "error": f"Unknown pipeline: {pipeline_name}",
            "available": list(PIPELINES.keys())
        }

    pipeline = PIPELINES[pipeline_name]
    results = {
        "pipeline": pipeline_name,
        "description": pipeline["description"],
        "purpose": pipeline["purpose"],
        "steps": [],
        "success": True
    }

    for tool in pipeline["steps"]:
        step_result = run_tool(tool)
        results["steps"].append(step_result)
        if "error" in step_result or not step_result.get("success", False):
            results["success"] = False
            # Continue anyway to show full picture

    return results

def list_pipelines():
    """Show available pipelines."""
    print("Available Composition Pipelines:")
    print("-" * 40)
    for name, info in PIPELINES.items():
        print(f"\n  {name}:")
        print(f"    {info['description']}")
        print(f"    Steps: {' → '.join(info['steps'])}")
        print(f"    Purpose: {info['purpose']}")

def main():
    if len(sys.argv) < 2:
        list_pipelines()
        print("\n\nUsage: python tool_composer.py <pipeline_name>")
        return

    pipeline_name = sys.argv[1]

    if pipeline_name == "--list":
        list_pipelines()
        return

    result = compose(pipeline_name)

    print(f"=== Pipeline: {result.get('pipeline', 'unknown')} ===")
    print(f"Purpose: {result.get('purpose', 'N/A')}")
    print(f"Overall Success: {result.get('success', False)}")
    print("\n--- Step Results ---")

    for i, step in enumerate(result.get("steps", []), 1):
        tool = step.get("tool", "unknown")
        success = "✓" if step.get("success") else "✗"
        print(f"\n[{i}] {tool} {success}")
        if step.get("output"):
            # Show first 500 chars of output
            output = step["output"][:500]
            for line in output.split("\n")[:10]:
                print(f"    {line}")
        if step.get("error"):
            print(f"    ERROR: {step['error']}")

if __name__ == "__main__":
    main()
