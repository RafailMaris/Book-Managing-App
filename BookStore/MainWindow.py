from sqlite3 import Cursor

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QStackedWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QLineEdit, QSizePolicy,
    QFormLayout, QSpacerItem, QMessageBox
)
from PyQt6 import QtWebEngineWidgets
from PyQt6.QtCore import QUrl

import AuthorPanelAdd
import PanelView
import BookPanelAdd
import Panel
import QuotePanelAdd
import DB
import AuthorPanelEdit
from LogicLevel import LogicLevel


# indici
# 0 - authorPanelEdit
# 1 - bookPanelEdit
# 2 - quotePanelEdit
# 3 - Panel
# 4 - book panel
# 5 - quote panel
# 6 - author panel
# 7 - panelview (all in one, type sh)
# 8 - web ul din django


class MainWindow(QMainWindow):
    stack = None

    def __init__(self, db: DB, logicLevel: LogicLevel):

        super().__init__()
        self.setWindowTitle("Book Manager")
        self.logicLevel = logicLevel

        self.book_button = QPushButton("Books")
        self.quote_button = QPushButton("Quotes")
        self.author_button = QPushButton("Authors")
        self.recommendations_button = QPushButton("📚 recommendations")  # NEW
        self.reset_button = QPushButton("Reset")

        self.book_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.quote_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.author_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.recommendations_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.reset_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.author_button)
        button_layout.addWidget(self.book_button)
        button_layout.addWidget(self.quote_button)
        button_layout.addWidget(self.recommendations_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addStretch()

        self.stack = QStackedWidget()
        self.view = PanelView.PanelView(self.stack, logicLevel)
        self.stack.addWidget(Panel.Panel(logicLevel))
        self.bookPanel = BookPanelAdd.BookPanelAdd(self.stack, logicLevel, self.view)
        self.stack.addWidget(self.bookPanel)
        self.quotePanel = QuotePanelAdd.QuotePanelAdd(self.stack, logicLevel, self.view)
        self.stack.addWidget(self.quotePanel)
        self.authorPanel = AuthorPanelAdd.AuthorPanelAdd(self.stack, logicLevel, self.view)
        self.stack.addWidget(self.authorPanel)
        self.stack.addWidget(self.view)

        # Adaugam web
        self.recommendations_web_view = QtWebEngineWidgets.QWebEngineView()
        self.recommendations_web_view.setUrl(QUrl("http://127.0.0.1:8000/accounts/login"))
        self.stack.addWidget(self.recommendations_web_view)

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
        self.recommendations_button.clicked.connect(self.show_recommendations)  # NEW
        self.reset_button.clicked.connect(lambda: self.logicLevel.resetDB())
        self.stack.currentChanged.connect(self.setButtons)

    def resetButtons(self):
        self.book_button.setStyleSheet("")
        self.quote_button.setStyleSheet("")
        self.author_button.setStyleSheet("")
        self.recommendations_button.setStyleSheet("")  # NEW

    def setButtons(self, index: int):
        if not index == 7:
            self.resetButtons()
        if index == 0:
            self.author_button.setStyleSheet("QPushButton { background-color: #ED650A; }")
        elif index == 1:
            self.book_button.setStyleSheet("QPushButton { background-color: #ED650A; }")
        elif index == 2:
            self.quote_button.setStyleSheet("QPushButton { background-color: #ED650A; }")
        elif index == 4:
            self.book_button.setStyleSheet("QPushButton { background-color: #0C8728; }")
        elif index == 5:
            self.quote_button.setStyleSheet("QPushButton { background-color: #0C8728; }")
        elif index == 6:
            self.author_button.setStyleSheet("QPushButton { background-color: #0C8728; }")
        elif index == 8:  # NEW: recommendations panel
            self.recommendations_button.setStyleSheet("QPushButton { background-color: #667eea; }")

    def show_book_panel(self):
        self.bookPanel.clearErrors("books", self.bookPanel)
        self.stack.setCurrentIndex(4)

    def show_quote_panel(self):
        self.quotePanel.clearErrors("quotes", self.quotePanel)
        self.stack.setCurrentIndex(5)

    def show_author_panel(self):
        self.authorPanel.clearErrors("author", self.authorPanel)
        self.stack.setCurrentIndex(6)

    def show_recommendations(self):  # NEW
        """Show the Django recommendations web interface"""
        # Reload the page to ensure fresh content
        current_url = self.recommendations_web_view.url().toString()
        if "login" not in current_url:
            # If already logged in, go to recommendations page
            self.recommendations_web_view.setUrl(QUrl("http://127.0.0.1:8000/"))
        self.stack.setCurrentIndex(8)

    def back_to_menu(self):
        self.stack.setCurrentIndex(3)















