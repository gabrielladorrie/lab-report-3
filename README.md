# Scholarship Advisory System

A **rule-based expert system** that evaluates university scholarship applications using student information and a knowledge base of scholarship rules. The inference engine checks which rules match the student's information and selects the matching rule with the highest priority.

## Features

- Collects student details, including student ID, CGPA, co-curricular score, family monthly income, and disciplinary actions.
- Stores scholarship eligibility rules in a knowledge base.
- Uses rule priorities to resolve cases where more than one rule matches.
- Displays the final scholarship decision, the selected rule, its priority, and the reason for the decision.
- Shows which conditions were satisfied so the result is understandable.

## System Screenshots and Interpretation

### 1. Student Information

![Student information form](images/01-student-information.png)

This section is where the applicant's information is entered. The example uses student ID `STU001`, CGPA `3.80`, co-curricular score `85`, family monthly income of RM 5,000, and zero disciplinary actions. These values are passed to the inference engine for evaluation.

### 2. Knowledge Base – Scholarship Rules

![Scholarship rules in the knowledge base](images/02-knowledge-base-rules.png)

The knowledge base contains five rules. Each rule has a name, priority, conditions, decision, and explanation:

| Rule | Priority | Condition / purpose | Decision |
|---|---:|---|---|
| Top merit candidate | 100 | High CGPA and co-curricular score, income within the stated limit, and an acceptable disciplinary record | `AWARD_FULL` |
| Good candidate – partial scholarship | 80 | Good academic performance and involvement, with a higher income limit than the full-scholarship rule | `AWARD_PARTIAL` |
| Need-based review | 70 | CGPA of at least 2.5 and family income of RM 4,000 or less | `REVIEW` |
| Low CGPA – not eligible | 95 | CGPA below 2.5 | `REJECT` |
| Serious disciplinary record | 90 | Two or more disciplinary actions | `REJECT` |

The priority value determines which rule wins when multiple rules match. A higher priority is selected over a lower-priority matching rule.

### 3. Scholarship Evaluation Result

![Scholarship evaluation and result](images/03-scholarship-evaluation.png)

After the user clicks **Evaluate Scholarship Application**, the system evaluates the entered student details. The result table confirms the values used for the decision. In this example, the system displays **FULL SCHOLARSHIP AWARDED** with the decision code `AWARD_FULL`.

### 4. Explanation of the Selected Rule

![Selected rule and satisfied conditions](images/04-selected-rule-explanation.png)

The system selects **Top merit candidate** with priority **100**. All four conditions shown in the result are satisfied:

- CGPA: `3.8 >= 3.7`
- Co-curricular score: `85 >= 80`
- Family income: `RM 5,000 <= RM 8,000`
- Disciplinary actions: `0 == 0`

The full-scholarship rule therefore matches this student's information. Its priority of 100 is higher than the partial-scholarship rule's priority of 80, so the inference engine selects `AWARD_FULL`.

## Example Result Summary

| Student detail | Example value |
|---|---:|
| Student ID | STU001 |
| CGPA | 3.80 |
| Co-curricular score | 85 |
| Family monthly income | RM 5,000 |
| Disciplinary actions | 0 |
| Final decision | **Full scholarship (`AWARD_FULL`)** |
| Selected rule | Top merit candidate |
| Rule priority | 100 |

**Interpretation:** The example student qualifies for a full scholarship because the academic, co-curricular, family-income, and disciplinary requirements of the top-merit rule are all met. The system provides both the decision and the conditions behind it, making the evaluation transparent and explainable.

## How the System Works

1. The user enters the student's information.
2. The inference engine compares the information with the conditions stored in the knowledge base.
3. The system identifies all rules whose conditions are satisfied.
4. It selects the matching rule with the highest priority.
5. It displays the scholarship decision and an explanation of the selected rule.

## Technology / Project Type

- **Language:** Python
- **Approach:** Knowledge representation and rule-based expert system
- **Main components:** Student information input, knowledge base, inference engine, and evaluation result display

## Project Note

The screenshots show an example evaluation, not a guarantee of an actual university scholarship award. The final outcome depends on the rules and values configured in the application.
