import json


def write_json(new_data, filename, key_name=None):
    with open(filename, "r+") as file:
        file_data = json.load(file)
        file_data[key_name].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)
