#!/usr/bin/env python3
"""
Batch test solver on multiple instances and categorize failures.
Produces CSV report: instance_id, repo, status (PASS/FAIL), failure_reason
"""
import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime

def run_solver_on_instance(instance_idx):
    """Run solver on a single instance, return (success, output, failure_type)."""
    try:
        result = subprocess.run(
            [sys.executable, "/home/user/evome/tools/swe_solver.py", str(instance_idx)],
            capture_output=True,
            text=True,
            timeout=300
        )

        output = result.stdout + result.stderr
        success = "PASS" in result.stdout

        # Categorize failure
        failure_type = "N/A"
        if not success:
            if "Missing required plugins" in output or "could not find" in output:
                failure_type = "MISSING_DEPS"
            elif "X11" in output or "display" in output or "ModuleNotFoundError" in output:
                failure_type = "ENV_ISSUE"
            elif "Patch application failed" in output or "patch does not apply" in output:
                failure_type = "PATCH_LOGIC"
            elif "Tests failed" in output:
                failure_type = "TEST_FAILURE"
            else:
                failure_type = "UNKNOWN"

        return success, failure_type, output
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT", "Solver timeout after 300s"
    except Exception as e:
        return False, "ERROR", str(e)

def main():
    # Test on instances: 0-4, 10-14, 20-24, 30-34, 50-54 (25 diverse instances)
    test_instances = list(range(0, 5)) + list(range(10, 15)) + list(range(20, 25)) + list(range(30, 35)) + list(range(50, 55))

    results = []
    timestamp = datetime.now().isoformat()

    print(f"[{timestamp}] Starting batch test on {len(test_instances)} instances...")
    print("Instance\tStatus\tFailure Type\tDetails")
    print("-" * 80)

    for idx, instance_idx in enumerate(test_instances):
        success, failure_type, output = run_solver_on_instance(instance_idx)
        status = "PASS" if success else "FAIL"

        # Extract repo name from output if possible
        repo = "unknown"
        for line in output.split('\n'):
            if line.startswith("Repo:"):
                repo = line.split(":", 1)[1].strip()
                break

        results.append({
            "instance_id": instance_idx,
            "repo": repo,
            "status": status,
            "failure_type": failure_type,
            "output": output[:200]  # First 200 chars
        })

        print(f"{instance_idx}\t{status}\t{failure_type}\t{repo}")
        print(f"  {idx+1}/{len(test_instances)}")

    # Summary statistics
    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    pass_rate = passed / len(results) * 100

    print("\n" + "=" * 80)
    print(f"SUMMARY: {passed}/{len(results)} PASS ({pass_rate:.1f}%)")
    print("=" * 80)

    # Failure breakdown
    failure_types = {}
    for r in results:
        if r['status'] == 'FAIL':
            ft = r['failure_type']
            failure_types[ft] = failure_types.get(ft, 0) + 1

    print("\nFailure Breakdown:")
    for ft, count in sorted(failure_types.items(), key=lambda x: -x[1]):
        print(f"  {ft}: {count} instances")

    # Save detailed results
    output_file = Path("/home/user/evome/batch_test_results.json")
    with open(output_file, 'w') as f:
        json.dump({
            "timestamp": timestamp,
            "total_instances": len(results),
            "passed": passed,
            "failed": failed,
            "pass_rate": pass_rate,
            "failure_breakdown": failure_types,
            "results": results
        }, f, indent=2)

    print(f"\nDetailed results saved to: {output_file}")

    return 0 if pass_rate >= 50 else 1

if __name__ == "__main__":
    sys.exit(main())
