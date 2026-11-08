
import streamlit as st
import json
from pathlib import Path

# =====================================
# 1. LOAD SCHOLARSHIP RULES FROM JSON
# =====================================

current_folder = Path(__file__).parent
json_file = current_folder / "scholarship_rules.json"

with open(json_file, "r", encoding="utf-8") as file:
    rules = json.load(file)


# =====================================
# 2. STREAMLIT INTERFACE
# =====================================

st.set_page_config(
    page_title="Scholarship Advisory System",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Scholarship Advisory System")

st.write(
    "A Rule-Based System for Scholarship Eligibility Evaluation"
)

st.success("Scholarship rules loaded successfully!")

st.write("Total rules:", len(rules))

st.divider()


# =====================================
# 3. APPLICANT INFORMATION
# =====================================

st.subheader("Applicant Information")

cgpa = st.number_input(
    "CGPA",
    min_value=0.0,
    max_value=4.0,
    value=3.85,
    step=0.01
)

co_curricular_score = st.number_input(
    "Co-curricular Score",
    min_value=0,
    max_value=100,
    value=90
)

family_income = st.number_input(
    "Family Monthly Income (RM)",
    min_value=0,
    value=5000
)

disciplinary_actions = st.number_input(
    "Number of Disciplinary Actions",
    min_value=0,
    value=0
)


# =====================================
# 4. CONDITION CHECKING
# =====================================

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


# =====================================
# 5. SCHOLARSHIP EVALUATION
# =====================================

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


# =====================================
# 6. EVALUATE BUTTON
# =====================================

if st.button("Evaluate Scholarship", type="primary"):

    applicant = {
        "cgpa": cgpa,
        "co_curricular_score": co_curricular_score,
        "family_income": family_income,
        "disciplinary_actions": disciplinary_actions
    }

    result = evaluate_scholarship(applicant)

    st.divider()

    st.subheader("Scholarship Evaluation Result")

    st.write("Applicant Information:")
    st.json(applicant)

    st.write("Matched Rule:", result["matched_rule"])

    decision = result["decision"]

    if decision == "AWARD_FULL":
        st.success("🎉 FULL SCHOLARSHIP")

    elif decision == "AWARD_PARTIAL":
        st.success("PARTIAL SCHOLARSHIP")

    elif decision == "REVIEW":
        st.warning("APPLICATION REQUIRES REVIEW")

    elif decision == "REJECT":
        st.error("APPLICATION REJECTED")

    else:
        st.info("NO DECISION")

    st.write("**Reason:**")
    st.info(result["reason"])


# =====================================
# 7. DISPLAY ALL SCHOLARSHIP RULES
# =====================================

with st.expander("View All Scholarship Rules"):

    for rule in rules:

        st.write("**Rule:**", rule["name"])
        st.write("**Priority:**", rule["priority"])
        st.write("**Conditions:**", rule["conditions"])
        st.write("**Decision:**", rule["action"]["decision"])
        st.write("**Reason:**", rule["action"]["reason"])

        st.divider()
