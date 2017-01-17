if __name__ == '__main__':
    print("You can't launch the module file directly.\nPlease, import it.")
    
import json
import constants

class Json_File:
    
    def __init__(self, file_path, flags='r', encod='UTF8'):
        with open(file_path, flags, encoding=encod) as file:
            data_str = file.read().replace('\n', '')
            self.data = json.loads(data_str)