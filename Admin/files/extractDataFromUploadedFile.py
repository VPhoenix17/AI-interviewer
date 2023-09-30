import streamlit as st
import os
from Admin import extractData as ed
from Admin import cvRanking as cvr
import openai
import streamlit.components.v1 as components


from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Now you can access your environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

def list_files_in_directory(directory):
    file_list = os.listdir(directory)
    return file_list

def showdir(files):
    filelist = []
    for file in files:
        filelist.append(file)
    return "<br>".join(filelist)
    

input_dir = "Admin/uploads"
output_dir = "Admin/output"


def app():
    st.title("Extract Keywords from Resumes:")

    if not os.path.isdir(input_dir):
        os.makedirs(input_dir)


    files = list_files_in_directory(input_dir)

    if files:
        components.html(
            f"""
            <style>
                .headingOne {
                    'background-color: #EBEBEB;'
                }
                
                .accordion {
                    'background-color: #262730;'
                }
            </style>
            
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
            <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
            <div id="accordion">
            <div class="card">
                <div class="card-header" id="headingOne">
                <h5 class="mb-0">
                    <button class="btn btn-link" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                        Uploaded Files
                    </button>
                </h5>
                </div>
                <div id="collapseOne" class="collapse show" aria-labelledby="headingOne" data-parent="#accordion">
                <div class="card-body">
                    {showdir(files)}
                </div>
                </div>
            </div> 
            """,
            height=400,
            scrolling=True,
        )
        #st.write("List of uploaded files:")
        
            
    else:
        st.error("No files uploaded yet!")

    if st.button("Extract Data"):
        if files:
            with st.spinner('This process may take a while...'):
                # loading_message = st.empty()
                # loading_message.text("Processing...")
                if os.path.isfile("Admin/output/mergedData.json"):
                    os.remove("Admin/output/mergedData.json")
                if os.path.isfile("Admin/output/importantData.json"):
                    os.remove("Admin/output/importantData.json")
                ed.extract_data(input_dir, output_dir)
                ed.merge_json_files(output_dir)
                ed.extract_important_data("Admin/output/mergedData.json")
                ed.add_unique_id_to_json("Admin/output/importantData.json")
                ed.delete_unnecessary_files(output_dir)
                # loading_message.text("Data extracted successfully!")
            st.success("Data extracted successfully!", icon="🎉")
            st.balloons()
        
        else:
            st.error("No files uploaded yet!")

