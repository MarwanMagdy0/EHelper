from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from utiles import *

class ChooseWordsUI(QDialog):
    scrollArea: QScrollArea
    def __init__(self):
        super().__init__()
        loadUi(PATH + "ui/select_words.ui", self)
        self.scroll_layout = self.scrollArea.widget().layout()
        self.refresh_ui()
    
    def refresh_ui(self):
        for key in reversed(json_file.keys()):
            word_translate = json_file[key]
            word          = word_translate["english"]
            arabic        = word_translate["arabic"]
            stop_asking   = word_translate["stop-asking"]
            custom_check_box = CustomCheckBox("{} | {}".format(word, arabic), self, id_=key)
            custom_check_box.checked.connect(self.check_box_is_checked)
            if not stop_asking:
                custom_check_box.setChecked(True)
            self.scroll_layout.addWidget(custom_check_box)
        
    def check_box_is_checked(self, id_):
        data = json_file.read_data()
        word_translate = data[id_]
        word_translate["stop-asking"] = not word_translate["stop-asking"]
        data[id_] = word_translate
        json_file.save_data(data)


if __name__ == "__main__":
    app = QApplication([])
    ui = ChooseWordsUI()
    ui.show()
    app.exec_()