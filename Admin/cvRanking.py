import json

def get_score(keyword, skills, education, marks):
    score = 0
    
    for mark in marks:
        score += mark * 0.01    
    
    score += education * 0.1
    keywordset = set(keyword.lower() for keyword in keyword)
    skillset = set(skill.lower() for skill in skills)
    
    common_skills = keywordset.intersection(skillset)
    score += len(common_skills) * 1
    
    extra_skills = skillset.difference(keywordset)
    score += len(extra_skills) * 0.5
    return score


def set_score(input_file, job_description):
    with open (job_description, "r") as myfile:
        jd = json.load(myfile)
        
    with open(input_file, "r") as f:
        data = json.load(f)
        
        
    keywords = jd[0]["keywords"]
    new_data = []
    for item in data:
        score = get_score(keywords, item["skills"], item["education"], item["marks"])
        new_data.extend([{"id": item["id"], "score": score}])
        
    with open("Admin/output/scores.json", "w") as f:
        json.dump(new_data, f, indent=4)
        
def sortcvs(input_file):
    with open(input_file, "r") as f:
        data = json.load(f)
        
    data.sort(key=lambda x: x["score"], reverse=True)
    
    with open(input_file, "w") as f:
        json.dump(data, f, indent=4)
        
def select_candidates(allInfoFile, scoreFile, no_of_candidates):
    with open(allInfoFile, "r") as f:
        allInfo = json.load(f)
    
    with open (scoreFile, "r") as f:
        scores = json.load(f)
    
    selected_candidates = []
    for i in range(no_of_candidates):
        id = scores[i]["id"]
        for item in allInfo:
            if item["id"] == id:
                selected_candidates.append([item["name"], item["email"], item["phone_number"]])
    
    return selected_candidates

# set_score("Admin/output/importantData.json", "jobDescription.json")
# sortcvs("json testing/scores.json")