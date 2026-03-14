from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout
from Panel import Panel
from PanelView import PanelView


class AuthorPanelBase(Panel):
    def __init__(self, logicalLevel, title: str):
        super().__init__(logicalLevel)

        self.layout = QVBoxLayout()
        self.setTitle(self.layout, title)

        # Nume
        self.setLabel(self.layout, "Nume")
        self.author_text = self.setLineEdit(self.layout, self.WIDTH)
        self.author_error = self.setError(self.layout)

        # Notitele
        self.setLabel(self.layout, "Notițe")
        self.notes_text = self.setText(self.layout)
        self.notes_error = self.setError(self.layout)

        # Butts
        self.buttons = QHBoxLayout()
        self.layout.addLayout(self.buttons)

        self.layout.addStretch()
        self.setLayout(self.layout)

    def setDataBase(self, name: str, notes: str):
        self.author_text.setText(name)
        self.notes_text.setText(notes)
        self.clearErrors("author", self)
