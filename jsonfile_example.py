#!/usr/bin/python3

import json_file
import usermgr

# Create an object of JsonFile
# jsonfile = json_file.JsonFile("users.json")

# Get a dict from json file
# data = jsonfile.getcontents()

# Add a new admin to the record
# data["admins"].append({"id" : 183562293})

# Remove a record where id = 146505982
# data["admins"].remove({"id" : 146505982})

# Existing admin id -> returns true
# print(usermgr.isadmin(jsonfile, 183562293))

# Nonexistent admin id -> returns false
# print(usermgr.isadmin(jsonfile, 111111111))

cnslt_json = json_file.JsonFile("consultations.json")
data = cnslt_json.getcontents()


# for i in data:
#     print("Предмет: {0}".format(i))
#     for m in data[i]:
#         print("Преподаватель: {0} - Аудитория: {1} - Дни: {2}".format(m["name"], m["room"], m["time"]))
#     print("----")

print(data["Экономика"][0]["name"] == "Ярышкина С.Ф.")
    