import openai
import json
import os
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
        "content": data+"\n"+query}
    ]
    )
    response=completion.choices[0].message.content
    return response

def fire_Request16(data,query):
    
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[
        {"role": "user", 
        "content": data+"\n"+query}
    ]
    )
    response=completion.choices[0].message.content
    return response

def delete_files(input_dir):
    for file_name in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file_name)
        os.remove(file_path)

def generateQuestion(candKeyword, jdKeyword, job):
    data = f"Job Title: {job}\nCandidate Skill: {candKeyword}\nJob Requirements: {jdKeyword}"
    query = """For the given job title, generate 10 questions based on the candidate skill and job requirements.
            give more importance to the candidates skill and ask personal questions about those skills.
            ask more technical questions based on the candidates skill.
            give your response in the form of list. no need to add any extra information. 
            just give your response as a list of 10 questions."""
    questions = fire_Request(data,query)
    return questions

