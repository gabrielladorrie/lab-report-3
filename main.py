
import json
import operator
import streamlit as st
import pandas as pd

from typing import List, Dict, Any, Tuple


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Scholarship Advisory System",
    page_icon="🎓",
    layout="wide"
)


# ==========================================
# 2. APPLICATION HEADER
# ==========================================

st.title("🎓 Scholarship Advisory System")

st.write(
    "A Rule-Based Expert System for evaluating "
    "university scholarship applications."
)

st.caption(
    "Python Knowledge Representation System | "
    "Rule-Based Expert System"
)

st.divider()


# ==========================================
# 3. RULE ENGINE OPERATORS
# ==========================================

OPS = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
    "in": lambda a, b: a in b,
    "not_in": lambda a, b: a not in b,
}


# ==========================================
# 4. DEFAULT SCHOLARSHIP RULES
# ==========================================

DEFAULT_RULES: List[Dict[str, Any]] = [

    {
        "name": "Top merit candidate",
        "priority": 100,

        "conditions": [
            ["cgpa", ">=", 3.7],
            ["co_curricular_score", ">=", 80],
            ["family_income", "<=", 8000],
            ["disciplinary_actions", "==", 0]
        ],

        "action": {
            "decision": "AWARD_FULL",
            "reason": "Excellent academic & co-curricular performance, with acceptable need"
        }
    },

    {
        "name": "Good candidate - partial scholarship",
        "priority": 80,

        "conditions": [
            ["cgpa", ">=", 3.3],
            ["co_curricular_score", ">=", 60],
            ["family_income", "<=", 12000],
            ["disciplinary_actions", "<=", 1]
        ],

        "action": {
            "decision": "AWARD_PARTIAL",
            "reason": "Good academic & involvement record with moderate need"
        }
    },

    {
        "name": "Need-based review",
        "priority": 70,

        "conditions": [
            ["cgpa", ">=", 2.5],
            ["family_income", "<=", 4000]
        ],

        "action": {
            "decision": "REVIEW",
            "reason": "High need but borderline academic score"
        }
    },

    {
        "name": "Low CGPA – not eligible",
        "priority": 95,

        "conditions": [
            ["cgpa", "<", 2.5]
        ],

        "action": {
            "decision": "REJECT",
            "reason": "CGPA below minimum scholarship requirement"
        }
    },

    {
        "name": "Serious disciplinary record",
        "priority": 90,

        "conditions": [
            ["disciplinary_actions", ">=", 2]
        ],

        "action": {
            "decision": "REJECT",
            "reason": "Too many disciplinary records"
        }
    },

]


# ==========================================
# 5. SESSION STATE INITIALIZATION
# ==========================================

if "json_rules" not in st.session_state:

    st.session_state.json_rules = json.dumps(
        DEFAULT_RULES,
        indent=2,
        ensure_ascii=False
    )


if "edit_mode" not in st.session_state:

    st.session_state.edit_mode = False


if "edit_json" not in st.session_state:

    st.session_state.edit_json = st.session_state.json_rules


if "evaluation_result" not in st.session_state:

    st.session_state.evaluation_result = None


if "rules_saved" not in st.session_state:

    st.session_state.rules_saved = False


# ==========================================
# 6. CONDITION EVALUATION
# ==========================================

def evaluate_condition(
    facts: Dict[str, Any],
    cond: List[Any]
) -> bool:

    """
    Evaluate a single condition:
    [attribute, operator, value]
    """

    if not isinstance(cond, list) or len(cond) != 3:
        raise ValueError("Invalid condition format.")

    field, op, value = cond

    if field not in facts:
        raise ValueError(
            f"Unknown student attribute: {field}"
        )

    if op not in OPS:
        raise ValueError(
            f"Unsupported operator: {op}"
        )

    try:

        return OPS[op](facts[field], value)

    except (TypeError, ValueError) as error:

        raise ValueError(
            f"Cannot evaluate condition: {cond}"
        ) from error


# ==========================================
# 7. RULE MATCHING
# ==========================================

def rule_matches(
    facts: Dict[str, Any],
    rule: Dict[str, Any]
) -> bool:

    """
    All conditions must be true (AND).
    """

    conditions = rule.get("conditions", [])

    return all(
        evaluate_condition(facts, condition)
        for condition in conditions
    )


# ==========================================
# 8. RULE-BASED INFERENCE ENGINE
# ==========================================

def run_rules(
    facts: Dict[str, Any],
    rules: List[Dict[str, Any]]
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:

    """
    Returns:
        best_action: Decision from the highest-priority rule.
        fired_rules: All matching rules sorted by priority.
    """

    # Find all rules that match the student information

    fired = [
        rule
        for rule in rules
        if rule_matches(facts, rule)
    ]

    # No matching rules

    if not fired:

        return (
            {
                "decision": "NOT QUALIFIED",
                "reason": "No scholarship rules were satisfied."
            },
            []
        )

    # Sort matching rules by highest priority

    fired_sorted = sorted(
        fired,
        key=lambda rule: rule["priority"],
        reverse=True
    )

    # Select the highest-priority rule

    best_rule = fired_sorted[0]

    best_action = best_rule["action"]

    return best_action, fired_sorted


# ==========================================
# 9. JSON VALIDATION
# ==========================================

def validate_rules(rules):

    """
    Validate JSON scholarship rules before saving.
    """

    if not isinstance(rules, list):

        raise ValueError(
            "Rules must be a JSON list."
        )

    if not rules:

        raise ValueError(
            "At least one scholarship rule is required."
        )

    required_attributes = {
        "cgpa": (0, 4),
        "co_curricular_score": (0, 100),
        "family_income": (0, float("inf")),
        "disciplinary_actions": (0, float("inf"))
    }

    rule_names = []

    for index, rule in enumerate(rules):

        if not isinstance(rule, dict):

            raise ValueError(
                f"Rule {index + 1} must be an object."
            )

        # Check required rule fields

        for key in ["name", "priority", "conditions", "action"]:

            if key not in rule:

                raise ValueError(
                    f"Rule {index + 1}: Missing field '{key}'."
                )

        # Validate rule name

        if (
            not isinstance(rule["name"], str)
            or not rule["name"].strip()
        ):

            raise ValueError(
                "Rule name must be non-empty text."
            )

        if rule["name"] in rule_names:

            raise ValueError(
                f"Duplicate rule name: {rule['name']}"
            )

        rule_names.append(rule["name"])

        # Validate priority

        priority = rule["priority"]

        if (
            isinstance(priority, bool)
            or not isinstance(priority, (int, float))
            or not __import__("math").isfinite(priority)
        ):

            raise ValueError(
                f"Priority of '{rule['name']}' must be numeric."
            )

        # Validate conditions

        if (
            not isinstance(rule["conditions"], list)
            or len(rule["conditions"]) == 0
        ):

            raise ValueError(
                f"'{rule['name']}' must contain at least one condition."
            )

        # Validate action

        action = rule["action"]

        if not isinstance(action, dict):

            raise ValueError(
                f"Action in '{rule['name']}' must be an object."
            )

        for key in ["decision", "reason"]:

            if key not in action:

                raise ValueError(
                    f"Missing action field: {key}"
                )

        if (
            not isinstance(action["decision"], str)
            or not action["decision"].strip()
        ):

            raise ValueError(
                "Decision must be non-empty text."
            )

        if not isinstance(action["reason"], str):

            raise ValueError(
                "Reason must be text."
            )

        # Validate individual conditions

        for condition in rule["conditions"]:

            if (
                not isinstance(condition, list)
                or len(condition) != 3
            ):

                raise ValueError(
                    "Each condition must contain "
                    "attribute, operator and value."
                )

            field, op, value = condition

            if field not in required_attributes:

                raise ValueError(
                    f"Unsupported attribute: {field}"
                )

            if op not in OPS:

                raise ValueError(
                    f"Unsupported operator: {op}"
                )

            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not __import__("math").isfinite(value)
            ):

                raise ValueError(
                    "Condition values must be numeric."
                )

            minimum, maximum = required_attributes[field]

            if not minimum <= value <= maximum:

                raise ValueError(
                    f"Invalid value for {field}."
                )

            if (
                field == "disciplinary_actions"
                and not float(value).is_integer()
            ):

                raise ValueError(
                    "Disciplinary actions must use whole numbers."
                )


# ==========================================
# 10. STUDENT INFORMATION INPUT
# ==========================================

st.header("1. Student Information")

st.write(
    "Enter the student's information to determine "
    "scholarship eligibility."
)

col1, col2 = st.columns(2)

with col1:

    student_id = st.text_input(
        "Student ID",
        value="STU001"
    )

    cgpa = st.number_input(
        "CGPA",
        min_value=0.0,
        max_value=4.0,
        value=3.80,
        step=0.01,
        format="%.2f"
    )

    co_curricular_score = st.number_input(
        "Co-curricular Score",
        min_value=0,
        max_value=100,
        value=85,
        step=1
    )


with col2:

    family_income = st.number_input(
        "Family Monthly Income (RM)",
        min_value=0,
        value=5000,
        step=100
    )

    disciplinary_actions = st.number_input(
        "Number of Disciplinary Actions",
        min_value=0,
        value=0,
        step=1
    )


# Store student facts

facts = {

    "cgpa": cgpa,

    "co_curricular_score": co_curricular_score,

    "family_income": family_income,

    "disciplinary_actions": disciplinary_actions

}


# ==========================================
# 11. KNOWLEDGE BASE
# ==========================================

st.divider()

st.header("2. Knowledge Base")

st.write(
    "The knowledge base stores the scholarship rules "
    "used by the inference engine."
)


# ------------------------------------------
# DEFAULT VIEW: DISPLAY RULES AS TABLE
# ------------------------------------------

if not st.session_state.edit_mode:

    try:

        rules = json.loads(
            st.session_state.json_rules
        )

        validate_rules(rules)

        rules_data = []

        for rule in rules:

            conditions_text = " AND ".join(
                [
                    f"{condition[0]} {condition[1]} {condition[2]}"
                    for condition in rule["conditions"]
                ]
            )

            rules_data.append({

                "Rule Name": rule["name"],

                "Priority": rule["priority"],

                "Conditions": conditions_text,

                "Decision": rule["action"]["decision"],

                "Reason": rule["action"]["reason"]

            })

        df_rules = pd.DataFrame(rules_data)

        st.subheader("Scholarship Rules")

        st.dataframe(
            df_rules,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Total scholarship rules: {len(rules)}"
        )

    except (json.JSONDecodeError, ValueError, KeyError) as error:

        st.error(
            f"Knowledge base error: {error}"
        )

    # Open JSON editor

    if st.button(
        "✏️ Edit JSON Rules",
        use_container_width=True
    ):

        st.session_state.edit_json = (
            st.session_state.json_rules
        )

        st.session_state.edit_mode = True

        st.rerun()


# ------------------------------------------
# EDIT VIEW: JSON EDITOR
# ------------------------------------------

else:

    st.subheader("Edit Scholarship Rules")

    st.info(
        "You can modify the scholarship rules below. "
        "The system will validate the JSON before saving."
    )

    json_input = st.text_area(
        "Scholarship Rules (JSON Editor)",
        key="edit_json",
        height=450
    )

    col1, col2 = st.columns(2)

    # SAVE CHANGES

    with col1:

        if st.button(
            "💾 Save Changes",
            use_container_width=True
        ):

            try:

                edited_rules = json.loads(
                    json_input
                )

                validate_rules(edited_rules)

                st.session_state.json_rules = json.dumps(
                    edited_rules,
                    indent=2,
                    ensure_ascii=False
                )

                st.session_state.edit_mode = False

                st.session_state.evaluation_result = None

                st.session_state.rules_saved = True

                st.rerun()

            except (
                json.JSONDecodeError,
                ValueError,
                KeyError,
                TypeError
            ) as error:

                st.error(
                    f"Invalid JSON rules: {error}"
                )

    # CANCEL EDITING

    with col2:

        if st.button(
            "↩️ Cancel Editing",
            use_container_width=True
        ):

            st.session_state.edit_mode = False

            st.rerun()


if st.session_state.rules_saved:

    st.success(
        "Scholarship rules saved successfully!"
    )

    st.session_state.rules_saved = False


# ==========================================
# 12. SCHOLARSHIP EVALUATION
# ==========================================

st.divider()

st.header("3. Scholarship Evaluation")

st.write(
    "Click the button below to evaluate the student's "
    "scholarship eligibility using the inference engine."
)


if st.button(
    "🎓 Evaluate Scholarship Application",
    type="primary",
    use_container_width=True
):

    if not student_id.strip():

        st.error(
            "Please enter a valid Student ID."
        )

        st.session_state.evaluation_result = None

    else:

        try:

            # Load saved JSON rules

            rules = json.loads(
                st.session_state.json_rules
            )

            validate_rules(rules)

            # Run inference engine

            action, fired_rules = run_rules(
                facts,
                rules
            )

            # Store evaluation result

            st.session_state.evaluation_result = {

                "student_id": student_id.strip(),

                "facts": facts.copy(),

                "action": action,

                "fired_rules": fired_rules

            }

        except (
            json.JSONDecodeError,
            ValueError,
            KeyError,
            TypeError
        ) as error:

            st.error(
                f"Evaluation error: {error}"
            )

            st.session_state.evaluation_result = None


# ==========================================
# 13. DISPLAY EVALUATION RESULTS
# ==========================================

if st.session_state.evaluation_result is not None:

    evaluation = st.session_state.evaluation_result

    action = evaluation["action"]

    fired_rules = evaluation["fired_rules"]

    decision = action["decision"]

    st.divider()

    st.subheader("📋 Evaluation Result")


    # --------------------------------------
    # STUDENT INFORMATION
    # --------------------------------------

    st.markdown("#### Student Information")

    student_data = pd.DataFrame([{

        "Student ID": evaluation["student_id"],

        "CGPA": evaluation["facts"]["cgpa"],

        "Co-curricular Score": evaluation["facts"]["co_curricular_score"],

        "Family Income (RM)": evaluation["facts"]["family_income"],

        "Disciplinary Actions": evaluation["facts"]["disciplinary_actions"]

    }])

    st.dataframe(
        student_data,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------
    # SCHOLARSHIP DECISION
    # --------------------------------------

    st.markdown("#### Final Scholarship Decision")

    if decision == "AWARD_FULL":

        st.success(
            "🎉 FULL SCHOLARSHIP AWARDED"
        )

    elif decision == "AWARD_PARTIAL":

        st.success(
            "🎓 PARTIAL SCHOLARSHIP AWARDED"
        )

    elif decision == "REVIEW":

        st.warning(
            "⚠️ APPLICATION REQUIRES REVIEW"
        )

    elif decision == "REJECT":

        st.error(
            "❌ SCHOLARSHIP APPLICATION REJECTED"
        )

    else:

        st.info(
            "No matching scholarship rule found."
        )


    # --------------------------------------
    # DECISION DETAILS
    # --------------------------------------

    result_col1, result_col2 = st.columns(2)

    with result_col1:

        st.metric(
            "Scholarship Decision",
            decision
        )

        if fired_rules:

            st.write(
                "**Selected Rule:**",
                fired_rules[0]["name"]
            )

        else:

            st.write(
                "**Selected Rule:** No matching rule"
            )


    with result_col2:

        if fired_rules:

            st.metric(
                "Rule Priority",
                fired_rules[0]["priority"]
            )

        else:

            st.metric(
                "Rule Priority",
                "N/A"
            )

        st.write(
            "**Reason:**",
            action["reason"]
        )


    # --------------------------------------
    # MATCHING RULES
    # --------------------------------------

    st.markdown("#### Matching Rules")

    if fired_rules:

        matching_data = []

        for rule in fired_rules:

            matching_data.append({

                "Rule Name": rule["name"],

                "Priority": rule["priority"],

                "Decision": rule["action"]["decision"],

                "Reason": rule["action"]["reason"]

            })

        matching_df = pd.DataFrame(
            matching_data
        )

        st.dataframe(
            matching_df,
            use_container_width=True,
            hide_index=True
        )

        st.info(
            "The inference engine selects the matching rule "
            "with the highest priority."
        )


        # ----------------------------------
        # EXPLANATION OF SELECTED RULE
        # ----------------------------------

        st.markdown(
            "#### Explanation of Selected Rule"
        )

        selected_rule = fired_rules[0]

        st.write(
            f"The system selected **{selected_rule['name']}** "
            f"because all its conditions were satisfied."
        )

        for condition in selected_rule["conditions"]:

            field, op, value = condition

            student_value = facts[field]

            st.write(
                f"✅ {field}: {student_value} "
                f"{op} {value}"
            )


    else:

        st.warning(
            "No scholarship rules matched the student's information."
        )


# ==========================================
# 14. FOOTER
# ==========================================

st.divider()

st.caption(
    "Scholarship Advisory System | "
    "Python Knowledge Representation | "
    "Rule-Based Expert System"
)
