import streamlit as st
from mentor_agent import analyze_code

st.set_page_config(page_title="AI Coding Mentor", layout="wide")

st.title("🧠 AI  LogicMedic Agent ")
st.write("Paste your Python or Java code and get mentor-style feedback.")

# Language selection
language = st.selectbox("Select Language:", ["Python", "Java"])

# Code input
code = st.text_area(
    "Enter your code:",
    height=300,
    placeholder="Paste your Python or Java code here..."
)

if st.button("Analyze"):
    if code.strip() == "":
        st.warning("Please enter some code.")
    else:
        with st.spinner("Analyzing your code..."):
            feedback = analyze_code(code, language)

        st.subheader("📌 Mentor Feedback")
        # Print feedback line by line
        for line in feedback.split("\n"):
            st.write(line)