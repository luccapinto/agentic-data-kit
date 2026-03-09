#!/usr/bin/env python3
"""
Documentation Completeness Auditor
Audits data dictionaries (dbt schema.yml files) to ensure definitions
follow the required organizational template (Name, Description, Formula base).
"""

import sys
import yaml
from pathlib import Path

def audit_docs_completeness(filepath: Path) -> list:
    issues = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = yaml.safe_load(f)
            
        if not content or not isinstance(content, dict):
            return issues
            
        models = content.get('models', [])
        for model in models:
            model_name = model.get('name', 'unknown')
            
            model_desc = model.get('description', '')
            if not model_desc or len(model_desc.strip()) < 15:
                 issues.append(f"Model '{model_name}': Description is missing or too short (under 15 chars). Provide business context.")
                 
            columns = model.get('columns', [])
            for col in columns:
                col_name = col.get('name', 'unknown')
                col_desc = col.get('description', '')
                
                # Check semantic layer items (e.g. if it's a metric or dimensional attribute)
                # We expect descriptions to give meaning, not just "this is the id"
                if not col_desc:
                    issues.append(f"Model '{model_name}', Column '{col_name}': Missing description in data dictionary.")
                elif col_name == col_desc.lower() or f"this is the {col_name}" == col_desc.lower():
                     issues.append(f"Model '{model_name}', Column '{col_name}': Description is circular/unhelpful ('{col_desc}'). Explain the business meaning.")

    except Exception as e:
        issues.append(f"Error parsing {filepath}: {e}")
        
    return issues

def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(f"\n📚 Documentation Completeness Auditor running on: {target}\n")
    
    files_to_check = []
    if target.is_file() and target.suffix in ['.yml', '.yaml']:
        files_to_check.append(target)
    elif target.is_dir():
        files_to_check.extend(target.rglob("**/models/**/*.yml")) # Focus heavily on models
        files_to_check.extend(target.rglob("**/models/**/*.yaml"))
        
    total_issues = 0
    checked_files = 0
    for file in files_to_check:
        issues = audit_docs_completeness(file)
        checked_files += 1
        if issues:
            print(f"📄 {file.name}:")
            for issue in issues:
                print(f"   ❌ {issue}")
            total_issues += len(issues)
            print()
            
    if checked_files == 0:
        print("ℹ️ No schema YAMLs found to audit.")
        sys.exit(0)
    elif total_issues == 0:
        print("✅ Data Dictionary completeness is flawless!")
        sys.exit(0)
    else:
        print(f"⚠️ Found {total_issues} documentation gaps in the Data Dictionary.")
        sys.exit(1)

if __name__ == "__main__":
    main()
