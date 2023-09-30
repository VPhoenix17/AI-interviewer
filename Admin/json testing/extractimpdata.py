import json

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
            if education.get("marks") > 10 and education.get("marks") < 100:
                marks.append(education.get("marks"))
        newdata = [{"name": item["name"], "email": item["email"], "phone_number": item["phone_number"], "education": len(item["education"]),"marks": marks ,"skills": list(all_skills)}]
        finalData.extend(newdata)
        
    json.dump(finalData, open("json testing/importantData.json", "w"), indent=4)

extract_important_data("json testing/mergedData.json")