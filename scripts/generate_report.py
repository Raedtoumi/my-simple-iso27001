#!/usr/bin/env python3
import json
import os
from datetime import datetime

print("📊 Generating Compliance Report...")

# Create reports directory
os.makedirs('reports', exist_ok=True)

# Load evidence
try:
    with open('evidence/compliance_evidence.json', 'r') as f:
        evidence = json.load(f)
except FileNotFoundError:
    evidence = {}
    print("❌ No evidence file found")

# Calculate compliance score
checks = []

# Check 1: Policies folder exists
if evidence.get('files_check', {}).get('has_policies_folder'):
    checks.append({"name": "Policies Directory", "status": "PASS", "importance": "HIGH"})
else:
    checks.append({"name": "Policies Directory", "status": "FAIL", "importance": "HIGH"})

# Check 2: Documents folder exists  
if evidence.get('files_check', {}).get('has_documents_folder'):
    checks.append({"name": "Documents Directory", "status": "PASS", "importance": "MEDIUM"})
else:
    checks.append({"name": "Documents Directory", "status": "FAIL", "importance": "MEDIUM"})

# Check 3: GitHub Actions configured
if evidence.get('files_check', {}).get('has_github_actions'):
    checks.append({"name": "GitHub Actions", "status": "PASS", "importance": "HIGH"})
else:
    checks.append({"name": "GitHub Actions", "status": "FAIL", "importance": "HIGH"})

# Check 4: Has policy files
if evidence.get('file_counts', {}).get('policy_files', 0) > 0:
    checks.append({"name": "Policy Files", "status": "PASS", "importance": "HIGH"})
else:
    checks.append({"name": "Policy Files", "status": "FAIL", "importance": "HIGH"})

# Calculate score
passed_checks = [c for c in checks if c['status'] == 'PASS']
compliance_score = len(passed_checks) / len(checks) * 100

# Generate report
report = {
    "generated_at": datetime.now().isoformat(),
    "compliance_score": round(compliance_score, 1),
    "summary": {
        "total_checks": len(checks),
        "passed": len(passed_checks),
        "failed": len(checks) - len(passed_checks)
    },
    "checks": checks,
    "recommendations": []
}

# Add recommendations
if compliance_score < 100:
    report["recommendations"].append("Add more policy files in the 'policies' folder")
if not evidence.get('files_check', {}).get('has_documents_folder'):
    report["recommendations"].append("Create a 'documents' folder for ISO documentation")

# Save JSON report
with open('reports/compliance_report.json', 'w') as f:
    json.dump(report, f, indent=2)

# Save pretty Markdown report
with open('reports/compliance_summary.md', 'w') as f:
    f.write("# 📋 ISO 27001 Compliance Report\n\n")
    f.write(f"**Generated**: {report['generated_at']}\n\n")
    f.write(f"## 🎯 Compliance Score: {report['compliance_score']}%\n\n")
    
    f.write("## 📊 Check Results\n\n")
    for check in checks:
        icon = "✅" if check['status'] == 'PASS' else "❌"
        f.write(f"{icon} **{check['name']}** - {check['status']} ({check['importance']})\n")
    
    f.write(f"\n## 📈 Summary\n")
    f.write(f"- **Passed**: {report['summary']['passed']} checks\n")
    f.write(f"- **Failed**: {report['summary']['failed']} checks\n")
    f.write(f"- **Total**: {report['summary']['total_checks']} checks\n\n")
    
    if report['recommendations']:
        f.write("## 💡 Recommendations\n\n")
        for rec in report['recommendations']:
            f.write(f"- {rec}\n")

print("✅ Compliance report generated!")
print(f"📈 Score: {report['compliance_score']}%")
print(f"✅ Passed: {report['summary']['passed']}/{report['summary']['total_checks']}")