#!/usr/bin/env python3
import json
import subprocess
import os
from datetime import datetime

def evaluate_with_opa():
    """Évalue les preuves avec OPA"""
    
    # Charger les preuves
    with open('evidence/real_evidence.json', 'r') as f:
        evidence = json.load(f)
    
    results = {
        "evaluation_time": datetime.utcnow().isoformat(),
        "policies_evaluated": [],
        "scores": {},
        "compliance_status": {}
    }
    
    # Évaluer chaque package OPA
    policies_dir = "policies"
    
    for root, dirs, files in os.walk(policies_dir):
        for file in files:
            if file.endswith('.rego'):
                policy_path = os.path.join(root, file)
                package_name = file.replace('.rego', '')
                category = os.path.basename(root)
                
                print(f"🔍 Évaluation de {category}/{package_name}...")
                
                try:
                    # Exécuter OPA
                    result = subprocess.run([
                        'opa', 'eval',
                        '--data', policy_path,
                        '--input', 'evidence/real_evidence.json',
                        '--format', 'json',
                        'data'
                    ], capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        opa_output = json.loads(result.stdout)
                        package_results = parse_opa_results(opa_output, package_name)
                        results["policies_evaluated"].append({
                            "package": f"{category}.{package_name}",
                            "results": package_results
                        })
                        
                        # Extraire le score si disponible
                        score_key = f"{package_name}_score"
                        if score_key in package_results:
                            results["scores"][f"{category}.{package_name}"] = package_results[score_key]
                            
                    else:
                        print(f"❌ Erreur OPA pour {package_name}: {result.stderr}")
                        
                except subprocess.TimeoutExpired:
                    print(f"⏰ Timeout pour {package_name}")
                except Exception as e:
                    print(f"❌ Exception pour {package_name}: {e}")
    
    # Calculer le score global
    results["overall_score"] = calculate_overall_score(results["scores"])
    results["compliance_status"] = assess_compliance_status(results["scores"])
    
    return results

def parse_opa_results(opa_output, package_name):
    """Parse les résultats OPA"""
    results = {}
    
    try:
        expressions = opa_output.get('result', [{}])[0].get('expressions', [])
        for expr in expressions:
            value = expr.get('value', {})
            if isinstance(value, dict):
                for key, val in value.items():
                    if not key.startswith('_'):  # Ignorer les variables internes
                        results[key] = val
    except Exception as e:
        print(f"❌ Erreur parsing OPA results: {e}")
    
    return results

def calculate_overall_score(scores):
    """Calcule le score global de conformité"""
    if not scores:
        return 0
    
    total_score = sum(scores.values())
    return round(total_score / len(scores), 1)

def assess_compliance_status(scores):
    """Évalue le statut de conformité"""
    status = {}
    
    for category, score in scores.items():
        if score >= 80:
            status[category] = "CONFORME"
        elif score >= 60:
            status[category] = "PARTIELLEMENT CONFORME"
        else:
            status[category] = "NON CONFORME"
    
    return status

def main():
    print("⚖️ Évaluation des politiques avec OPA...")
    
    # Vérifier qu'OPA est installé
    try:
        subprocess.run(['opa', 'version'], capture_output=True, check=True)
    except:
        print("❌ OPA n'est pas installé ou accessible")
        return
    
    # Évaluer avec OPA
    opa_results = evaluate_with_opa()
    
    # Sauvegarder les résultats
    os.makedirs('reports', exist_ok=True)
    
    with open('reports/opa_evaluation_results.json', 'w') as f:
        json.dump(opa_results, f, indent=2)
    
    print("✅ Évaluation OPA terminée!")
    print(f"🎯 Score global: {opa_results['overall_score']}%")
    print(f"📊 Politiques évaluées: {len(opa_results['policies_evaluated'])}")
    print(f"📈 Scores par catégorie: {opa_results['scores']}")

if __name__ == "__main__":
    main()