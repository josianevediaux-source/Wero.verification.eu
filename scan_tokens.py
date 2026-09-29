import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

print("Scanning for hardcoded tokens...")
print()

issues = []

for filename in sorted(html_files):
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if "[REDACTED]" in content or "'[REDACTED]'" in content:
        issues.append((filename, "REDACTED token"))
    
    if "'6078788670'" in content:
        issues.append((filename, "Old Chat ID: 6078788670"))

if issues:
    print(f"Found {len(issues)} issues:")
    for filename, issue in issues:
        print(f"  [ISSUE] {filename}: {issue}")
else:
    print("All files look clean!")
