#!/usr/bin/python3

import json_file


def newadmin(jsonfile: json_file.JsonFile, userid: int):
    data = jsonfile.getcontents()
    if not ({'id': userid} in data["admins"]):
        data["admins"].append({'id': userid})
    jsonfile.writecontents(data)


def newmoder(jsonfile: json_file.JsonFile, userid: int):
    data = jsonfile.getcontents()
    if not ({'id': userid} in data["moderators"]):
        data["moderators"].append({'id': userid})
    jsonfile.writecontents(data)


def isadmin(jsonfile: json_file.JsonFile, userid: int) -> bool:
    data = jsonfile.getcontents()
    if {'id': userid} in data["admins"]:
        return True
    else:
        return False
