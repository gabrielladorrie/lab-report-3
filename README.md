# 🎓 Scholarship Advisory System

## 1. Project Overview

The **Scholarship Advisory System** is a rule-based expert system developed using Python and Streamlit. It assists universities in evaluating students' eligibility for scholarships based on academic performance, co-curricular involvement, family income, and disciplinary records.

The system uses a JSON-based knowledge base containing predefined scholarship rules. Based on the information entered by the user, the inference engine evaluates the rules and recommends an appropriate scholarship decision.

## 2. Project Objectives

The objectives of this project are to:

- Develop a rule-based system for scholarship advisory.
- Represent scholarship eligibility knowledge using JSON rules.
- Apply an inference engine to evaluate student information.
- Determine the most suitable scholarship decision based on rule priorities.
- Provide an interactive interface for users to enter student information and view evaluation results.
- Allow users to view and edit the scholarship rules through the JSON editor.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Development of the web application interface |
| Pandas | Displaying scholarship rules in table format |
| JSON | Representing and storing the knowledge base |
| Operator | Evaluating logical comparison conditions |

## 4. Scholarship Eligibility Criteria

The system evaluates students based on four main criteria:

1. **CGPA** – Student's academic performance.
2. **Co-curricular Score** – Student's participation and involvement in co-curricular activities.
3. **Family Income** – Student's monthly family income in RM.
4. **Disciplinary Actions** – Number of disciplinary records.

## 5. Knowledge Base

The knowledge base consists of five predefined scholarship rules.

| Rule Name | Priority | Decision |
|---|---:|---|
| Top merit candidate | 100 | AWARD_FULL |
| Good candidate - partial scholarship | 80 | AWARD_PARTIAL |
| Need-based review | 70 | REVIEW |
| Low CGPA – not eligible | 95 | REJECT |
| Serious disciplinary record | 90 | REJECT |

Each rule contains:
- **Name:** Identifies the scholarship rule.
- **Priority:** Determines which rule takes precedence when multiple rules match.
- **Conditions:** Specifies the eligibility requirements.
- **Action:** Defines the scholarship decision and its reason.

The system evaluates all applicable conditions in a rule. If multiple rules match, the rule with the highest priority determines the final decision.

## 6. Main Features

- **Student Information Input:** Allows users to enter student details.
- **Knowledge Base Display:** Displays the scholarship rules in a table.
- **JSON Rule Editor:** Allows users to view and modify the rules when necessary.
- **Rule Validation:** Checks whether edited JSON rules have a valid structure and acceptable values.
- **Inference Engine:** Evaluates student information against the scholarship rules.
- **Priority-Based Decision:** Selects the matching rule with the highest priority.
- **Evaluation Results:** Displays the scholarship decision, selected rule, priority, and explanation.

## 7. Scholarship Decisions

The system can produce the following decisions:

| Decision | Description |
|---|---|
| AWARD_FULL | Student qualifies for a full scholarship. |
| AWARD_PARTIAL | Student qualifies for a partial scholarship. |
| REVIEW | Student requires further consideration. |
| REJECT | Student does not meet the scholarship requirements. |
| NOT QUALIFIED | No scholarship rule matches the student's information. |

## 8. How to Use the System

1. Run the Streamlit application.
2. Enter the student's information, including student ID, CGPA, co-curricular score, family income, and disciplinary actions.
3. View the predefined scholarship rules in the Knowledge Base section.
4. Select **Edit JSON Rules** if you want to modify the rules.
5. Save the changes after editing the JSON rules.
6. Click the evaluation button to evaluate the student's scholarship eligibility.
7. View the final scholarship decision and the explanation provided by the system.

## 9. Example Evaluation

The following is an example of student information entered into the system:

| Student Information | Value |
|---|---:|
| Student ID | STU001 |
| CGPA | 3.80 |
| Co-curricular Score | 85 |
| Family Monthly Income | RM5,000 |
| Disciplinary Actions | 0 |

**Expected Result: AWARD_FULL**

The student satisfies all conditions under the *Top merit candidate* rule. Since this rule has the highest priority of 100, the system recommends awarding a full scholarship.

## 10. Conclusion

The Scholarship Advisory System demonstrates how a rule-based expert system can support university scholarship decision-making. By using a JSON-based knowledge base and a priority-based inference engine, the system evaluates student eligibility and provides consistent scholarship recommendations. The interactive Streamlit interface also allows users to view and modify scholarship rules conveniently.

---

**Developed using Python and Streamlit.**
