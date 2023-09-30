import streamlit as st
from streamlit_option_menu import option_menu
from Admin.files import home, extractDataFromUploadedFile, notifyselectedcandidates, jobDescription, shortlistCandidate, uploadFiles, screeningquestions, showQuestions, showfinalScores

HRpages = {
    "Extract Data": extractDataFromUploadedFile,
    "Upload Resumes": uploadFiles,
    "Select Candidates": shortlistCandidate,
    "Notify Selected Candidates": notifyselectedcandidates,
    "Job Details": jobDescription,
    "Screening Questions": screeningquestions,
    "Show Generated Questions": showQuestions,
    "Show Final Scores": showfinalScores,
}
def page():
    with st.sidebar:
        HRselected = option_menu(
            menu_title = "Main Menu",
            options = ["Home","Job Details", "Upload Resumes","Extract Data", "Select Candidates", "Notify Selected Candidates", "Screening Questions", "Show Generated Questions", "Show Final Scores"],
            icons = ["house","person-workspace", "archive", "file-earmark", "person-check-fill", "envelope-check", "patch-question","list-task"],
            menu_icon="cast",
            default_index = 0 
        )

    def home():
        st.title("AI Recruiter")
        st.image("Student\\INTERVIEWER\\static\\images\\axis_bank_logo.png")
        st.header("Welcome Admin")
        st.text("Please select an option from the menu on the left.")

    if HRselected in HRpages:
        HRpages[HRselected].app()
    else:
        home()
