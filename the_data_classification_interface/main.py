from PySide6.QtWidgets import QApplication as Application
from PySide6.QtWidgets import QMainWindow
from the_data_clasification_interface import Ui_MainWindow

class DataClassificationApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Data Classification Interface")

if __name__ == "__main__":
    app = Application([])
    window = DataClassificationApp()
    window.show()
    app.exec()