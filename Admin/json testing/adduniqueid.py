import time
import json

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

add_unique_id_to_json("Admin/output/importantData.json")