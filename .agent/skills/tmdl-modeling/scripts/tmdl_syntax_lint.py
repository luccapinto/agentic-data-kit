#!/usr/bin/env python3
"""
TMDL Syntax Linter
Validates the basic syntax of Tabular Model Definition Language (TMDL) files.
Since TMDL relies heavily on indentation (like YAML, but different), this
script warns on potentially misaligned properties or expressions.
"""

import sys
import re
from pathlib import Path

def lint_tmdl_file(filepath: Path) -> list:
    issues = []
    try:
        content = filepath.read_text(encoding="utf-8")
        lines = content.splitlines()
        
        in_expression = False
        expression_indent = 0
        
        for i, line in enumerate(lines, 1):
            line_str = line.strip()
            
            # Skip empty lines
            if not line_str:
                continue
                
            indent_level = len(line) - len(line.lstrip(' '))
            
            # Detect multi-line expressions (DAX M etc.) which evaluate after `=` or `:`
            if in_expression:
                if indent_level <= expression_indent and line_str != "":
                    # The expression might have ended, or indentation is broken
                    if not line.startswith(" ") and not line.startswith("\t"):
                        in_expression = False
                    
            if not in_expression:
                # Check for properties assignments
                if '=' in line_str and not line_str.startswith("=") and not line_str.startswith("'"):
                    parts = line_str.split('=', 1)
                    prop = parts[0].strip()
                    val = parts[1].strip()
                    
                    if not val: # Line ends with `=`, means start of multi-line block
                        in_expression = True
                        expression_indent = indent_level
                        continue
                        
                # Warn about tabs vs spaces (TMDL prefers spaces)
                if '\t' in line:
                    issues.append(f"Line {i}: Tab character found. TMDL relies on exact spacing; use spaces instead of tabs.")
                    
                # Look for common DAX keywords at root level mistakenly un-indented
                if line_str.startswith("EVALUATE") or line_str.startswith("CALCULATE"):
                    issues.append(f"Line {i}: DAX keyword '{line_str.split()[0]}' found but it appears completely unindented. Verify expression scope.")
                    
    except Exception as e:
        issues.append(f"Error reading {filepath}: {e}")
        
    return issues

def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(f"\n📊 TMDL Syntax Linter running on: {target}\n")
    
    files_to_check = []
    if target.is_file() and target.suffix == ".tmdl":
        files_to_check.append(target)
    elif target.is_dir():
        files_to_check.extend(target.rglob("*.tmdl"))
        
    total_issues = 0
    for file in files_to_check:
        issues = lint_tmdl_file(file)
        if issues:
            print(f"📄 {file.name}:")
            for issue in issues:
                print(f"   ❌ {issue}")
            total_issues += len(issues)
            print()
            
    if total_issues == 0:
        print("✅ No basic TMDL syntax errors found!")
        sys.exit(0)
    else:
        print(f"⚠️ Found {total_issues} TMDL indentation or syntax issues.")
        sys.exit(1)

if __name__ == "__main__":
    main()
