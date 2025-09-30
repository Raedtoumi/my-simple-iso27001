package people.awareness

# A.6.3 - Sensibilisation, éducation et formation
default security_awareness = false

security_awareness {
    input.system.has_readme
    input.policies.total_policies >= 1
}

# A.6.7 - Travail à distance
default remote_working_security = false

remote_working_security {
    input.security.authentication.mfa_configured
    input.security.encryption.https_enforced
}

# A.6.8 - Signalement des événements de sécurité
default security_incident_reporting = false

security_incident_reporting {
    input.system.has_github_actions
    input.security.monitoring.security_events
}

# Score personnes
people_score = score {
    controls := [
        security_awareness,
        remote_working_security,
        security_incident_reporting
    ]
    implemented := count([c | c := controls[_]; c == true])
    score := (implemented / count(controls)) * 100
}