import openai
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

def getKeywords(JD):
    data=JD
    query="Find all the keywords in the above jd. Your response must be only keywords in a single line. no need to give the description of the keywords"
    keywords=fire_Request(data,query)
    return keywords

def getIdeal(Job_Title, keywords):
    separator=", "
    keywordsString = separator.join(str(item) for item in keywords)
    data = "Job Title: " + Job_Title + "\nKeywords: " + keywordsString
    query="Write the Ideal Job description for the given Job Title and the job description must contain the keywords. the description must be aleast 2 pages long."
    ideal_JD=fire_Request(data,query)
    return ideal_JD

def getSuggestions(job,possibles):
    data=str(possibles)
    query=f"The above array provides possible suggestions that can be added for {job} Job Description for hiring. Using strictly the keywords from the array generate maximum 10 points that can be added to make the job description better. Your response must be in the form of a list. dont add any special characters in the start of any sentence."
    suggestion=fire_Request16(data,query)
    return suggestion

def incorporateSuggestion(job, jobDescription, suggestion):
    data = f"Job Title: {job} \nJob Description: {jobDescription} '\nSuggestion: {suggestion}"
    query = f"Add the above suggestion to the job description for {job} and give the final job description."
    finalJD = fire_Request(data, query)
    return finalJD

def findCommon(JD,idealJD):
    data="This is the first JD: \n"+str(JD)+"\nThis is the Second JD: \n"+str(idealJD)
    query="Find the common keywords between first JD and Second JD, given above and print in single line"
    commonKeywords=fire_Request(data,query)
    return commonKeywords

def calcScore(len1,len2,len3):
    num=(len1-len3)*0.5+len3
    denom=len2
    score=num/denom
    
    return score