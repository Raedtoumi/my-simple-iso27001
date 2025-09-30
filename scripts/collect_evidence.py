#!/usr/bin/env python3
import json
import os
import subprocess
from datetime import datetime

print("🔄 Starting ISO 27001 Evidence Collection...")

# Create evidence directory
os.makedirs('evidence', exist_ok=True)

# Collect basic information
evidence = {
    "timestamp": datetime.now().isoformat(),
    "repository_name": os.getenv('GITHUB_REPOSITORY', 'local'),
    "branch": os.getenv('GITHUB_REF', 'main'),
    
    # Check what files exist
    "files_check": {
        "has_policies_folder": os.path.exists('policies'),
        "has_documents_folder": os.path.exists('documents'),
        "has_scripts_folder": os.path.exists('scripts'),
        "has_requirements_file": os.path.exists('requirements.txt'),
        "has_github_actions": os.path.exists('.github/workflows')
    },
    
    # Count files
    "file_counts": {
        "policy_files": 0,
        "document_files": 0,
        "script_files": 0
    }
}

# Count files in each directory
try:
    if os.path.exists('policies'):
        evidence["file_counts"]["policy_files"] = len([f for f in os.listdir('policies') if os.path.isfile(os.path.join('policies', f))])
    
    if os.path.exists('documents'):
        evidence["file_counts"]["document_files"] = len([f for f in os.listdir('documents') if os.path.isfile(os.path.join('documents', f))])
    
    if os.path.exists('scripts'):
        evidence["file_counts"]["script_files"] = len([f for f in os.listdir('scripts') if os.path.isfile(os.path.join('scripts', f))])
        
except Exception as e:
    print(f"Error counting files: {e}")

# Save evidence
with open('evidence/compliance_evidence.json', 'w') as f:
    json.dump(evidence, f, indent=2)

print("✅ Evidence collected successfully!")
print(f"📁 Policies folder: {evidence['files_check']['has_policies_folder']}")
print(f"📄 Documents folder: {evidence['files_check']['has_documents_folder']}")
print(f"🔧 Scripts folder: {evidence['files_check']['has_scripts_folder']}")