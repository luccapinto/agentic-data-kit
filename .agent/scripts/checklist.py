#!/usr/bin/env python3
"""
Master Checklist Runner - Antigravity Kit
==========================================

Orchestrates all validation scripts in priority order.
Use this for incremental validation during development.

Usage:
    python scripts/checklist.py .

Priority Order:
    P0: Security Scan (vulnerabilities, secrets)
    P1: SQL Lint & Python Lint
    P2: Data Documentation Check
    P3: Data Pipeline Test Runner
    P4: Heavy Query Profiler
"""

import sys
import subprocess
import argparse
from pathlib import Path
from typing import List, Tuple, Optional

# ANSI colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}\n")

def print_step(text: str):
    print(f"{Colors.BOLD}{Colors.BLUE}[RUN] {text}{Colors.ENDC}")

def print_success(text: str):
    print(f"{Colors.GREEN}[OK] {text}{Colors.ENDC}")

def print_warning(text: str):
    print(f"{Colors.YELLOW}[WARN] {text}{Colors.ENDC}")

def print_error(text: str):
    print(f"{Colors.RED}[FAIL] {text}{Colors.ENDC}")

# Define priority-ordered checks for the Data Team
CORE_CHECKS = [
    ("Lint (Ruff + SQLFluff)", ".agent/scripts/lint_runner.py", True),
    ("Schema Validation", ".agent/scripts/schema_validator.py", False),
    ("Data Contracts", ".agent/skills/data-quality-testing/scripts/data_contracts_validator.py", False),
]

def check_script_exists(script_path: Path) -> bool:
    """Check if script file exists"""
    return script_path.exists() and script_path.is_file()

def run_script(name: str, script_path: Path, project_path: str, url: Optional[str] = None) -> dict:
    """
    Run a validation script and capture results
    
    Returns:
        dict with keys: name, passed, output, skipped
    """
    if not check_script_exists(script_path):
        print_warning(f"{name}: Script not found, skipping")
        return {"name": name, "passed": True, "output": "", "skipped": True}
    
    print_step(f"Running: {name}")
    
    # Build command
    cmd = ["python", str(script_path), project_path]
    if url:
        cmd.append(url)
    
    # Run script
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        passed = result.returncode == 0
        
        if passed:
            print_success(f"{name}: PASSED")
        else:
            print_error(f"{name}: FAILED")
            if result.stderr:
                print(f"  Error: {result.stderr[:200]}")
        
        return {
            "name": name,
            "passed": passed,
            "output": result.stdout,
            "error": result.stderr,
            "skipped": False
        }
    
    except subprocess.TimeoutExpired:
        print_error(f"{name}: TIMEOUT (>5 minutes)")
        return {"name": name, "passed": False, "output": "", "error": "Timeout", "skipped": False}
    
    except Exception as e:
        print_error(f"{name}: ERROR - {str(e)}")
        return {"name": name, "passed": False, "output": "", "error": str(e), "skipped": False}

def print_summary(results: List[dict]):
    """Print final summary report"""
    print_header("CHECKLIST SUMMARY")
    
    passed_count = sum(1 for r in results if r["passed"] and not r.get("skipped"))
    failed_count = sum(1 for r in results if not r["passed"] and not r.get("skipped"))
    skipped_count = sum(1 for r in results if r.get("skipped"))
    
    print(f"Total Checks: {len(results)}")
    print(f"{Colors.GREEN}[OK] Passed: {passed_count}{Colors.ENDC}")
    print(f"{Colors.RED}[FAIL] Failed: {failed_count}{Colors.ENDC}")
    print(f"{Colors.YELLOW}[SKIP]  Skipped: {skipped_count}{Colors.ENDC}")
    print()
    
    # Detailed results
    for r in results:
        if r.get("skipped"):
            status = f"{Colors.YELLOW}[SKIP]{Colors.ENDC}"
        elif r["passed"]:
            status = f"{Colors.GREEN}[OK]{Colors.ENDC}"
        else:
            status = f"{Colors.RED}[FAIL]{Colors.ENDC}"
        
        print(f"{status} {r['name']}")
    
    print()
    
    if failed_count > 0:
        print_error(f"{failed_count} check(s) FAILED - Please fix before proceeding")
        return False
    else:
        print_success("All checks PASSED")
        return True

def main():
    parser = argparse.ArgumentParser(
        description="Run Antigravity Kit validation checklist",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/checklist.py .                      # Core data checks
        """
    )
    parser.add_argument("path", nargs="?", default=".", help="Path to check (project root)")
    
    args = parser.parse_args()
    
    project_path = Path(args.path).resolve()
    
    if not project_path.exists():
        print_error(f"Project path does not exist: {project_path}")
        sys.exit(1)
    
    print_header("[ANTIGRAVITY KIT - MASTER CHECKLIST]")
    print(f"Project: {project_path}")
    
    results = []
    
    # Run core checks
    print_header("CORE CHECKS")
    for name, script_path, required in CORE_CHECKS:
        script = project_path / script_path
        result = run_script(name, script, str(project_path))
        results.append(result)
        
        # If required check fails, stop
        if required and not result["passed"] and not result.get("skipped"):
            print_error(f"CRITICAL: {name} failed. Stopping checklist.")
            print_summary(results)
            sys.exit(1)
    

    
    # Print summary
    all_passed = print_summary(results)
    
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
