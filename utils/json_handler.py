import json

def load_json_file(path):
    with open(path, 'r') as file:
        return json.load(file)

def save_json_file(path, data):
    with open(path, 'w', encoding="utf8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False, sort_keys=True)
