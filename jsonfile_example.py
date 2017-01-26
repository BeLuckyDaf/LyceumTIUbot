import json_file
import usermgr

# Create an object of JsonFile
jsonfile = json_file.JsonFile("users.json")

# Get a dict from json file
data = jsonfile.getcontents()

# Add a new admin to the record
data["admins"].append({"id" : 183562293})

# Remove a record where id = 146505982
data["admins"].remove({"id" : 146505982})

# Existing admin id
print(usermgr.isadmin(jsonfile, 183562293))

#
print(usermgr.isadmin(jsonfile, 111111111))