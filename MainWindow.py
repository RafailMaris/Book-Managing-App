from sqlite3 import Cursor

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QStackedWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QLineEdit, QSizePolicy,
    QFormLayout, QSpacerItem
)

import AuthorPanelAdd
import PanelView
import BookPanelAdd
import Panel
import QuotePanelAdd
import DB
import AuthorPanelEdit

#STACK INDEXES
# 0 - authorPanelEdit
# 1 - bookPanelEdit
# 2 - quotePanelEdit
# 3 - Panel
# 4 - book panel
# 5 - quote panel
# 6 - author panel

class MainWindow(QMainWindow):
    stack = None
    def __init__(self,db: DB):
        super().__init__()
        self.setWindowTitle("Book Manager")

        # Create buttons
        self.book_button = QPushButton("Books")
        self.quote_button = QPushButton("Quotes")
        self.author_button = QPushButton("Authors")
        # Make them expand equally
        self.book_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.quote_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.author_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        # Menu layout (horizontally centered)
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # left spacer
        button_layout.addWidget(self.author_button)
        button_layout.addWidget(self.book_button)
        button_layout.addWidget(self.quote_button)
        button_layout.addStretch()  # right spacer

        # Panel stack

        self.stack = QStackedWidget()
        self.view = PanelView.PanelView(self.stack,db)
        self.stack.addWidget(Panel.Panel())
        self.stack.addWidget(BookPanelAdd.BookPanelAdd(self.stack,db,self.view))
        self.stack.addWidget(QuotePanelAdd.QuotePanelAdd(self.stack,db,self.view))
        self.stack.addWidget(AuthorPanelAdd.AuthorPanelAdd(self.stack,db,self.view))
        self.stack.addWidget(self.view)
        self.stack.setCurrentIndex(3)
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.stack)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.book_button.clicked.connect(self.show_book_panel)
        self.quote_button.clicked.connect(self.show_quote_panel)
        self.author_button.clicked.connect(self.show_author_panel)
        self.stack.currentChanged.connect(self.setButtons)
    def resetButtons(self):
        self.book_button.setStyleSheet("")
        self.quote_button.setStyleSheet("")
        self.author_button.setStyleSheet("")

    def setButtons(self, index: int):
        if not index == 7:
            self.resetButtons()
        if index == 0:
            self.author_button.setStyleSheet("QPushButton { background-color: #ED650A; }")
        elif index == 1:
            self.book_button.setStyleSheet("QPushButton { background-color: #ED650A; }")
        elif index == 2:
            self.quote_button.setStyleSheet("QPushButton { background-color: #ED650A; }")
        elif index == 3:
            #panel
            print()
        elif index == 4:
            self.book_button.setStyleSheet("QPushButton { background-color: #0C8728; }")
        elif index == 5:
            self.quote_button.setStyleSheet("QPushButton { background-color: #0C8728; }")
        elif index == 6:
            self.author_button.setStyleSheet("QPushButton { background-color: #0C8728; }")

    def show_book_panel(self):
        """Switch to the book management panel"""
        self.stack.setCurrentIndex(4)

    def show_quote_panel(self):
        """Switch to the quote management panel"""
        self.stack.setCurrentIndex(5)


    def show_author_panel(self):
        """Switch to the author management panel"""
        self.stack.setCurrentIndex(6)


    def back_to_menu(self):
        self.stack.setCurrentIndex(3)
