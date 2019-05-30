import json

data = {"president": {"name": "zaphod","home": "betelgeuse"},"guest": {"name": "bob","home": "earth"}
}

json_string = json.dumps(data, indent=4)
print(json_string)


#with open("data_file.json", "w") as write_file:
 #   json.dump(data, write_file)             # dump() takes two positional arguments (1)the data to be serialised & (2)the file object written to
    #json_string = json.dumps(data) # dumps() method writes the json to a python string