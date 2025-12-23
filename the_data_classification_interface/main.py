from PySide6.QtWidgets import QApplication as Application
from PySide6.QtWidgets import QMainWindow
from the_data_clasification_interface import Ui_MainWindow
class DataClassificationApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Data Classification Interface")
        self.the_top_holder.hide()
        self.collapse_button.clicked.connect(self.toggle_diss_menu)
    def collapse_diss_menu(self):
        self.title.hide()
        self.disscussions_list.hide()
        self.the_top_holder.show()
        self.main_horizantal_layout.setStretch(1, 20)
    def expand_diss_menu(self):
        self.title.show()
        self.disscussions_list.show()
        self.the_top_holder.hide()
        self.main_horizantal_layout.setStretch(1, 5)
    def toggle_diss_menu(self):
        if self.disscussions_list.isVisible():
            self.collapse_diss_menu()
        else:
            self.expand_diss_menu()
if __name__ == "__main__":
    app = Application([])
    window = DataClassificationApp()
    window.show()
    app.exec()