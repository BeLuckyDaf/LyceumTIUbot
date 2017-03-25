import json_file
import usermgr
import random

data = json_file.JsonFile("users.json")

users = data.getcontents()

user = usermgr.isadmin(data, 146505982)

#user["subscriber"] = False

print(user)