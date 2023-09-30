import PyPDF2
import openai
import os
import json

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Now you can access your environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

def fire_Request(data,query):
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", 
        "content": data +"\n"+query}
    ]
    )
    response = completion.choices[0].message.content
    return response

def list_files_in_directory(directory):
    file_list = os.listdir(directory)
    return file_list

def save_uploaded_file(uploaded_file):
    file_path = os.path.join("Admin/jds", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        #st.success(f"File saved: {uploaded_file.name}") 

def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    return text

def extract_data(file_path):
    text = read_pdf(file_path)
    query = """From the above Job Description, extract the following information: 
    1. Job Title as 'job_title', 
    2. Job Description as 'job_description', 
    Give the output in json format"""
    response = fire_Request(text, query)
    
    with open ("Admin/jds/JDData.json", "w") as f:
        f.write(response)
        
    
