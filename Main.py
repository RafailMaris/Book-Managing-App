from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QStackedWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QLineEdit, QSizePolicy,
    QFormLayout, QSpacerItem
)
import sys
import MainWindow
from DB import *
import multiprocessing
if __name__ == "__main__":

    multiprocessing.freeze_support()
    #query = db.query
    app = QApplication(sys.argv)
    db = DB()
    window = MainWindow.MainWindow(db)
    window.resize(1000, 700)  # Increased height for better layout
    window.show()

    sys.exit(app.exec())