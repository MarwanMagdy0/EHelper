from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QTextEdit, QListWidget, QLineEdit, QDialog
from PyQt5.QtCore import QThread, pyqtSignal, QModelIndex
from googletrans import Translator
from PyQt5.uic import loadUi
import requests
import json
import os
class HandleJsonFiles:
    def __init__(self, file_path, default = None):
        self.file_path = os.path.normpath(file_path)
        if not os.path.isfile(self.file_path):
            if default is not None:
                self.save_data(default)
            else:
                self.save_data({})


    def save_data(self, data):
        with open(self.file_path, 'w') as f:
            json.dump(data, f)

    def read_data(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)
        
    def __getitem__(self, key):
        data = self.read_data()
        return data[key]
    
    def __setitem__(self, key: str, value) -> None:
        data = self.read_data()
        data[key] = value
        self.save_data(data)
        
    def keys(self):
        data = self.read_data()
        return data.keys()

json_file = HandleJsonFiles("words.json")
translator = Translator()


def is_connected_to_internet():
    try:
        if requests.get('https://google.com').ok:
            return True
    except:
        return False


def translate_to_arabic(text):
    if is_connected_to_internet():
        translation = translator.translate(text, src='en', dest='ar')
        return translation.text
    return ""


if __name__ == "__main__":
    # print(json_file.read_data())
    print(translate_to_arabic("Hello, how are you?"))