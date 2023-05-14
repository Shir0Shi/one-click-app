import json


def rewrite_set_file(set_data=None):
    if set_data is None:
        set_data = []
    with open(sets_file, "w") as f:
        json.dump(set_data, f, indent=4)


sets_file = "sets.json"
