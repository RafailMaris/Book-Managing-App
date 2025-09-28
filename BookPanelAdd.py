from PyQt6.QtWidgets import (
    QVBoxLayout, QPushButton, QHBoxLayout
)

import DB
import PanelView
from Panel import Panel


class BookPanelAdd(Panel):
    def __init__(self,stack,db: DB, panelView: PanelView):
        super().__init__()
        layout = QVBoxLayout()

        self.setTitle(layout,"Carti - Add")

        self.setLabel(layout,"Titlu")
        self.bookTitleText = self.setLineEdit(layout,self.WIDTH)
        self.bookTitleError = self.setError(layout)

        self.setLabel(layout,"Autor")
        self.bookAuthorText = self.setLineEdit(layout,self.WIDTH)
        self.bookAuthorError = self.setError(layout)

        self.setLabel(layout,"Notite")
        self.bookNotesText = self.setText(layout)
        self.bookNotesError = self.setError(layout)

        self.buttons = QHBoxLayout()
        self.saveButton = QPushButton("Save")
        self.searchButton = QPushButton("Search")
        self.buttons.addWidget(self.saveButton)
        self.buttons.addWidget(self.searchButton)
        self.saveButton.clicked.connect(lambda: db.addBooks(self))
        self.searchButton.clicked.connect(lambda: db.searchBooks(stack,self,panelView))
        layout.addLayout(self.buttons)

        layout.addStretch()

        self.setLayout(layout)
