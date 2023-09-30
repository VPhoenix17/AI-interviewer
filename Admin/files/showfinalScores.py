import streamlit as st
import json

def app():
    with open("Student/INTERVIEWER/finals/finalScores.json", "r") as fs:
        fs_data = json.load(fs)
        
    with open("Admin/output/selectedCandidates.json", "r") as sc:
        sc_data = json.load(sc)
    st.title("Show scores")
    candidates = []
    ids = []
    for id in fs_data: 
        id = int(id)
        for item in sc_data:
            if id == item["id"]:
                candidates.append(item["name"])

    name = st.selectbox("Select Candidate", candidates)
    
    for item in sc_data:
        if item["name"] == name:
            id = item["id"]
            id = str(id)
            st.write("Score: ", fs_data[id])
    
