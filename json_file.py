#!/usr/bin/python3

if __name__ == '__main__':
    print("You can't launch the module file directly.\nPlease, import it.")
    
import json
import constants


class JsonFile(object):

    def __init__(self, path, encod='UTF8'):
        self.filepath = path
        self.encod = encod
        self.data = object

        
    def getcontents(self):
        with open(self.filepath, "r", encoding=self.encod) as file:
            data_str = file.read().replace('\n', '')
            self.data = json.loads(data_str)
        return self.data

        
    def setpath(self, newpath):
        self.filepath = newpath

        
    def writecontents(self, contents: dict):
        with open(self.filepath, "w", encoding=self.encod) as file:
            file.write(json.dumps(contents))
