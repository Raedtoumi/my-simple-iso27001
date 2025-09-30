#!/usr/bin/env python3
import json
import os
from datetime import datetime

def generate_iso27001_2022_report(evidence):
    """Génère un rapport conforme à la structure ISO 27001:2022"""
    
    rapport = {
        "date_generation": datetime.utcnow().isoformat(),
        "norme": "ISO 27001:2022",
        "structure": "4 groupes de contrôles (A.5, A.6, A.7, A.8)",
        "score_global": evidence.get('score_global', 0),
        "evaluation_groupes": evaluer_groupes_controles(evidence),
        "ecarts_principaux": identifier_ecarts_principaux(evidence),
        "recommandations_prioritaires": generer_recommandations_prioritaires(evidence),
        "plan_amelioration": generer_plan_amelioration(evidence)
    }
    
    return rapport

def evaluer_groupes_controles(evidence):
    """Évalue chaque groupe de contrôles"""
    groupes = evidence.get('groupes_controles', {})
    evaluation = {}
    
    for groupe, controles in groupes.items():
        total_controles = len(controles)
        controles_implementes = sum(1 for c in controles.values() if c)
        score = (controles_implementes / total_controles) * 100 if total_controles > 0 else 0
        
        evaluation[groupe] = {
            "score": round(score, 1),
            "controles_implementes": controles_implementes,
            "total_controles": total_controles,
            "statut": "Conforme" if score >= 80 else "Partiellement conforme" if score >= 60 else "Non conforme",
            "controles_cles": identifier_controles_cles(groupe, controles)
        }
    
    return evaluation

def identifier_controles_cles(groupe, controles):
    """Identifie les contrôles clés par groupe"""
    controles_cles = {
        "A.5": ["A.5.1", "A.5.2", "A.5.3", "A.5.7"],
        "A.6": ["A.6.1", "A.6.2", "A.6.3"],
        "A.7": ["A.7.1", "A.7.2", "A.7.3"],
        "A.8": ["A.8.1", "A.8.2", "A.8.7", "A.8.8"]
    }
    
    resultat = {}
    for controle in controles_cles.get(groupe, []):
        if controle in controles:
            resultat[controle] = {
                "implemente": controles[controle],
                "description": get_controle_description(controle)
            }
    
    return resultat

def get_controle_description(code_controle):
    """Retourne la description du contrôle"""
    descriptions = {
        "A.5.1": "Politiques de sécurité de l'information",
        "A.5.2": "Rôles et responsabilités en matière de sécurité",
        "A.5.3": "Séparation des fonctions",
        "A.5.7": "Renseignement sur les menaces",
        "A.6.1": "Vérification préalable du personnel",
        "A.6.2": "Conditions d'emploi",
        "A.6.3": "Sensibilisation, éducation et formation",
        "A.7.1": "Périmètre de sécurité physique",
        "A.7.2": "Contrôles des entrées physiques",
        "A.7.3": "Sécurisation des bureaux et salles",
        "A.8.1": "Dispositifs des utilisateurs finaux",
        "A.8.2": "Droits d'accès privilégiés",
        "A.8.7": "Protection contre les codes malveillants",
        "A.8.8": "Gestion des vulnérabilités techniques"
    }
    return descriptions.get(code_controle, "Contrôle non documenté")

def identifier_ecarts_principaux(evidence):
    """Identifie les écarts principaux"""
    groupes = evidence.get('groupes_controles', {})
    ecarts = []
    
    for groupe, controles in groupes.items():
        for code_controle, implemente in controles.items():
            if not implemente and code_controle in [
                "A.5.1", "A.5.2", "A.6.3", "A.8.2", "A.8.7", "A.8.8"
            ]:
                ecarts.append({
                    "groupe": groupe,
                    "controle": code_controle,
                    "description": get_controle_description(code_controle),
                    "priorite": "Élevée" if code_controle in ["A.5.1", "A.8.7"] else "Moyenne"
                })
    
    return ecarts[:5]  # Retourne les 5 premiers écarts

def generer_recommandations_prioritaires(evidence):
    """Génère des recommandations prioritaires"""
    return [
        "Implémenter les politiques de sécurité (A.5.1)",
        "Définir les rôles et responsabilités de sécurité (A.5.2)",
        "Mettre en place un programme de sensibilisation (A.6.3)",
        "Gérer les droits d'accès privilégiés (A.8.2)",
        "Protéger contre les codes malveillants (A.8.7)",
        "Gérer les vulnérabilités techniques (A.8.8)"
    ]

def generer_plan_amelioration(evidence):
    """Génère un plan d'amélioration"""
    return {
        "phase_1_30_jours": [
            "Créer la politique de sécurité de l'information",
            "Documenter les rôles et responsabilités",
            "Mettre en place la gestion des accès privilégiés"
        ],
        "phase_2_60_jours": [
            "Implémenter la protection anti-malware",
            "Démarrer le programme de sensibilisation",
            "Établir la gestion des vulnérabilités"
        ],
        "phase_3_90_jours": [
            "Auditer l'ensemble des contrôles",
            "Préparer la revue de direction",
            "Planifier la certification ISO 27001"
        ]
    }

def main():
    print("📊 Génération du rapport ISO 27001:2022...")
    print("🏗️ Structure: 4 groupes de contrôles (A.5, A.6, A.7, A.8)")
    
    # Charger les preuves
    try:
        with open('evidence/iso27001_2022_correct_evidence.json', 'r') as f:
            evidence = json.load(f)
    except FileNotFoundError:
        print("❌ Fichier de preuves non trouvé. Exécutez d'abord collect_evidence.py")
        return
    
    # Générer le rapport
    rapport = generate_iso27001_2022_report(evidence)
    
    # Sauvegarder les rapports
    os.makedirs('reports', exist_ok=True)
    
    with open('reports/iso27001_2022_correct_rapport.json', 'w') as f:
        json.dump(rapport, f, indent=2, ensure_ascii=False)
    
    # Générer le résumé exécutif
    generate_executive_summary(rapport)
    
    print("✅ Rapport ISO 27001:2022 généré!")
    print(f"🎯 Score global: {rapport['score_global']}%")
    print(f"📊 Groupes évalués: {len(rapport['evaluation_groupes'])}")
    print(f"⚠️ Écarts identifiés: {len(rapport['ecarts_principaux'])}")

def generate_executive_summary(rapport):
    """Génère un résumé exécutif"""
    with open('reports/iso27001_2022_correct_resume.md', 'w') as f:
        f.write("# Rapport de Conformité ISO 27001:2022\n\n")
        f.write("**Structure: 4 groupes de contrôles**\n\n")
        f.write(f"**Date**: {rapport['date_generation']}\n\n")
        
        f.write(f"## 🎯 Score Global: {rapport['score_global']}%\n\n")
        
        f.write("## 📊 Évaluation par Groupe\n\n")
        for groupe, details in rapport['evaluation_groupes'].items():
            statut_emoji = "✅" if details['statut'] == "Conforme" else "⚠️" if details['statut'] == "Partiellement conforme" else "❌"
            f.write(f"{statut_emoji} **{groupe}**: {details['score']}% ({details['controles_implementes']}/{details['total_controles']} contrôles)\n")
        
        f.write(f"\n## ⚠️ Écarts Prioritaires\n\n")
        for ecart in rapport['ecarts_principaux']:
            f.write(f"- **{ecart['controle']}**: {ecart['description']} ({ecart['priorite']})\n")
        
        f.write(f"\n## 🚀 Plan d'Amélioration\n\n")
        f.write("**Phase 1 (30 jours):**\n")
        for action in rapport['plan_amelioration']['phase_1_30_jours']:
            f.write(f"- {action}\n")

if __name__ == "__main__":
    main()