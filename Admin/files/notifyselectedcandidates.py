import streamlit as st
from Admin import sendEmails as se
import json


def app():
    with open("Admin/output/selectedCandidates.json", "r") as f:
        selected_candidates = json.load(f)
    st.title("Notify Selected Candidates")
    st.header("Selected Candidates:")
    for i in range (len(selected_candidates)):
        st.write(f"{i+1}. {selected_candidates[i]['name']}")
        
    if st.button("Notify"):
        with st.spinner('Wait for it...'):
            subject = "Selected for Interview"
            for i in range (len(selected_candidates)):
                message = f"Dear {selected_candidates[i]['name']},\n\nCongratulations! You have been selected for the interview. You have a interview scheduled on 14th Aug 2023. Please be ready for the interview 10 minutes prior\nFollowing is the credentials for login to your interview:\nID: {selected_candidates[i]['email']}\nPassword: {selected_candidates[i]['id']}\n\nRegards,\nHR"
                se.send_email(subject, message, selected_candidates[i]["email"])
        st.success("Emails sent!", icon="🎉")