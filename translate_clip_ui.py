from utiles import *

class TranslatorThread(QThread):
    text_is_translated = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.text_to_translate = None
    def run(self):
        if self.text_to_translate:
            print(self.text_to_translate)
            arabic = translate_to_arabic(self.text_to_translate)
            print(arabic)
            self.text_is_translated.emit(arabic)
        self.text_to_translate = None

class TranslateUI(QDialog):
    save_button: QPushButton
    translate_button: QPushButton
    english_text: QTextEdit
    arabic_text : QTextEdit
    new_word_is_added = pyqtSignal()
    def __init__(self):
        super().__init__()
        loadUi("ui/translate_clipboard.ui", self)
        self.save_button.clicked.connect(self.save_and_exit_method)
        self.translate_button.clicked.connect(self.translate_word_method)
        self.new_key = None
        self.translator_thread = TranslatorThread()
        self.translator_thread.text_is_translated.connect(self.update_arabic)
    
    def translate_word_method(self):
        self.save_button.setEnabled(False)
        self.translate_button.setEnabled(False)
        self.translator_thread.text_to_translate = self.english_text.toPlainText()
        self.translator_thread.start()
    
    def update_arabic(self, text):
        self.arabic_text.setText(text)
        self.save_button.setEnabled(True)
        self.translate_button.setEnabled(True)
    def save_and_exit_method(self):
        data = json_file.read_data()
        if self.new_key is None:
            self.new_key = len(data)
        data[str(self.new_key)] = {
            "english":self.english_text.toPlainText().strip(),
            "arabic":self.arabic_text.toPlainText().strip(), 
            "word-displayed":False
        }
        json_file.save_data(data)
        self.new_word_is_added.emit()
        self.hide()
        self.english_text.setText("")
        self.arabic_text.setText("")


if __name__ == "__main__":
    app = QApplication([])
    ui = TranslateUI()
    ui.show()
    app.exec_()