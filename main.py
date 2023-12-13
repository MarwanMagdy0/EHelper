from PIL import Image
from translate_clip_ui import *
from ask import *
from utiles import *
import pystray

TIMER = 20 * 60000 # min

class TrayThread(QThread):
    ui: QMainWindow
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.translate_clip_obj = self.ui.translate_window

    def on_left_click(self):
        """
        this method show the screen of the program
        """
        self.ui.showMaximized()
        self.ui.activateWindow()
    
    def translate_clip(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        self.translate_clip_obj.english_text.setText(text)
        self.translate_clip_obj.arabic_text.setText("")
        self.translate_clip_obj.save_button.setEnabled(False)
        self.translate_clip_obj.new_key = None
        self.translate_clip_obj.show()
        self.translate_clip_obj.activateWindow()

    def on_right_click(self):
        """
        this method closes the entire program
        """
        self.translate_clip_obj.close()
        self.ui.close()

    def run(self):
        image = Image.open(PATH + "ui/data/logo.png")

        # Create a menu item with the left-click event handler
        menu = (pystray.MenuItem("show", self.on_left_click, default = True),
                pystray.MenuItem("trans-clip", self.translate_clip),
                pystray.MenuItem("exit", self.on_right_click))

        # Create the tray icon with the menu
        icon = pystray.Icon("tray_icon", image, "Tray Icon", menu)

        # Run the tray icon
        icon.run()

class MainUI(QMainWindow):
    listWidget_english : QListWidget
    listWidget_arabic  : QListWidget
    search_line: QLineEdit
    add_button : QPushButton
    def __init__(self):
        super().__init__()
        loadUi(PATH + "ui/main.ui", self)
        self.add_button.clicked.connect(self.add_button_clicked)
        self.search_line.textChanged.connect(self.search_line_method)
        self.init_translate_window()
        self.init_list_widget()
        self.init_tray_thread()
        self.init_timers()
        self.ask_ui = AskUI()
    
    def search_line_method(self):
        self.listWidget_arabic. clear()
        self.listWidget_english.clear()
        for key in reversed(json_file.keys()):
            word_translate = json_file[key]
            word      = word_translate["english"]
            arabic = word_translate["arabic"]
            if self.search_line.text().strip() =="":
                self.listWidget_english.addItem(word)
                self.listWidget_arabic.addItem(arabic)

            elif self.search_line.text() in word or self.search_line.text() in arabic:
                self.listWidget_english.addItem(word)
                self.listWidget_arabic.addItem(arabic)

    def init_tray_thread(self):
        self.tray_thread  = TrayThread(self)
        self.tray_thread.start()

    def init_translate_window(self):
        self.translate_window = TranslateUI()
        self.translate_window.run_alone = False
        self.translate_window.new_word_is_added.connect(self.load_json)

    def init_list_widget(self):
        self.listWidget_arabic.setVerticalScrollBar(self.listWidget_english.verticalScrollBar())
        self.listWidget_english.doubleClicked.connect(self.edit_index)
        self.listWidget_arabic.doubleClicked. connect(self.edit_index)
        self.load_json()

    def init_timers(self):
        self.ask_timer = QTimer()
        self.ask_timer.timeout.connect(self.ask_question)  # Connect the timer's timeout signal to the update_label function
        self.ask_timer.start(TIMER)

        # self.notify_timer = QTimer()
        # self.notify_timer.timeout.connect(notify)  # Connect the timer's timeout signal to the update_label function
        # self.notify_timer.start((TIMER-0.01)*1000) 

    def load_json(self):
        self.listWidget_arabic. clear()
        self.listWidget_english.clear()
        for key in reversed(json_file.keys()):
            word_translate = json_file[key]
            word = word_translate["english"]
            translate = word_translate["arabic"]
            self.listWidget_english.addItem(word)
            self.listWidget_arabic.addItem(translate)
    
    def add_button_clicked(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        self.translate_window.english_text.setText(text)
        self.translate_window.save_button.setEnabled(False)
        self.translate_window.translate_word_method()
        self.translate_window.new_key = None
        self.translate_window.show()
    
    def edit_index(self, index: QModelIndex):
        row_clicked_index = index.row()
        data = json_file.read_data()
        words_length = len(data)
        self.translate_window.new_key = words_length - row_clicked_index - 1
        word_data = data[str(words_length - row_clicked_index - 1)]
        english = word_data["english"]
        arabic  = word_data["arabic"]
        self.translate_window.english_text.setText(english)
        self.translate_window.arabic_text.setText(arabic)
        self.translate_window.save_button.setEnabled(True)
        self.translate_window.show()
    
    def ask_question(self):
        self.ask_ui.answer1_button.setEnabled(True)
        self.ask_ui.answer2_button.setEnabled(True)
        self.ask_ui.answer3_button.setEnabled(True)
        done = self.ask_ui.get_word()
        if done:
            self.ask_ui.show()
            self.ask_ui.activateWindow()
        
    def closeEvent(self, event):
        if event.spontaneous():
            self.hide()
            event.ignore()
        else:
            event.accept()


app = QApplication([])
ui = MainUI()
app.exec_()