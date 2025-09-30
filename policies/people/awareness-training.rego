package people.awareness

# A.6.3 - Sensibilisation, éducation et formation
default security_awareness = false

security_awareness {
    input.system.has_readme
}

# Score personnes - NOM IMPORTANT!
awareness_score = score {
    security_awareness == true
    score := 100
} else := 0