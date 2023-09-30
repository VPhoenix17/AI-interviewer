import streamlit as st
import json
from Admin import jdEnhancement as je
from Admin import fileprocessing as fp
from streamlit_option_menu import option_menu
import os



def save_to_json(data):
    with open("Admin/jobDescription.json", "w") as f:
        json.dump(data, f, indent=4)

    

def app():
    st.title("Job Details")
    with st.sidebar:
        selected = option_menu(
        menu_title = "Upload as:",
        options = ["Text", "Upload File"],
        icons=["pencil-square", "file-earmark-pdf"],
        menu_icon="file-earmark-arrow-up",
        default_index = 0,
        orientation="horizontal"
    )
    
    #job_data = ""
    #job_title = ""
    keywords = []
    job_data = []
    suggestions = ""    
    
    #If Text Option is selected by user
    if selected == "Text":
        
        #If the user has already entered the job details previously and saved it 
        if os.path.isfile("Admin\jds\JDData.json"):
            with open("Admin\jds\JDData.json", "r") as f:
                job_data1 = json.load(f)
                job_title = job_data1["job_title"]
                job_description = job_data1["job_description"]
         
        #If the user has not entered the job details previously   
        else:
            job_title = ("Enter Job Title here...")
            job_description = "Enter Job Description here..."
            
        #Take input from user
        job_title = st.text_input("Job Title:", job_title)
        job_description = st.text_area("Job Description:", job_description, height=200)
        
        
        if st.button("Score and Suggest"):
            #Checking if both the fields are filled
            with st.spinner('Wait for it...'):
                if job_title and job_description:               
                    # Extract keywords from job description
                    keywords = je.getKeywords(job_description).split(", ")
                    IdealJD = je.getIdeal(job_title, keywords)
                    IdealKeyWords = je.getKeywords(IdealJD).split(", ")
                    commonKeywords = je.findCommon(keywords, IdealKeyWords).split(", ")
                    
                    #Calculating lenghts of the arrays and calculating score
                    JDlen=len(keywords)
                    idealLen=len(IdealJD)
                    commonLen=len(commonKeywords)
                    JD_score= je.calcScore(JDlen,idealLen,commonLen)
                    st.text(f"JD Score: {JD_score}")
                    
                    #Finding suggestions to enhance the JD
                    Possible_enhancements=[x for x in IdealJD if x not in commonKeywords]
                    suggestions = je.getSuggestions(job_title,Possible_enhancements)
                    #saving suggestions in a json file
                    with open ("Admin/output/suggestions.json", "w") as f:
                        json.dump(suggestions, f, indent=4)
                        
                        
                    #Displaying suggestions to the user based on the score of the JD
                    suggestionsArray = suggestions.split("\n")                 
                    if JD_score>=1:
                        st.text("The JD you have created is on point, if you still wish to enhance the description you may consider adding the following points: ")
                        for item in suggestionsArray:
                            if item!='':
                                st.write(item)
                    elif JD_score>0.5 and JD_score<1:
                        st.text("Here are a few suggestions you can add to enhance your JD: ")
                        for item in suggestionsArray:
                            if item!='':
                                st.write(item)
                    else:
                        st.write("You should consider the following suggestions/points and expand your JD to make the applicants better understand their Expected Role:")
                        for item in suggestionsArray:
                            if item!='':
                                st.write(item)
                else:
                    st.warning("Please enter both job title and description.")
                
        st.write("Incorporate the the above changes to your job description manually and click on the button below to save it in our database.")
        if st.button("Save", key="1"):
            with st.spinner('Wait for it...'):
                with open ("Admin/output/suggestions.json", "r") as f:
                    suggestions = json.load(f)
                finaljd = job_description + "\n" + suggestions
                keywords = je.getKeywords(finaljd).split(", ")
                newdata = [{"title": job_title, "description": job_description, "keywords": keywords}]
                job_data.extend(newdata)
                save_to_json(job_data) 
            
        if st.button("Save without changes", key="2"):
            with st.spinner('Wait for it...'):
                keywords = je.getKeywords(job_description).split(", ")
                newdata = [{"title": job_title, "description": job_description, "keywords": keywords}]
                job_data.extend(newdata)
                save_to_json(job_data)
            
    if selected == "Upload File":
        folderpath = "Admin/jds"
        if not os.path.isdir(folderpath):
            os.makedirs(folderpath)


        files = fp.list_files_in_directory(folderpath)
        verificationFile = ""
        if files:
            uploads = []
            for file in os.listdir(folderpath):
                if file.endswith(".pdf"):
                    uploads.append(file)
            existing_file = st.selectbox("Select file from existing uploads", uploads)        
        else:
            st.error("No files uploaded yet!")
            
         
        uploaded_file = st.file_uploader("Upload a New File", type=["pdf"]) 
        
        if uploaded_file:
                fp.save_uploaded_file(uploaded_file)
                st.success("File Uploaded")
            
        if st.button("Score and Suggest"):
            with st.spinner('Wait for it...'):
                if uploaded_file:
                    verificationFile = uploaded_file.name
                    
                if uploaded_file is None:
                    verificationFile = existing_file
                
                if uploaded_file is None and existing_file is None:
                    verificationFile = None
                
                if verificationFile is None:
                    st.error("Please upload a file first!")
                
                if verificationFile is not None:
                    fp.extract_data(file_path = os.path.join("Admin/jds", verificationFile))
                    
                    with open("Admin/jds/JDData.json", "r") as f:
                        job_data = json.load(f)
                    job_title = job_data["job_title"]
                    job_description = job_data["job_description"]
                    
                    st.write(f"Job Title: {job_title}")
                    st.write(f"Job Description: {job_description}")
                    keywords = je.getKeywords(job_description).split(", ")   
                    IdealJD = je.getIdeal(job_title, keywords)
                    IdealKeyWords = je.getKeywords(IdealJD).split(", ")
                    commonKeywords = je.findCommon(keywords, IdealKeyWords).split(", ")
                    
                    JDlen=len(keywords)
                    idealLen=len(IdealJD)
                    commonLen=len(commonKeywords)
                    JD_score= je.calcScore(JDlen,idealLen,commonLen)
                    st.text(f"JD Score: {JD_score}")
                    Possible_enhancements=[x for x in IdealJD if x not in commonKeywords]
                    suggestions = je.getSuggestions(job_title,Possible_enhancements)
                    with open ("Admin/output/suggestions.json", "w") as f:
                        json.dump(suggestions, f, indent=4)
                    suggestionsArray = suggestions.split("\n") 
                    if JD_score>=1:
                        st.text("The JD you have created is on point, if you still wish to enhance the description you may consider adding the following points: ")
                        for item in suggestionsArray:
                            if item!='':
                                st.write(item)
                    elif JD_score>0.5 and JD_score<1:
                        st.text("Here are a few suggestions you can add to enhance your JD: ")
                        for item in suggestionsArray:
                            if item!='':
                                st.write(item)
                    else:
                        st.write("You should consider the following suggestions/points and expand your JD to make the applicants better understand their Expected Role:")
                        for item in suggestionsArray:
                            if item!='':
                                st.write(item)
        
        st.write("Incorporate the the above changes to your job description manually and click on the button below to save it in our database.")
        if st.button("Save", key = "3"):
            with st.spinner('Wait for it...'):
                with open ("Admin/output/suggestions.json", "r") as f:
                    suggestions = json.load(f)
                with open ("Admin/jds/JDData.json", "r") as f:
                    jd_data = json.load(f)
                job_title = jd_data["job_title"]
                job_description = jd_data["job_description"]
                finaljd = job_description + "\n" + suggestions
                keywords = je.getKeywords(finaljd).split(", ")
                newdata = [{"title": job_title, "description": job_description, "keywords": keywords}]
                job_data.extend(newdata)
                save_to_json(job_data) 
            
        if st.button("Save without changes", key = "4"):
            with st.spinner('Wait for it...'):
                keywords = je.getKeywords(job_description).split(", ")
                with open ("Admin/jds/JDData.json", "r") as f:
                    jd_data = json.load(f)
                job_title = jd_data["job_title"]
                job_description = jd_data["job_description"]
                newdata = [{"title": job_title, "description": job_description, "keywords": keywords}]
                job_data.extend(newdata)
                save_to_json(job_data)