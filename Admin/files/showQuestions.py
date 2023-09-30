import streamlit as st
import json
import os

def app():
    with open ("Admin/output/selectedCandidates.json", "r") as f:
        selected_candidates = json.load(f)
    st.title("Show Generated Questions")
    candidates = []
    for item in selected_candidates:
        candidates.append(item["name"])
    name = st.selectbox("Select Candidate", candidates)
    for item in selected_candidates:
        if item["name"] == name:
            id = item["id"]
            if os.path.isfile(f"Admin/Questions/{id}.json"):
                with open (f"Admin/Questions/{id}.json", "r") as f:
                    questions = json.load(f)
                    for i in range(len(questions)):
                        st.write(f"{questions[i]}")
            else:
                st.error("No questions generated yet!")