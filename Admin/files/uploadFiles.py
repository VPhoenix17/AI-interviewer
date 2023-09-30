import streamlit as st
import os


def save_uploaded_file(uploaded_file):
    file_path = os.path.join("Admin/jds", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        #st.success(f"File saved: {uploaded_file.name}")        


def app():
    st.title("Upload All Resumes")

    uploaded_files = st.file_uploader("Choose a file...", type=["pdf"],accept_multiple_files=True)

    if st.button("Continue"):
        if uploaded_files:
            for uploaded_file in uploaded_files:
                save_uploaded_file(uploaded_file)
            st.success("All Files saved successfully!")
        else:
            st.warning("Files not uploaded. Please upload files.")


