#!/usr/bin/python3

import json_file

usertier = ["admins", "moderators", "subscribers"]


def adduser(tier, jsonfile: json_file.JsonFile, userid: int):
    if tier in usertier:
        data = jsonfile.getcontents()
        if not ({'id': userid} in data[tier]):
            data[tier].append({'id': userid})
        jsonfile.writecontents(data)


def removeuser(tier, jsonfile: json_file.JsonFile, userid: int):
    if tier in usertier:
        data = jsonfile.getcontents()
        if ({'id': userid} in data[tier]):
            data[tier].remove({'id': userid})
        jsonfile.writecontents(data)


def isadmin(jsonfile: json_file.JsonFile, userid: int) -> bool:
    data = jsonfile.getcontents()
    if {'id': userid} in data["admins"]:
        return True
    else:
        return False
        

def ismoder(jsonfile: json_file.JsonFile, userid: int) -> bool:
    data = jsonfile.getcontents()
    if {'id': userid} in data["moderators"]:
        return True
    else:
        return False
        
        
def issub(jsonfile: json_file.JsonFile, userid: int) -> bool:
    data = jsonfile.getcontents()
    if {'id': userid} in data["subscribers"]:
        return True
    else:
        return False

        
def get_subs(jsonfile: json_file.JsonFile):
    data = jsonfile.getcontents()
    return data["subscribers"]