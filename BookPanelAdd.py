from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit, QHBoxLayout
)

import DB
from Panel import Panel
import PanelView


class BookPanelAdd(Panel):
    def __init__(self,stack,db: DB, panelView: PanelView):
        super().__init__()
        layout = QVBoxLayout()

        # Titlul panel ului
        self.setTitle(layout,"Carti - Add")
        #in DB: titlu, autor, notite
        # Titlu carte
        self.setLabel(layout,"Titlu")
        self.bookTitleText = self.setLineEdit(layout,self.WIDTH)
        self.bookTitleError = self.setError(layout)
        #autor
        self.setLabel(layout,"Autor")
        self.bookAuthorText = self.setLineEdit(layout,self.WIDTH)
        self.bookAuthorError = self.setError(layout)
        #notite
        self.setLabel(layout,"Notite")
        self.bookNotesText = self.setText(layout)
        self.bookNotesError = self.setError(layout)
        # Save button
        self.buttons = QHBoxLayout()
        self.saveButton = QPushButton("Save")
        self.searchButton = QPushButton("Search")
        self.buttons.addWidget(self.saveButton)
        self.buttons.addWidget(self.searchButton)
        self.saveButton.clicked.connect(lambda: db.addBooks(self))
        self.searchButton.clicked.connect(lambda: db.searchBooks(stack,self,panelView))
        layout.addLayout(self.buttons)
        # Add stretch to push everything to top
        layout.addStretch()

        self.setLayout(layout)
