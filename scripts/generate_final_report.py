#!/usr/bin/env python3
import json
import os
from datetime import datetime

def generate_final_report():
    """Génère le rapport final de conformité"""
    
    # Vérifier si les résultats OPA existent
    if not os.path.exists('reports/opa_evaluation_results.json'):
        print("❌ Fichier OPA results non trouvé. Exécutez d'abord evaluate_with_opa.py")
        return create_fallback_report()
    
    # Charger les résultats OPA
    try:
        with open('reports/opa_evaluation_results.json', 'r') as f:
            opa_results = json.load(f)
    except:
        print("❌ Erreur lecture OPA results")
        return create_fallback_report()
    
    # Charger les preuves
    evidence = {}
    if os.path.exists('evidence/real_evidence.json'):
        try:
            with open('evidence/real_evidence.json', 'r') as f:
                evidence = json.load(f)
        except:
            evidence = {"error": "Erreur lecture evidence"}
    
    report = {
        "generation_time": datetime.utcnow().isoformat(),
        "summary": generate_summary(opa_results, evidence),
        "detailed_results": opa_results.get("policies_evaluated", []),
        "recommendations": generate_recommendations(opa_results, evidence),
        "next_steps": generate_next_steps(opa_results)
    }
    
    # Sauvegarder le rapport JSON
    os.makedirs('reports', exist_ok=True)
    with open('reports/final_compliance_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    # Générer le rapport Markdown
    generate_markdown_report(report, evidence)
    
    return report

def create_fallback_report():
    """Crée un rapport de secours si les données sont manquantes"""
    report = {
        "generation_time": datetime.utcnow().isoformat(),
        "summary": {
            "overall_compliance_score": 0,
            "policies_evaluated_count": 0,
            "compliance_status": {"error": "Données manquantes"},
            "evidence_collected": {"error": "Exécutez collect_real_evidence.py d'abord"}
        },
        "detailed_results": [],
        "recommendations": [
            "Exécutez d'abord scripts/collect_real_evidence.py",
            "Puis scripts/evaluate_with_opa.py",
            "Enfin scripts/generate_final_report.py"
        ],
        "next_steps": [
            "Vérifier que tous les scripts existent",
            "Exécuter les scripts dans le bon ordre",
            "Vérifier les permissions des fichiers"
        ]
    }
    
    os.makedirs('reports', exist_ok=True)
    with open('reports/final_compliance_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    generate_markdown_report(report, {})
    return report

def generate_summary(opa_results, evidence):
    """Génère le résumé du rapport"""
    return {
        "overall_compliance_score": opa_results.get("overall_score", 0),
        "policies_evaluated_count": len(opa_results.get("policies_evaluated", [])),
        "compliance_status": opa_results.get("compliance_status", {}),
        "evidence_collected": {
            "system_checks": evidence.get("system", {}).get("file_structure", {}),
            "policy_files": evidence.get("policies", {}).get("total_policies", 0),
            "opa_policies": evidence.get("policies", {}).get("opa_policies", 0)
        }
    }

def generate_recommendations(opa_results, evidence):
    """Génère les recommandations d'amélioration"""
    recommendations = []
    
    # Recommandations basées sur les scores
    scores = opa_results.get("scores", {})
    for category, score in scores.items():
        if score < 60:
            recommendations.append(f"Améliorer la conformité dans {category} (score: {score}%)")
    
    # Recommandations basées sur les preuves manquantes
    policies = evidence.get("policies", {})
    if policies.get("total_policies", 0) < 2:
        recommendations.append("Créer les politiques de sécurité manquantes (au moins 2)")
    
    if policies.get("opa_policies", 0) < 3:
        recommendations.append("Développer plus de politiques OPA (actuellement: {})".format(
            policies.get("opa_policies", 0)
        ))
    
    system = evidence.get("system", {})
    if not system.get("has_tests", False):
        recommendations.append("Implémenter des tests automatisés")
    
    if not system.get("has_github_actions", False):
        recommendations.append("Configurer GitHub Actions pour la CI/CD")
    
    return recommendations

def generate_next_steps(opa_results):
    """Génère les prochaines étapes"""
    return [
        "Réviser les écarts de conformité identifiés",
        "Implémenter les recommandations prioritaires", 
        "Mettre à jour les politiques OPA si nécessaire",
        "Planifier le prochain audit de conformité",
        "Documenter les améliorations apportées"
    ]

def generate_markdown_report(report, evidence):
    """Génère un rapport Markdown lisible"""
    
    with open('reports/final_compliance_report.md', 'w') as f:
        f.write("# 📋 Rapport de Conformité ISO 27001:2022\n\n")
        f.write(f"**Date de génération**: {report['generation_time']}\n\n")
        
        score = report['summary']['overall_compliance_score']
        f.write(f"## 🎯 Score Global de Conformité: {score}%\n\n")
        
        # Barre de progression visuelle
        progress_bar = "🟩" * (score // 20) + "⬜" * (5 - (score // 20))
        f.write(f"{progress_bar}\n\n")
        
        f.write("## 📊 Statut de Conformité par Catégorie\n\n")
        status_dict = report['summary']['compliance_status']
        if status_dict and "error" not in str(status_dict):
            for category, status in status_dict.items():
                emoji = "✅" if status == "CONFORME" else "⚠️" if status == "PARTIELLEMENT CONFORME" else "❌"
                f.write(f"{emoji} **{category}**: {status}\n")
        else:
            f.write("❌ *Données de conformité non disponibles*\n")
        
        f.write(f"\n## 📈 Métriques Collectées\n\n")
        evidence_data = report['summary']['evidence_collected']
        if "error" not in str(evidence_data):
            f.write(f"- 🔍 Politiques évaluées: {report['summary']['policies_evaluated_count']}\n")
            f.write(f"- 📋 Politiques documentées: {evidence_data.get('policy_files', 0)}\n")
            f.write(f"- ⚖️ Politiques OPA: {evidence_data.get('opa_policies', 0)}\n")
        else:
            f.write("❌ *Métriques non disponibles - exécutez collect_real_evidence.py*\n")
        
        f.write(f"\n## 💡 Recommandations d'Amélioration\n\n")
        recommendations = report['recommendations']
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                f.write(f"{i}. {rec}\n")
        else:
            f.write("✅ Aucune recommandation critique - bon travail!\n")
        
        f.write(f"\n## 🚀 Prochaines Étapes Recommandées\n\n")
        for step in report['next_steps']:
            f.write(f"- {step}\n")
        
        f.write(f"\n## 🔄 Workflow d'Audit\n\n")
        f.write("1. `scripts/collect_real_evidence.py` - Collecte des preuves\n")
        f.write("2. `scripts/evaluate_with_opa.py` - Évaluation avec OPA\n") 
        f.write("3. `scripts/generate_final_report.py` - Génération du rapport\n")
        
        f.write(f"\n---\n")
        f.write(f"*Rapport généré automatiquement par le système de conformité ISO 27001* | ")
        f.write(f"[Voir les artefacts](#) | ")
        f.write(f"[Journal d'exécution](#)\n")

def main():
    print("📊 Génération du rapport final de conformité...")
    
    report = generate_final_report()
    
    print("✅ Rapport final généré!")
    print(f"🎯 Score global: {report['summary']['overall_compliance_score']}%")
    print(f"📋 Politiques évaluées: {report['summary']['policies_evaluated_count']}")
    print(f"💡 Recommandations: {len(report['recommendations'])}")
    print(f"📄 Rapport disponible: reports/final_compliance_report.md")
    
    # Afficher un résumé dans la console
    if report['recommendations']:
        print(f"\n🔔 Recommandations importantes:")
        for rec in report['recommendations'][:3]:  # Afficher les 3 premières
            print(f"   - {rec}")

if __name__ == "__main__":
    main()