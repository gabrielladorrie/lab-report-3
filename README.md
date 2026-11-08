# 🎓 Scholarship Advisory System

## 1. Project Overview

The **Scholarship Advisory System** is a Python-based Rule-Based Expert System designed to evaluate university students' eligibility for scholarships.

The system uses a Knowledge Base containing predefined scholarship rules and an Inference Engine to analyse student information and determine whether a student qualifies for a full scholarship, partial scholarship, further review, or rejection.

The main purpose of this system is to provide consistent, transparent, and efficient scholarship decisions.

## 2. Project Objectives

- To develop a rule-based expert system for scholarship evaluation.
- To represent scholarship eligibility criteria using a Knowledge Base.
- To apply an Inference Engine to evaluate student information.
- To determine scholarship eligibility based on predefined conditions.
- To provide clear explanations for the final scholarship decisions.

## 3. System Features

The system consists of three main components:

### 3.1 Student Information

Users can enter the following student details:

- Student ID
- CGPA
- Co-curricular Score
- Family Monthly Income (RM)
- Number of Disciplinary Actions

### 3.2 Knowledge Base

The Knowledge Base stores five predefined scholarship rules:

| Rule Name | Priority | Decision |
|---|---:|---|
| Top merit candidate | 100 | AWARD_FULL |
| Good candidate – partial scholarship | 80 | AWARD_PARTIAL |
| Need-based review | 70 | REVIEW |
| Low CGPA – not eligible | 95 | REJECT |
| Serious disciplinary record | 90 | REJECT |

### 3.3 Inference Engine

The Inference Engine evaluates the student's information against the conditions stored in the Knowledge Base.

It identifies the matching rules and selects the rule with the highest priority to determine the final scholarship decision.

## 4. Scholarship Eligibility Rules

The system applies the following conditions:

**Rule 1: Top Merit Candidate**
- CGPA ≥ 3.7
- Co-curricular Score ≥ 80
- Family Income ≤ RM8,000
- No disciplinary actions

Decision: Full Scholarship.

**Rule 2: Good Candidate – Partial Scholarship**
- CGPA ≥ 3.3
- Co-curricular Score ≥ 60
- Family Income ≤ RM12,000

Decision: Partial Scholarship.

**Rule 3: Need-Based Review**
- CGPA ≥ 2.5
- Family Income ≤ RM4,000

Decision: Review.

**Rule 4: Low CGPA – Not Eligible**
- CGPA < 2.5

Decision: Reject.

**Rule 5: Serious Disciplinary Record**
- Disciplinary Actions ≥ 2

Decision: Reject.

## 5. How the System Works

1. The user enters the student's information.
2. The system retrieves the scholarship rules from the Knowledge Base.
3. The Inference Engine checks the student's information against the rule conditions.
4. The system identifies all matching rules.
5. The highest-priority matching rule is selected.
6. The final scholarship decision and explanation are displayed.

## 6. Sample Evaluation Result

The following example demonstrates the system's evaluation:

| Student Information | Value |
|---|---:|
| Student ID | STU001 |
| CGPA | 3.80 |
| Co-curricular Score | 85 |
| Family Income | RM5,000 |
| Disciplinary Actions | 0 |

**Evaluation Result: FULL SCHOLARSHIP AWARDED**

The system selects the Top Merit Candidate rule because the student satisfies all its eligibility conditions.

The selected rule has a priority of 100, making it the highest-priority matching rule in this evaluation.

## 7. Technologies Used

- Python
- Rule-Based Expert System
- Knowledge Representation
- Inference Engine

## 8. Expected Output

The system provides:
- Student information summary.
- Matching scholarship rules.
- Selected rule and priority.
- Final scholarship decision.
- Explanation of why the rule was selected.

## 9. Conclusion

The Scholarship Advisory System demonstrates how a Rule-Based Expert System can be applied to university scholarship evaluation.

By combining a Knowledge Base and an Inference Engine, the system can evaluate student qualifications and generate scholarship decisions based on predefined rules.

Overall, the system helps make scholarship evaluation more systematic, consistent, and understandable.
