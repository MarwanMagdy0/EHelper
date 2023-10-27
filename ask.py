from utiles import *
class AskUI(QDialog):
    check_button     : QPushButton
    show_button      : QPushButton
    english_word     : QLabel
    translated_label : QLabel
    arabic_text      : QTextEdit
    def __init__(self):
        super().__init__()
        loadUi(PATH + "ui/ask.ui", self)
        self.check_button.clicked.connect(self.check_text)
        self.show_button.clicked .connect(self.show_text )
        self.translated_word = None
        self.translated_key  = None
        self.get_word()

    def get_word(self):
        data = json_file.read_data()
        if len(data) < 1:
            return
        self.translated_label.setText("")
        self.arabic_text.setText("")
        
        for key in reversed(data.keys()):
            if not data[key]["word-displayed"] and not data[key]["stop-asking"]:
                self.translated_word = data[key]["arabic"]
                self.translated_key = key
                english = data[key]["english"]
                self.english_word.setText(english)
                break
        else:
            for key in data.keys():
                data[key]["word-displayed"] = False
            json_file.save_data(data)
            self.get_word() # it will enter here only one time

    def check_text(self):
        if self.arabic_text.toPlainText() == self.translated_word:
            data = json_file.read_data()
            data[self.translated_key]["word-displayed"] = True
            json_file.save_data(data)
            print("True")
            self.hide()

    def show_text(self):
        self.translated_label.setText(self.translated_word)
    
    def closeEvent(self, event):
        self.hide()
        event.ignore()



if __name__ == "__main__":
    app = QApplication([])
    ui = AskUI()
    ui.show()
    app.exec_()