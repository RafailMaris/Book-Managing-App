from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from BookStore.Panel import Panel


class BookPanelBase(Panel):
    def __init__(self, logicalLevel, title: str):
        super().__init__(logicalLevel)

        self.layout = QVBoxLayout()
        self.setTitle(self.layout, title)

        # Titlu cartii
        self.setLabel(self.layout, "Titlu")
        self.bookTitleText = self.setLineEdit(self.layout, self.WIDTH)
        self.bookTitleError = self.setError(self.layout)

        # Autor
        self.setLabel(self.layout, "Autor")
        self.bookAuthorText = self.setLineEdit(self.layout, self.WIDTH)
        self.bookAuthorError = self.setError(self.layout)

        # Not
        self.setLabel(self.layout, "Notite")
        self.bookNotesText = self.setText(self.layout)
        self.bookNotesError = self.setError(self.layout)

        # Butt fara comenzi
        self.buttons = QHBoxLayout()
        self.layout.addLayout(self.buttons)

        self.layout.addStretch()
        self.setLayout(self.layout)

    def setDataBase(self, title: str, author: str, notes: str):
        self.bookTitleText.setText(title)
        self.bookAuthorText.setText(author)
        self.bookNotesText.setText(notes)
        self.clearErrors("books", self)
