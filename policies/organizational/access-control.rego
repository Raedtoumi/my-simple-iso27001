package organizational.access_control

# A.5.1 - Politiques de sécurité
default security_policies_defined = false

security_policies_defined {
    input.policies.information_security_policy
    input.policies.access_control_policy
}

# A.5.2 - Rôles et responsabilités
default roles_responsibilities_defined = false

roles_responsibilities_defined {
    input.policies.total_policies >= 2
}

# A.5.3 - Séparation des fonctions
default segregation_of_duties = false

segregation_of_duties {
    input.github.access_control.collaborators_limited
    input.github.branch_protection.require_reviews
}

# A.5.7 - Renseignement sur les menaces
default threat_intelligence = false

threat_intelligence {
    input.github.security_features.code_scanning
    input.github.security_features.dependabot
}

# A.5.15 - Règles de contrôle d'accès
default access_control_rules = false

access_control_rules {
    input.policies.access_control_policy
    input.github.branch_protection.main
}

# Score organisationnel
organizational_score = score {
    controls := [
        security_policies_defined,
        roles_responsibilities_defined,
        segregation_of_duties,
        threat_intelligence,
        access_control_rules
    ]
    implemented := count([c | c := controls[_]; c == true])
    score := (implemented / count(controls)) * 100
}