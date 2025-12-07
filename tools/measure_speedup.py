#!/usr/bin/env python3
"""
Measure test execution speedup from environment resilience and targeted execution.
Compares: function-level vs file-level vs full suite execution times.
Reports: speedup factors and timing metrics.
"""
import json
import subprocess
import tempfile
import time
import os
from pathlib import Path
from swe_solver import (
    parse_test_functions,
    extract_test_files_from_patch,
    run_tests,
    detect_language,
    discover_requirements,
    parse_pytest_plugins_from_config,
    install_missing_plugins,
)


def measure_test_execution(repo_path, test_patch, test_name=""):
    """
    Measure execution time for different test targeting levels.
    Returns dict with timing metrics.
    """
    metrics = {
        "test_name": test_name,
        "times": {},
        "speedups": {},
        "success": {}
    }

    try:
        # Ensure repo is clean before each test
        subprocess.run(['git', 'reset', '--hard'], cwd=repo_path, capture_output=True)

        # LEVEL 1: Ultra-targeted (function-level)
        if test_patch:
            test_functions_dict = parse_test_functions(test_patch)
            if test_functions_dict:
                start_time = time.time()
                test_file_funcs = list(test_functions_dict.items())
                if test_file_funcs:
                    test_file, test_funcs = test_file_funcs[0]
                    if test_funcs:
                        filter_expr = ' or '.join(test_funcs)
                        cmd = ['python', '-m', 'pytest', '-xvs', '-k', filter_expr, test_file]
                        result = subprocess.run(cmd, cwd=repo_path, capture_output=True, timeout=120)
                        elapsed = time.time() - start_time
                        metrics["times"]["function_level"] = elapsed
                        metrics["success"]["function_level"] = result.returncode == 0
                        print(f"  [Function-level] {test_file}::{filter_expr} -> {elapsed:.2f}s (rc={result.returncode})")

        # LEVEL 2: File-level
        if test_patch:
            subprocess.run(['git', 'reset', '--hard'], cwd=repo_path, capture_output=True)
            test_files = extract_test_files_from_patch(test_patch)
            if test_files:
                start_time = time.time()
                cmd = ['python', '-m', 'pytest', '-xvs'] + test_files
                result = subprocess.run(cmd, cwd=repo_path, capture_output=True, timeout=120)
                elapsed = time.time() - start_time
                metrics["times"]["file_level"] = elapsed
                metrics["success"]["file_level"] = result.returncode == 0
                print(f"  [File-level] {len(test_files)} files -> {elapsed:.2f}s (rc={result.returncode})")

        # LEVEL 3: Full suite (sample - just count time)
        subprocess.run(['git', 'reset', '--hard'], cwd=repo_path, capture_output=True)
        start_time = time.time()
        cmd = ['python', '-m', 'pytest', '-xvs', '--co', '-q']  # Just collect tests, don't run
        result = subprocess.run(cmd, cwd=repo_path, capture_output=True, timeout=120)
        elapsed = time.time() - start_time
        metrics["times"]["full_collection"] = elapsed  # Time to just collect all tests
        print(f"  [Full collection] Collection time -> {elapsed:.2f}s")

        # Calculate speedups
        if "function_level" in metrics["times"] and "file_level" in metrics["times"]:
            metrics["speedups"]["function_vs_file"] = (
                metrics["times"]["file_level"] / metrics["times"]["function_level"]
            )
        if "file_level" in metrics["times"] and "full_collection" in metrics["times"]:
            metrics["speedups"]["file_vs_collection"] = (
                metrics["times"]["full_collection"] / metrics["times"]["file_level"]
            )

        return metrics

    except Exception as e:
        print(f"  [ERROR] Measurement failed: {e}")
        metrics["error"] = str(e)
        return metrics


def prepare_environment(repo_path):
    """Ensure environment is ready for testing."""
    try:
        language = detect_language(repo_path)
        if language == 'python':
            # Install pytest and plugins
            subprocess.run(['python', '-m', 'pip', 'install', '-q', 'pytest'], timeout=30)

            # Discover and install pytest plugins
            required_plugins = discover_requirements(repo_path)
            pytest_plugins = [p for p in required_plugins if 'pytest' in p.lower()]
            if pytest_plugins:
                install_missing_plugins(pytest_plugins, repo_path)
                print(f"  [INFO] Environment prepared: {len(pytest_plugins)} plugins installed")

        return language
    except Exception as e:
        print(f"  [WARN] Environment preparation failed: {e}")
        return 'unknown'


def run_measurement_cycle(sample_file, output_file):
    """Run speedup measurements on sample instances."""
    with open(sample_file) as f:
        instances = json.load(f)

    results = {
        "timestamp": time.time(),
        "sample_size": len(instances),
        "measurements": []
    }

    for i, instance in enumerate(instances[:5]):  # Measure on first 5 instances
        instance_id = instance.get('instance_id', f'instance_{i}')
        repo = instance.get('repo', '')

        print(f"\n[{i+1}/5] Measuring {instance_id}...")

        try:
            # Clone repo (or use existing)
            repo_path = Path(tempfile.gettempdir()) / repo.replace('/', '_')
            if not repo_path.exists():
                print(f"  Cloning {repo}...")
                subprocess.run(
                    ['git', 'clone', f'https://github.com/{repo}.git', repo_path],
                    capture_output=True,
                    timeout=60
                )

            # Reset to base commit
            base_commit = instance.get('base_commit', 'HEAD')
            subprocess.run(
                ['git', 'checkout', base_commit],
                cwd=repo_path,
                capture_output=True,
                timeout=30
            )

            # Prepare environment
            language = prepare_environment(repo_path)

            # Measure execution times
            test_patch = instance.get('test_patch', '')
            metrics = measure_test_execution(repo_path, test_patch, instance_id)

            metrics["instance_id"] = instance_id
            metrics["repo"] = repo
            metrics["language"] = language
            results["measurements"].append(metrics)

            print(f"  Speedups: {metrics.get('speedups', {})}")

        except Exception as e:
            print(f"  [ERROR] Failed to measure {instance_id}: {e}")
            results["measurements"].append({
                "instance_id": instance_id,
                "error": str(e)
            })

    # Write results
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults written to {output_file}")

    # Summary
    print("\n=== MEASUREMENT SUMMARY ===")
    for m in results["measurements"]:
        if "speedups" in m:
            print(f"{m.get('instance_id', 'unknown')}: {m['speedups']}")


if __name__ == '__main__':
    sample_file = '/home/user/evome/external_validation/swe_bench_sample.json'
    output_file = '/home/user/evome/external_validation/speedup_measurements.json'
    run_measurement_cycle(sample_file, output_file)
