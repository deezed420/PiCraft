from progress import ProgressBar
from json import load, dump
from os import system, name
from requests import get
from menu import Menu

def clear(): system('cls' if name == 'nt' else 'clear')

class ConfigFile:
    def __init__(self, file: str):
        self.filename = file

    def addServer(self, name: str, jarType: str, version: str) -> None:
        with open(self.filename, 'r') as file:
            contents = load(file)

        contents['servers'][name] = {
            'Jar Type': jarType,
            'Version': version
        }

        with open(self.filename, 'w') as file:
            dump(contents, file, indent=4)

        return contents
    
    def delServer(self, name: str) -> None:
        with open(self.filename, 'r') as file:
            contents = load(file)

        del contents['servers'][name]

        with open(self.filename, 'w') as file:
            dump(contents, file, indent=4)

        return contents
    
    def getServers(self) -> dict:
        with open(self.filename, 'r') as file:
            return load(file)['servers']