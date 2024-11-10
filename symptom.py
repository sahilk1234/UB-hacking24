symptoms_conditions = {
    "fever": ["Cold", "Flu", "COVID-19"],
    "headache": ["Migraine", "Tension Headache", "Sinusitis"],
    # Extend with more symptoms and conditions
}

def get_possible_conditions(symptoms):
    conditions = set()
    for symptom in symptoms:
        conditions.update(symptoms_conditions.get(symptom, []))
    return list(conditions)
