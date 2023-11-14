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
        loadUi(PATH + "ui/translate_clipboard.ui", self)
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_and_exit_method)
        self.translate_button.clicked.connect(self.translate_word_method)
        self.new_key = None
        self.translator_thread = TranslatorThread()
        self.translator_thread.text_is_translated.connect(self.update_arabic)
        self.run_alone = True
    
    def translate_word_method(self):
        if self.english_text.toPlainText() == "":
            return
        self.save_button.setEnabled(False)
        self.translate_button.setEnabled(False)
        self.translator_thread.text_to_translate = self.english_text.toPlainText()
        self.translator_thread.start()
    
    def update_arabic(self, text):
        self.arabic_text.setText(text)
        self.save_button.setEnabled(True)
        self.translate_button.setEnabled(True)

    def save_and_exit_method(self):
        if self.arabic_text.toPlainText().strip() == "" or self.arabic_text.toPlainText().strip()==" ":
            return
        
        data = json_file.read_data()
        if self.new_key is None:
            self.new_key = len(data)
        data[str(self.new_key)] = {
            "english":self.english_text.toPlainText().strip(),
            "arabic":self.arabic_text.toPlainText().strip(), 
            "word-displayed":False,
            "stop-asking": False
        }
        json_file.save_data(data)
        self.new_word_is_added.emit()
        if self.run_alone:
            self.close()
        else:
            self.hide()
        self.english_text.setText("")
        self.arabic_text.setText("")
    
    def closeEvent(self, event):
        if event.spontaneous() and not self.run_alone:
            self.hide()
            event.ignore()
        else:
            event.accept()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and not self.run_alone:
            self.hide()
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    ui = TranslateUI()
    clipboard = QApplication.clipboard()
    text = clipboard.text()
    ui.english_text.setText(text)
    ui.translate_word_method()
    ui.arabic_text.setText("")
    ui.save_button.setEnabled(False)
    ui.new_key = None
    ui.show()
    app.exec_()