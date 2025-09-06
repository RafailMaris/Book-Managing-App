from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout

import DB
from PanelView import PanelView
from Panel import Panel

class AuthorPanelAdd(Panel):
    def __init__(self,stack,db: DB, view: PanelView):
        layout = QVBoxLayout()
        super().__init__()
        self.title_label = self.setTitle(layout, "Autor - Add")
        self.author_label = self.setLabel(layout,"Nume")
        self.author_text = self.setLineEdit(layout,self.WIDTH)
        self.author_error = self.setError(layout)
        self.notes_label = self.setLabel(layout,"Notițe")
        self.notes_text = self.setText(layout)

        self.notes_error = self.setError(layout)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(lambda: db.addAuthors(self))
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(lambda: db.searchAuthors(stack,self,view))
        self.buttons = QHBoxLayout()
        self.buttons.addWidget(self.save_button)
        self.buttons.addWidget(self.search_button)
        layout.addLayout(self.buttons)
        layout.addStretch()
        self.setLayout(layout)


