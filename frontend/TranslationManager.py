import os
import json
from PyQt5.QtCore import QObject, pyqtSignal

class GlobalTranslationManager(QObject):
    languageChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.json_path = os.path.join(os.path.dirname(__file__), "..", "Style", "translations.json")
        self.translations = {}
        self.current_language = "English"
        self.load_translations()

    def load_translations(self):
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, "r", encoding="utf-8") as f:
                    self.translations = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error loading JSON file: {e}")



    def setLanguage(self, language):
        
        if language in self.translations:
            if language != self.current_language:
                self.current_language = language
                self.languageChanged.emit(language) 

    def getTranslation(self, key):
        return self.translations.get(self.current_language, {}).get(key, 
               self.translations.get("English", {}).get(key, key))

# Initialize translator globally
translator = GlobalTranslationManager()
