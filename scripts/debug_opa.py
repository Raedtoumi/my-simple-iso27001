#!/usr/bin/env python3
import json
import subprocess
import os

def debug_opa():
    """Diagnostique le problème OPA"""
    
    print("🔧 DIAGNOSTIC OPA")
    print("=" * 50)
    
    # 1. Vérifier le fichier evidence
    print("1. 📁 Vérification du fichier evidence...")
    try:
        with open('evidence/real_evidence.json', 'r') as f:
            evidence = json.load(f)
        print("   ✅ Fichier evidence chargé")
        print(f"   📊 Sections: {list(evidence.keys())}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return
    
    # 2. Vérifier les politiques OPA
    print("\n2. ⚖️ Vérification des politiques OPA...")
    policies_dir = "policies"
    rego_files = []
    
    for root, dirs, files in os.walk(policies_dir):
        for file in files:
            if file.endswith('.rego'):
                rego_files.append(os.path.join(root, file))
                print(f"   📄 {os.path.join(root, file)}")
    
    if not rego_files:
        print("   ❌ Aucun fichier .rego trouvé!")
        return
    
    # 3. Tester chaque politique avec OPA
    print("\n3. 🧪 Test manuel de chaque politique...")
    for rego_file in rego_files:
        print(f"\n   🔍 Test de {rego_file}:")
        try:
            result = subprocess.run([
                'opa', 'eval',
                '--data', rego_file,
                '--input', 'evidence/real_evidence.json',
                '--format', 'pretty',
                'data'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("   ✅ OPA a exécuté avec succès")
                if result.stdout.strip():
                    print("   📋 Résultat:")
                    for line in result.stdout.split('\n'):
                        if line.strip():
                            print(f"      {line}")
                else:
                    print("   ⚠️  Aucun résultat retourné")
            else:
                print(f"   ❌ Erreur OPA: {result.stderr}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")

if __name__ == "__main__":
    debug_opa()