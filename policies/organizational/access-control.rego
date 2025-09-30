package organizational.access_control

# A.5.1 - Politiques de sécurité
default security_policies_defined = false

security_policies_defined {
    input.policies.information_security_policy
}

# A.5.2 - Rôles et responsabilités  
default roles_responsibilities_defined = false

roles_responsibilities_defined {
    input.policies.total_policies >= 2
}

# Score organisationnel - NOM IMPORTANT!
access_control_score = score {
    controls := [
        security_policies_defined,
        roles_responsibilities_defined
    ]
    implemented := count([c | c := controls[_]; c == true])
    score := (implemented / count(controls)) * 100
}