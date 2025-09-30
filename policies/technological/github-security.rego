package technological.github

# A.8.7 - Protection contre les codes malveillants
default malware_protection_enabled = false

malware_protection_enabled {
    input.github.security_features.code_scanning
}

# A.8.8 - Gestion des vulnérabilités techniques
default vulnerability_management_enabled = false

vulnerability_management_enabled {
    input.github.security_features.dependabot
}

# Score technologique - NOM IMPORTANT!
github_security_score = score {
    controls := [
        malware_protection_enabled,
        vulnerability_management_enabled
    ]
    implemented := count([c | c := controls[_]; c == true])
    score := (implemented / count(controls)) * 100
}