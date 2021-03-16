"""
    Implement a function that creates a dictionary from a
    JSON file.
"""

import json


def dictionary_from_json(file_path):
    with open(file_path) as json_file:
        return json.load(json_file)


# --------------------------------------------------------------------
# Tests

json_path = "file.json"
my_dict = dictionary_from_json(json_path)
print(type(my_dict), my_dict)
