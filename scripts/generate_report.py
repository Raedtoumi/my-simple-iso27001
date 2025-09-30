#!/usr/bin/env python3
import json
import os
from datetime import datetime

def generate_final_report():
    """Génère le rapport final de conformité"""
    
    # Charger les résultats OPA
    with open('reports/opa_evaluation_results.json', 'r') as f:
        opa_results = json.load(f)
    
    # Charger les preuves
    with open('evidence/real_evidence.json', 'r') as f:
        evidence = json.load(f)
    
    report = {
        "generation_time": datetime.utcnow().isoformat(),
        "summary": generate_summary(opa_results, evidence),
        "detailed_results": opa_results["policies_evaluated"],
        "recommendations": generate_recommendations(opa_results, evidence),
        "next_steps": generate_next_steps(opa_results)
    }
    
    # Sauvegarder le rapport JSON
    with open('reports/final_compliance_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    # Générer le rapport Markdown
    generate_markdown_report(report, evidence)
    
    return report

def generate_summary(opa_results, evidence):
    """Génère le résumé du rapport"""
    return {
        "overall_compliance_score": opa_results["overall_score"],
        "policies_evaluated_count": len(opa_results["policies_evaluated"]),
        "compliance_status": opa_results["compliance_status"],
        "evidence_collected": {
            "system_checks": len(evidence["system"]),
            "policy_files": evidence["policies"]["total_policies"],
            "opa_policies": evidence["policies"]["opa_policies"]
        }
    }

def generate_recommendations(opa_results, evidence):
    """Génère les recommandations d'amélioration"""
    recommendations = []
    
    # Recommandations basées sur les scores
    for category, score in opa_results["scores"].items():
        if score < 60:
            recommendations.append(f"Améliorer la conformité dans {category} (score: {score}%)")
    
    # Recommandations basées sur les preuves manquantes
    if evidence["policies"]["total_policies"] < 3:
        recommendations.append("Créer les politiques de sécurité manquantes")
    
    if not evidence["policies"]["opa_policies"]:
        recommendations.append("Développer plus de politiques OPA")
    
    if not evidence["system"]["has_tests"]:
        recommendations.append("Implémenter des tests automatisés")
    
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
        
        f.write(f"## 🎯 Score Global de Conformité: {report['summary']['overall_compliance_score']}%\n\n")
        
        f.write("## 📊 Résumé par Catégorie\n\n")
        for category, status in report['summary']['compliance_status'].items():
            emoji = "✅" if status == "CONFORME" else "⚠️" if status == "PARTIELLEMENT CONFORME" else "❌"
            f.write(f"{emoji} **{category}**: {status}\n")
        
        f.write(f"\n## 📈 Preuves Collectées\n\n")
        f.write(f"- ✅ Contrôles système: {report['summary']['evidence_collected']['system_checks']}\n")
        f.write(f"- 📋 Politiques documentées: {report['summary']['evidence_collected']['policy_files']}\n")
        f.write(f"- ⚖️ Politiques OPA: {report['summary']['evidence_collected']['opa_policies']}\n")
        
        f.write(f"\n## 💡 Recommandations ({len(report['recommendations'])})\n\n")
        for i, rec in enumerate(report['recommendations'], 1):
            f.write(f"{i}. {rec}\n")
        
        f.write(f"\n## 🚀 Prochaines Étapes\n\n")
        for step in report['next_steps']:
            f.write(f"- {step}\n")
        
        f.write(f"\n---\n")
        f.write(f"*Rapport généré automatiquement par le système de conformité ISO 27001*")

def main():
    print("📊 Génération du rapport final...")
    
    report = generate_final_report()
    
    print("✅ Rapport final généré!")
    print(f"🎯 Score global: {report['summary']['overall_compliance_score']}%")
    print(f"💡 Recommandations: {len(report['recommendations'])}")
    print(f"📄 Rapport disponible: reports/final_compliance_report.md")

if __name__ == "__main__":
    main()