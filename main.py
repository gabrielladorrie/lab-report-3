

import json
from pathlib import Path

# Load JSON rules from the same folder as main.py
current_folder = Path(__file__).parent
json_file = current_folder / "scholarship_rules.json"

with open(json_file, "r", encoding="utf-8") as file:
    rules = json.load(file)

print("Scholarship rules loaded successfully!")
print("Total rules:", len(rules))


# Check individual conditions
def check_condition(applicant, condition):
    field, operator, value = condition

    if operator == ">=":
        return applicant[field] >= value
    elif operator == "<=":
        return applicant[field] <= value
    elif operator == "==":
        return applicant[field] == value
    elif operator == "<":
        return applicant[field] < value

    return False


# Scholarship evaluation system
def evaluate_scholarship(applicant):

    sorted_rules = sorted(
        rules,
        key=lambda rule: rule["priority"],
        reverse=True
    )

    for rule in sorted_rules:

        if all(
            check_condition(applicant, condition)
            for condition in rule["conditions"]
        ):

            return {
                "matched_rule": rule["name"],
                "decision": rule["action"]["decision"],
                "reason": rule["action"]["reason"]
            }

    return {
        "matched_rule": "No matching rule",
        "decision": "NO_DECISION",
        "reason": "Applicant does not meet any scholarship criteria"
    }


# Applicant information
applicant = {
    "cgpa": 3.85,
    "co_curricular_score": 90,
    "family_income": 5000,
    "disciplinary_actions": 0
}


# Display scholarship result
result = evaluate_scholarship(applicant)

print("\n===== SCHOLARSHIP ADVISORY SYSTEM =====")
print("Applicant:", applicant)
print("Matched Rule:", result["matched_rule"])
print("Decision:", result["decision"])
print("Reason:", result["reason"])
