#!/usr/bin/env python3
"""
Data Contracts Validator
Audits dbt schema YAML files to ensure that data models are properly tested.
Checks if basic data contracts (like unique, not_null on primary keys) are present.
"""

import sys
import yaml
from pathlib import Path

def validate_data_contracts(filepath: Path) -> list:
    issues = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = yaml.safe_load(f)
            
        if not content or not isinstance(content, dict):
            return issues
            
        models = content.get('models', [])
        for model in models:
            model_name = model.get('name', 'unknown')
            columns = model.get('columns', [])
            
            # Check 1: Does the model have any tests at all?
            has_model_tests = 'tests' in model
            has_col_tests = any('tests' in col for col in columns)
            
            if not has_model_tests and not has_col_tests:
                issues.append(f"Model '{model_name}': No tests configured. Data contract violation.")
                continue # Skip further checks if no tests
                
            # Check 2: Try to find a primary key (id, _sk, _key) and check if it's tested
            pk_cols = [c for c in columns if c.get('name', '').endswith('_key') or c.get('name', '').endswith('_sk') or c.get('name') == 'id']
            
            for pk_col in pk_cols:
                tests = pk_col.get('tests', [])
                
                # Handle old dbt syntax (list of strings) and new (list of dicts)
                test_names = []
                for t in tests:
                    if isinstance(t, str):
                        test_names.append(t)
                    elif isinstance(t, dict):
                        test_names.extend(t.keys())
                        
                if 'unique' not in test_names:
                    issues.append(f"Model '{model_name}': Primary key '{pk_col.get('name')}' is missing the 'unique' test.")
                if 'not_null' not in test_names:
                    issues.append(f"Model '{model_name}': Primary key '{pk_col.get('name')}' is missing the 'not_null' test.")

    except Exception as e:
        issues.append(f"Error parsing {filepath}: {e}")
        
    return issues

def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(f"\n[DATA CONTRACTS] Validator running on: {target}\n")
    
    files_to_check = []
    if target.is_file() and target.suffix in ['.yml', '.yaml']:
        files_to_check.append(target)
    elif target.is_dir():
        files_to_check.extend(target.rglob("*.yml"))
        files_to_check.extend(target.rglob("*.yaml"))
        
    total_issues = 0
    checked_files = 0
    for file in files_to_check:
        # Only check dbt model files, skip macro/project config files
        if 'dbt_project' in file.name or 'profiles' in file.name:
            continue
            
        issues = validate_data_contracts(file)
        checked_files += 1
        if issues:
            print(f"[FILE] {file.name}:")
            for issue in issues:
                print(f"   [FAIL] {issue}")
            total_issues += len(issues)
            print()
            
    if checked_files == 0:
        print("[INFO] No YAML files found to check.")
        sys.exit(0)
    elif total_issues == 0:
        print("[OK] Data contracts are successfully upheld across all models!")
        sys.exit(0)
    else:
        print(f"[WARN] Found {total_issues} data contract violations.")
        sys.exit(1)

if __name__ == "__main__":
    main()
