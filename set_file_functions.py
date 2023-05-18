import json
import os.path


def rewrite_set_file(set_data=None):
    if set_data is None:
        set_data = []
    with open(sets_file, "w") as f:
        json.dump(set_data, f, indent=4)


def load_data():
    if not os.path.exists(sets_file):
        rewrite_set_file()
    with open(sets_file, "r") as f:
        data = json.load(f)
    if data:
        return data
    else:
        return []


sets_file = "sets.json"


def update_set_data(new_set, data):
    found = False
    for i, set_ in enumerate(data):
        if set_["id"] == new_set["id"]:
            data[i] = new_set
            found = True
            break
    if not found:
        data.append(new_set)
    return data
