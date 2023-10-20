from PIL import Image
from translate_clip_ui import *
from utiles import *
import pystray
class TrayThread(QThread):
    """
    This class is to open the second python file and get the internet output from it
    """
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.translate_clip_obj = self.ui.translate_window

    def on_left_click(self):
        """
        this method show the screen of the program
        """
        self.ui.show()
        self.ui.activateWindow()
    
    def translate_clip(self):
        self.translate_clip_obj.new_key = None
        self.translate_clip_obj.show()

    def on_right_click(self):
        """
        this method closes the entire program
        """
        self.ui.close()

    def run(self):
        image = Image.open("/home/marwan/Documents/Python_Projects/Qt/MyWe/wifi.png")

        # Create a menu item with the left-click event handler
        menu = (pystray.MenuItem("   show", self.on_left_click, default = True),
                pystray.MenuItem("trans-clip", self.translate_clip),
                pystray.MenuItem("   exit", self.on_right_click))

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
        loadUi("ui/main.ui", self)
        self.add_button.clicked.connect(self.add_button_clicked)
        self.init_translate_window()
        self.init_list_widget()
        self.init_tray_thread()

    def init_tray_thread(self):
        self.tray_thread  = TrayThread(self)
        self.tray_thread.start()


    def init_translate_window(self):
        self.translate_window = TranslateUI()
        self.translate_window.new_word_is_added.connect(self.load_json)

    def init_list_widget(self):
        self.listWidget_arabic.setVerticalScrollBar(self.listWidget_english.verticalScrollBar())
        self.listWidget_english.doubleClicked.connect(self.edit_index)
        self.listWidget_arabic.doubleClicked.connect(self.edit_index)
        self.load_json()

    def load_json(self):
        self.listWidget_arabic.clear()
        self.listWidget_english.clear()
        for key in reversed(json_file.keys()):
            word_translate = json_file[key]
            word = word_translate["english"]
            translate = word_translate["arabic"]
            self.listWidget_english.addItem(word)
            self.listWidget_arabic.addItem(translate)
    
    def add_button_clicked(self):
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
        self.translate_window.show()


app = QApplication([])
ui = MainUI()
ui.show()
app.exec_()