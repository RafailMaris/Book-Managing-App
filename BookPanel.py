from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QStackedWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QLineEdit, QSizePolicy,
    QFormLayout, QSpacerItem
)
import sys
import DB
class BookPanel(QWidget):
    def __init__(self,stack,db: DB):
        super().__init__()
        layout = QVBoxLayout()

        # Title
        self.addEditBookText = QLabel("Add/Edit Book")
        self.addEditBookText.setFont(QFont('Segoe UI', 30))
        layout.addWidget(self.addEditBookText)

        # Form fields
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Book title...")

        self.author_edit = QLineEdit()
        self.author_edit.setPlaceholderText("Author name...")

        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Book description...")
        self.description_edit.setMaximumHeight(150)

        layout.addWidget(QLabel("Title:"))
        layout.addWidget(self.title_edit)
        layout.addWidget(QLabel("Author:"))
        layout.addWidget(self.author_edit)
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.description_edit)

        # Save button
        self.save_button = QPushButton("Save Book")
        layout.addWidget(self.save_button)
        # Add stretch to push everything to top
        layout.addStretch()

        self.setLayout(layout)
