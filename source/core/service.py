from progress import ProgressBar
from requests import get
from menu import Menu
import json

class ConfigFile:
    def __init__(self, file: str):
        self.filename = file

    def addServer(self, name: str, jarType: str, version: str, folder: str):
        with open(self.filename, 'r') as file:
            contents = json.load(file)

        contents['servers'][name] = {
            'Jar Type': jarType,
            'Version': version,
            'Location': folder
        }

        with open(self.filename, 'w') as file:
            json.dump(contents, file, indent=4)

        return contents
    
    def delServer(self, name: str):
        with open(self.filename, 'r') as file:
            contents = json.load(file)

        del contents['servers'][name]

        with open(self.filename, 'w') as file:
            json.dump(contents, file, indent=4)

        return contents
    
    def getServers(self):
        with open(self.filename, 'r') as file:
            return json.load(file)['servers']