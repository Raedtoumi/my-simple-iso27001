package technological.github

# A.8.2 - Droits d'accès privilégiés
default privileged_access_controlled = false

privileged_access_controlled {
    input.github.access_control.admin_access_restricted
    input.github.access_control.collaborators_limited
}

# A.8.7 - Protection contre les codes malveillants
default malware_protection_enabled = false

malware_protection_enabled {
    input.github.security_features.code_scanning
    input.github.security_features.secret_scanning
}

# A.8.8 - Gestion des vulnérabilités techniques
default vulnerability_management_enabled = false

vulnerability_management_enabled {
    input.github.security_features.dependabot
}

# A.8.11 - Surveillance des systèmes
default monitoring_enabled = false

monitoring_enabled {
    input.security.monitoring.audit_logs
    input.security.monitoring.security_events
}

# A.8.26 - Gestion des changements
default change_management_enabled = false

change_management_enabled {
    input.github.branch_protection.require_reviews
    input.github.branch_protection.require_checks
}

# Score de sécurité technologique
github_security_score = score {
    controls := [
        privileged_access_controlled,
        malware_protection_enabled,
        vulnerability_management_enabled,
        monitoring_enabled,
        change_management_enabled
    ]
    implemented := count([c | c := controls[_]; c == true])
    score := (implemented / count(controls)) * 100
}