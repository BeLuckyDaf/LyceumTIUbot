#!/usr/bin/python3

import json_file

#usertier = ["admins", "moderators", "subscribers", "allusers"]


#def adduser(tier, jsonfile: json_file.JsonFile, userid: int):
#    if tier in usertier:
#        data = jsonfile.getcontents()
#        if not ({'id': userid} in data[tier]):
#            data[tier].append({'id': userid})
#        jsonfile.writecontents(data)


def adduser(jsonfile: json_file.JsonFile, userid=0, first_name="", last_name="", username="", 
            is_subscriber=True, is_moderator=False, is_admin=False, position="User"):
    data = jsonfile.getcontents()
    for user in data["users"]:
        #print("{0}\n".format(user))
        if ("id" in user and user["id"] == userid):
            return False
        
    data["users"].append({
            "id": userid,
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "subscriber": is_subscriber,
            "moderator": is_moderator,
            "admin": is_admin,
            "position": position})
    jsonfile.writecontents(data)
    return True
    
    
def updateuser(jsonfile: json_file.JsonFile, userid=0, first_name="", last_name="", username="",
            is_subscriber=True, is_moderator=False, is_admin=False, position="User"):
    data = jsonfile.getcontents()
    found = False
    usern = 0;
    for user in data["users"]:
        #print("{0}\n".format(user))
        if ("id" in user and user["id"] == userid):
            found = True
            usern = data["users"].index(user)
    
    if not found:
        return False
    
    data["users"][usern] = {
            "id": userid,
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "subscriber": is_subscriber,
            "moderator": is_moderator,
            "admin": is_admin,
            "position": position}
    jsonfile.writecontents(data)
    return True

        
#def add_allusers(jsonfile: json_file.JsonFile, uname, fname, lname):
#    data = jsonfile.getcontents()
#    if not ({'uname': uname, 'fname': fname, 'lname': lname} in data["allusers"]):
#        data["allusers"].append({'uname': uname, 'fname': fname, 'lname': lname})
#    jsonfile.writecontents(data)


def removeuser(jsonfile: json_file.JsonFile, userid: int):
    data = jsonfile.getcontents()
    for user in data["users"]:
        if ("id" in user and user["id"] == userid):
            del data["users"][data["users"].index(user)]
    jsonfile.writecontents(data)


def isadmin(jsonfile: json_file.JsonFile, userid: int):
    data = jsonfile.getcontents()
    for user in data["users"]:
        if (("id" in user) and (user["id"] == userid) and (user["admin"] == True)):
            return True
    return False
        

def ismoder(jsonfile: json_file.JsonFile, userid: int):
    data = jsonfile.getcontents()
    for user in data["users"]:
        if (("id" in user) and (user["id"] == userid) and (user["admin"] == True)):
            return True
    return False
        
        
def issub(jsonfile: json_file.JsonFile, userid: int) -> bool:
    data = jsonfile.getcontents()
    for user in data["users"]:
        if ("id" in user and user["id"] == userid and user["subscriber"] == True):
            return True
    return False

        
def get_subs(jsonfile: json_file.JsonFile):
    data = jsonfile.getcontents()
    subs = []
    for user in data["users"]:
        if user["subscriber"]:
            subs.append(user)
    return subs
  
  
def get_all_users(jsonfile: json_file.JsonFile):
    data = jsonfile.getcontents()
    return data["users"]
    
    
def get_user(jsonfile: json_file.JsonFile, userid: int):
    data = jsonfile.getcontents()
    user = filter(lambda x: x["id"] == userid, data["users"])
    return tuple(user)[0]