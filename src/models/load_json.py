import os
import json


def read_json(json_file):
    if not os.path.exists(json_file):
        return {}

    try:
        with open(json_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}


def write_json(json_file, data):
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
