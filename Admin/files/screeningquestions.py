import streamlit as st
import json
from Admin import generateQuestions as gq

def app():
    st.title("Generate Screening Questions for selected candidates:")
    
    with open("Admin/output/selectedCandidates.json", "r") as f:
        selected_candidates = json.load(f)
        
    with open("Admin/output/importantData.json", "r") as impdata:
        data = json.load(impdata)
        
    with open ("Admin/jobDescription.json", "r") as jd:
        job = json.load(jd)
        
    
    st.header("Selected Candidates:")
    for i in range (len(selected_candidates)):
        st.write(f"{i+1}. {selected_candidates[i]['name']}")
        
    if st.button("Generate"):
        with st.spinner('Wait for it...'):
            gq.delete_files("Admin/Questions")
            jdKeywords = str(job[0]["keywords"])
            jobTitle = job[0]["title"]
            for i in range (len(selected_candidates)):
                id = selected_candidates[i]["id"]
                for item in data:
                    if item["id"] == id:
                        candidateKeywords = str(data[i]["skills"])
                        questions = gq.generateQuestion(candidateKeywords, jdKeywords, jobTitle)
                        questionsArray = questions.split("\n")
                        with open(f"Admin/Questions/{selected_candidates[i]['id']}.json", "w") as f:
                            json.dump(questionsArray, f, indent=4)
        st.success("Questions generated successfully!")
                
            
            
                
            
            