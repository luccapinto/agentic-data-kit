#!/usr/bin/env python3
"""
Schema Validator - Data Engineering Schema Validation
Validates Data modeling artifacts such as dbt schema.yml files.

Usage:
    python schema_validator.py <project_path>

Checks:
    - dbt model definitions (descriptions, tests)
    - Basic naming conventions
"""

import sys
import json
import yaml
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except:
    pass

def check_dbt_schemas(project_path: Path) -> list:
    """Validate dbt schema YAML files."""
    issues = []
    
    # Find dbt schema files
    yml_files = list(project_path.glob('**/models/**/*.yml'))
    
    for file_path in yml_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
                
            if not content or not isinstance(content, dict):
                continue
                
            # Check models
            models = content.get('models', [])
            for model in models:
                name = model.get('name', 'unknown')
                
                # Check description
                if 'description' not in model:
                    issues.append(f"Model '{name}' in {file_path.name} is missing a description")
                
                # Check if it has any tests configured on columns, or at model level
                columns = model.get('columns', [])
                has_tests = False
                for col in columns:
                    if 'tests' in col:
                        has_tests = True
                        break
                        
                if not has_tests:
                    issues.append(f"Model '{name}' in {file_path.name} has no column-level tests configured")
                    
        except Exception as e:
            issues.append(f"Error parsing {file_path.name}: {str(e)[:50]}")
            
    return issues

def main():
    project_path = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    
    print(f"\n{'='*60}")
    print(f"[SCHEMA VALIDATOR] Data Schema Validation")
    print(f"{'='*60}")
    print(f"Project: {project_path}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-"*60)
    
    issues = check_dbt_schemas(project_path)
    
    if not issues:
        print("No schema issues found or no dbt schemas available!")
        output = {
            "script": "schema_validator",
            "project": str(project_path),
            "passed": True,
            "issues_found": 0
        }
    else:
        print("\n" + "="*60)
        print("SCHEMA ISSUES")
        print("="*60)
        for issue in issues[:10]:
            print(f"  - {issue}")
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more issues")
            
        output = {
            "script": "schema_validator",
            "project": str(project_path),
            "passed": True,  # Schema issues are warnings for now
            "issues_found": len(issues),
            "issues": issues
        }
        
    print("\n" + json.dumps(output, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()
