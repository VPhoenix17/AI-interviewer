import streamlit as st
import json
import os
from streamlit_option_menu import option_menu
from Admin.extractData import jsonToExcel as jte
from Admin import sendEmails as se
from Admin import cvRanking as cvr
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()



def select_candidates(allInfoFile, scoreFile, no_of_candidates):
    with open(allInfoFile, "r") as f:
        allInfo = json.load(f)
    
    with open (scoreFile, "r") as f:
        scores = json.load(f)
    
    selected_candidates = []
    selected_candidates_json = []
    for i in range(no_of_candidates):
        id = scores[i]["id"]
        for item in allInfo:
            if item["id"] == id:
                selected_candidates.append([item["name"], item["email"], item["phone_number"]])
                data = [{"id": item["id"], "name": item["name"], "email": item["email"], "phone_number": item["phone_number"]}]
                selected_candidates_json.extend(data)
                
    with open("Admin/output/selectedCandidates.json", "w") as f:
        json.dump(selected_candidates_json, f, indent=4)
        
    jte("Admin/output/selectedCandidates.json", "Admin/output/selectedCandidates.xlsx")
    return selected_candidates

def app():
    hrEmail = os.getenv("HR_EMAIL_ADDRESS")
    cvr.set_score("Admin/output/importantData.json", "Admin/jobDescription.json")
    cvr.sortcvs("Admin/output/scores.json")
    with open ("Admin/output/scores.json", "r") as f:
        scores = json.load(f)
    maxValue = len(scores)
    st.title("Shortlist Candidates")
    number = 0
    selected_candidates = []
    # Option selection on the main page
    with st.sidebar:
        selected = option_menu(
        menu_title = "Shortlist by:",
        options = ["Number", "Percentage"],
        icons=["123", "percent"],
        menu_icon="funnel",
        default_index = 0,
        orientation="horizontal"
    )
    #option = st.radio("Choose an option:", ["Number of People", "Percentage of People"])

    if selected == "Number":
        st.markdown("### Enter Number of People:")
        number = st.number_input(label="", min_value=1, max_value=maxValue, value=1, step = 1)
        st.write(f"You selected {number} people.")

    elif selected == "Percentage":
        st.markdown("### Enter Percentage of People:")
        percentage = st.number_input(label="", min_value=1, max_value=100, value=1, step = 5)
        st.write(f"You selected {percentage}% of people.")

    if st.button("Select"):
        if selected == "Number":
            with st.spinner('Wait for it...'):
                selected_candidates = select_candidates("Admin/output/importantData.json", "Admin/output/scores.json", number)
                st.table(selected_candidates)
                se.send_email_with_attachment("Selected candidates for interview", "Following is attached the list of selected candidates for interview", hrEmail, "Admin/output/selectedCandidates.xlsx")
            st.success("Excel sent to your email!", icon="✉️")
            
        elif selected == "Percentage":
            with st.spinner('Wait for it...'):
                selected_candidates = select_candidates("Admin/output/importantData.json", "Admin/output/scores.json", int(percentage/100 * 10))
                st.table(selected_candidates)
                se.send_email_with_attachment("Selected candidates for interview", "Following is attached the list of selected candidates for interview", hrEmail, "Admin/output/selectedCandidates.xlsx")
            st.success("Excel sent to your email!", icon="✉️")
        