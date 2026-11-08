
import streamlit as st
import json
import os

# --------------------------------
# 1. LOAD JSON FILE
# --------------------------------

current_dir = os.path.dirname(os.path.abspath(__file__))
json_file = os.path.join(current_dir, "scholarship_rules.json")

st.title("Scholarship Advisory System")
st.subheader("Scholarship Rules JSON Editor")

# Check whether JSON file exists
if not os.path.exists(json_file):
    st.error("scholarship_rules.json not found!")
    st.write("Expected location:", json_file)
    st.stop()

# Load JSON
with open(json_file, "r", encoding="utf-8") as file:
    rules = json.load(file)

# --------------------------------
# 2. JSON EDITOR
# --------------------------------

json_input = st.text_area(
    "Edit scholarship rules here:",
    value=json.dumps(rules, indent=4),
    height=400
)

# --------------------------------
# 3. VALIDATE JSON
# --------------------------------

try:
    edited_rules = json.loads(json_input)

    if not isinstance(edited_rules, (dict, list)):
        st.error("JSON must contain an object or list.")
    else:
        st.success("JSON rules are valid!")
        st.write("Total rules:", len(edited_rules))

        # Save edited JSON
        if st.button("Save JSON Rules"):
            with open(json_file, "w", encoding="utf-8") as file:
                json.dump(edited_rules, file, indent=4)

            st.success("Scholarship rules saved successfully!")

except json.JSONDecodeError as e:
    st.error(f"Invalid JSON: {e}")
