import PyPDF2
import openai
import os
import json
import time 
import pandas as pd

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Now you can access your environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

def read_pdf_resume(file_path):
    resume_text = ""
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            resume_text += page.extract_text()

    return resume_text

def save_text_to_file(text, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(text)
        
def save_text_to_json(response_json, output_file):
    with open(output_file, "a") as json_file:
        json.dump(response_json, json_file, indent=4)

def delete_json_contents(file_path):
    with open(file_path, "w") as json_file:
        json.dump("", json_file, indent=4)
        
def delete_files(input_dir):
    file_list = os.listdir(input_dir)
    for file_name in file_list:
        file_path = os.path.join(input_dir, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            
def delete_unnecessary_files(input_dir):
    for file in os.listdir(input_dir):
        if not (file.startswith("importantData") or file.startswith("mergedData") or file.startswith("selectedCandidates") or file.startswith("scores")):
            file_path = os.path.join(input_dir, file)
            os.remove(file_path)

def convert_pseudo_json_to_json(pseudo_json_string):
    json_data = {}
    key_value_pairs = pseudo_json_string.split('\n')
    key = None
    for line in key_value_pairs:
        if ':' in line:
            key, value = line.split(':', 1)
            json_data[key] = value.strip()
        elif key is not None:
            json_data[key] += '\n' + line.strip()
    return json_data

def jsonToExcel(input_file, output_file):
    with open(input_file, "r") as f:
        file_data = json.load(f)
        
    df = pd.DataFrame(file_data)
    df.to_excel(output_file, index=False, sheet_name = "Selected Candidates")

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

def extract_resume_data(file_path, txtoutput_file):
    resume_text = read_pdf_resume(file_path)
    query = """From the above resume, extract the following information: 
    1. Name as 'name', 
    2. Email as 'email', 
    3. Phone number as 'phone_number',
    4. Create a list of dictionaries for education, in the dictionary you must have - 
        1. Instituion name as 'institution',
        2. Degree as 'degree',
        3. marks as 'marks', respond with integer value only,
    5. Create a list of dictionaries for experience, in the dictionary you must have - 
        1. Organization name as 'organization',
        2. role as 'role',
        3. create a list for skills as 'skills'
        Even if no experience is mentioned, create an empty list of ditionaries having the above mentioned keys,
    6. create a list of key skill as 'key_skills',
    7. create a list of soft skill as 'soft_skills', and add data to 'soft_skills' if there is any personal information about the candidate. dont include weblinks or references,
    Give the output in json format"""
    response = fire_Request(resume_text, query)
    #response_json = convert_pseudo_json_to_json(response)
    save_text_to_file(response, txtoutput_file) 

def extract_data(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            file_path = os.path.join(input_dir, filename)
            txtoutput_file = os.path.join(output_dir, f"{filename}".replace(".pdf", ".json"))
            extract_resume_data(file_path, txtoutput_file)
        else:
            continue
        
def merge_json_files(input_dir):
    mergedData = []
    for file in os.listdir(input_dir):
        if (not((file.startswith("merged") or file.startswith("scores") or file.startswith("important") or file.startswith("selected") or file.startswith("suggestions"))) and file.endswith(".json")):
            file_path = os.path.join(input_dir, file)
            with open(file_path, "r") as f:
                data = json.load(f)
                mergedData.append(data)
            
    with open("Admin/output/mergedData.json", "w") as f:
        json.dump(mergedData, f, indent=4)
        
def extract_important_data(input_file):
    with open(input_file, "r") as f:
        file_data = json.load(f)
        
    finalData = []
    for item in file_data:
        all_skills = set()
        marks = []
        for experience in item.get("experience", []):
            all_skills.update(experience.get("skills", []))
        all_skills.update(item.get("key_skills", []))
        all_skills.update(item.get("soft_skills", []))
        
        for education in item.get("education", []):
            if education.get("marks") > 40 and education.get("marks") < 100:
                marks.append(education.get("marks"))
            if education.get("marks") > 100:
                marks.append(education.get("marks")/10)
        newdata = [{"name": item["name"], "email": item["email"], "phone_number": item["phone_number"], "education": len(item["education"]),"marks": marks ,"skills": list(all_skills)}]
        finalData.extend(newdata)
        
    json.dump(finalData, open("Admin/output/importantData.json", "w"), indent=4)
        
        
def generate_unique_id(name):
    # Get current timestamp in milliseconds
    timestamp = int(time.time() * 1000)
    unique_string = f"{name.lower()}_{timestamp}"
    unique_id = abs(hash(unique_string))
    return unique_id

def add_unique_id_to_json(input_file):
    with open(input_file, "r") as json_file:
        json_data = json.load(json_file)
    
    for item in json_data:
        unique_id = generate_unique_id(item["name"])
        item["id"] = unique_id

    with open(input_file, "w") as json_file:
        json.dump(json_data, json_file, indent=4)