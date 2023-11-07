from utiles import *
class AskUI(QDialog):
    answer1_button   : QPushButton
    answer2_button   : QPushButton
    answer3_button   : QPushButton
    english_word     : QLabel
    def __init__(self):
        super().__init__()
        loadUi(PATH + "ui/ask.ui", self)
        self.answer1_button.clicked.connect(lambda: self.check_answer("button1"))
        self.answer2_button.clicked.connect(lambda: self.check_answer("button2"))
        self.answer3_button.clicked.connect(lambda: self.check_answer("button3"))
        self.translated_word = None
        self.translated_key  = None
        self.buttons_array = [self.answer1_button, self.answer2_button, self.answer3_button]
        self.get_word()

    def get_word(self):
        data = json_file.read_data()
        if len(data) < 1:
            return False
        
        for key in reversed(data.keys()):
            if not data[key]["word-displayed"] and not data[key]["stop-asking"]:
                self.translated_word = data[key]["arabic"]
                self.translated_key = key
                english = data[key]["english"]
                self.english_word.setText(english)
                values = get_different_values(len(data)-1, int(key), 2)
                wrong_word1 = data[str(values[0])]["arabic"]
                wrong_word2 = data[str(values[1])]["arabic"]
                random.shuffle(self.buttons_array)
                self.buttons_array[0].setText(wrong_word1)
                self.buttons_array[1].setText(wrong_word2)
                self.buttons_array[2].setText(self.translated_word)
                break
        else:
            for key in data.keys():
                data[key]["word-displayed"] = False
            json_file.save_data(data)
            self.get_word() # it will enter here only one time
        return True
    
    def check_answer(self, button_selected):
        if button_selected == "button1":
            button = self.answer1_button
        elif button_selected == "button2":
            button = self.answer2_button
        elif button_selected == "button3":
            button = self.answer3_button
        
        if button.text() == self.translated_word:
            data = json_file.read_data()
            data[self.translated_key]["word-displayed"] = True
            json_file.save_data(data)
            self.hide()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        self.hide()
        event.ignore()

if __name__ == "__main__":
    app = QApplication([])
    ui = AskUI()
    ui.show()
    app.exec_()