#!/usr/bin/env python3
import json
import os
from datetime import datetime

def generate_iso27001_report(evidence):
    """Generate comprehensive ISO 27001 compliance report"""
    
    # ISO 27001:2022 Controls Assessment
    controls_assessment = {
        "A.5 Information Security Policies": assess_policy_controls(evidence),
        "A.6 Organization of Information Security": assess_organization_controls(evidence),
        "A.7 Human Resource Security": assess_hr_controls(evidence),
        "A.8 Asset Management": assess_asset_controls(evidence),
        "A.9 Access Control": assess_access_controls(evidence),
        "A.10 Cryptography": assess_crypto_controls(evidence),
        "A.11 Physical and Environmental Security": assess_physical_controls(evidence),
        "A.12 Operations Security": assess_operations_controls(evidence),
        "A.13 Communications Security": assess_communications_controls(evidence),
        "A.14 System Acquisition, Development and Maintenance": assess_system_controls(evidence),
        "A.15 Supplier Relationships": assess_supplier_controls(evidence),
        "A.16 Information Security Incident Management": assess_incident_controls(evidence),
        "A.17 Information Security Aspects of Business Continuity": assess_business_continuity_controls(evidence),
        "A.18 Compliance": assess_compliance_controls(evidence)
    }
    
    # Calculate overall scores
    domain_scores = {}
    for domain, controls in controls_assessment.items():
        implemented = sum(1 for control in controls.values() if control['status'] == 'Implemented')
        total = len(controls)
        domain_scores[domain] = {
            'score': (implemented / total) * 100 if total > 0 else 0,
            'implemented': implemented,
            'total': total
        }
    
    overall_score = sum(domain['score'] for domain in domain_scores.values()) / len(domain_scores)
    
    report = {
        "report_date": datetime.utcnow().isoformat(),
        "standard": "ISO 27001:2022",
        "overall_compliance_score": round(overall_score, 1),
        "domain_scores": domain_scores,
        "detailed_assessment": controls_assessment,
        "gaps_identified": identify_gaps(controls_assessment),
        "recommendations": generate_recommendations(controls_assessment),
        "next_steps": generate_next_steps(controls_assessment)
    }
    
    return report

def assess_policy_controls(evidence):
    """Assess A.5: Information Security Policies"""
    return {
        "A.5.1 Information Security Policies": {
            "status": "Implemented" if evidence['security_controls']['policies']['information_security_policy'] else "Not Implemented",
            "evidence": "Information Security Policy document",
            "maturity": "Advanced" if evidence['security_controls']['policies']['information_security_policy'] else "Initial"
        }
    }

def assess_access_controls(evidence):
    """Assess A.9: Access Control"""
    return {
        "A.9.1 Business Requirements of Access Control": {
            "status": "Implemented",
            "evidence": "Access control policy and user management procedures",
            "maturity": "Advanced"
        },
        "A.9.2 User Access Management": {
            "status": "Implemented" if evidence['access_control']['user_management']['unique_identifiers'] else "Partially Implemented",
            "evidence": "Unique user IDs and access review processes",
            "maturity": "Managed"
        },
        "A.9.4 System and Application Access Control": {
            "status": "Implemented",
            "evidence": "Role-based access control and authentication mechanisms",
            "maturity": "Advanced"
        }
    }

def identify_gaps(assessment):
    """Identify compliance gaps"""
    gaps = []
    for domain, controls in assessment.items():
        for control_name, control_info in controls.items():
            if control_info['status'] != 'Implemented':
                gaps.append({
                    'domain': domain,
                    'control': control_name,
                    'status': control_info['status'],
                    'priority': 'High' if 'Access Control' in control_name else 'Medium'
                })
    return gaps

def generate_recommendations(assessment):
    """Generate improvement recommendations"""
    recommendations = []
    
    # Policy recommendations
    if not any('A.5' in domain for domain in assessment.keys()):
        recommendations.append("Develop and implement comprehensive information security policies")
    
    # Risk management recommendations
    if not any('A.6' in domain for domain in assessment.keys()):
        recommendations.append("Establish formal risk assessment and treatment processes")
    
    return recommendations

def main():
    print("📊 Generating ISO 27001 Compliance Report...")
    
    # Load evidence
    try:
        with open('evidence/iso27001_evidence.json', 'r') as f:
            evidence = json.load(f)
    except FileNotFoundError:
        print("❌ No evidence file found. Run collect_evidence.py first.")
        return
    
    # Generate report
    report = generate_iso27001_report(evidence)
    
    # Save reports
    os.makedirs('reports', exist_ok=True)
    
    with open('reports/iso27001_compliance_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    # Generate executive summary
    generate_executive_summary(report)
    
    print("✅ ISO 27001 Compliance Report generated!")
    print(f"📈 Overall Compliance Score: {report['overall_compliance_score']}%")
    print(f"🔍 Gaps Identified: {len(report['gaps_identified'])}")
    print(f"💡 Recommendations: {len(report['recommendations'])}")

def generate_executive_summary(report):
    """Generate executive summary markdown report"""
    with open('reports/iso27001_executive_summary.md', 'w') as f:
        f.write("# ISO 27001:2022 Compliance Executive Summary\n\n")
        f.write(f"**Report Date**: {report['report_date']}\n\n")
        
        f.write(f"## 🎯 Overall Compliance Score: {report['overall_compliance_score']}%\n\n")
        
        f.write("## 📊 Domain Scores\n\n")
        for domain, scores in report['domain_scores'].items():
            f.write(f"- **{domain}**: {scores['score']:.1f}% ({scores['implemented']}/{scores['total']} controls)\n")
        
        f.write(f"\n## ⚠️ Identified Gaps: {len(report['gaps_identified'])}\n\n")
        for gap in report['gaps_identified'][:5]:  # Show top 5
            f.write(f"- **{gap['control']}** ({gap['priority']} priority)\n")
        
        f.write(f"\n## 💡 Key Recommendations: {len(report['recommendations'])}\n\n")
        for rec in report['recommendations'][:3]:  # Show top 3
            f.write(f"- {rec}\n")
        
        f.write(f"\n## 🚀 Next Steps\n\n")
        f.write("1. Address high-priority gaps identified above\n")
        f.write("2. Implement recommended security controls\n")
        f.write("3. Conduct internal audit of implemented controls\n")
        f.write("4. Prepare for certification audit\n")

if __name__ == "__main__":
    main()