from PyQt6.QtSql import QSqlQuery
from PyQt6.QtWidgets import (
    QVBoxLayout, QPushButton, QHBoxLayout
)

import DB
from Entries.Book import Book
from Panel import Panel
import PanelView


class BookPanelEdit(Panel):
    def __init__(self,stack,db: DB, panelView: PanelView):
        self.command = ""
        self.previousTitle = ""
        self.previousAuthor = ""
        self.previousId = ""
        self.panelView = panelView
        super().__init__()
        layout = QVBoxLayout()


        self.setTitle(layout,"Carti - Edit")

        self.setLabel(layout, "Titlu")
        self.bookTitleText = self.setLineEdit(layout, self.WIDTH)
        self.bookTitleError = self.setError(layout)

        self.setLabel(layout, "Autor")
        self.bookAuthorText = self.setLineEdit(layout, self.WIDTH)
        self.bookAuthorError = self.setError(layout)

        self.setLabel(layout, "Notite")
        self.bookNotesText = self.setText(layout)
        self.bookNotesError = self.setError(layout)

        self.buttons = QHBoxLayout()
        self.save_button = QPushButton("Edit")
        self.search_button = QPushButton("Back to search")
        self.buttons.addWidget(self.save_button)
        self.save_button.clicked.connect(lambda: self.saveChanges(db))
        self.search_button.clicked.connect(lambda: self.returnToAdd(stack,panelView))
        self.buttons.addWidget(self.search_button)
        layout.addLayout(self.buttons)

        layout.addStretch()

        self.setLayout(layout)
    def setData(self,title,author,notes,identifier,command):
        self.bookTitleText.setText(title)
        self.bookNotesText.setText(notes)
        self.bookAuthorText.setText(author)
        self.previousTitle = title
        self.previousAuthor = author
        self.previousId = identifier
        self.command = command
        self.clearErrors("books",self)

    def saveChanges(self,db:DB):
        currentTitle = str(self.bookTitleText.text()).strip()
        currentAuthor = str(self.bookAuthorText.text()).strip()
        currentNotes = str(self.bookNotesText.toPlainText()).strip()
        book = Book(currentTitle,currentAuthor,currentNotes)
        changed = False
        if self.previousTitle != currentTitle or self.previousAuthor != currentAuthor:
            changed = True
        db.updateDB(self,"books",book,self.previousId,changed)

    def returnToAdd(self,stack,view: PanelView):
        model = self.panelView.table.model()
        newQuery = QSqlQuery(self.command)
        model.setQuery(newQuery)
        view.prepareContent(model, "books", self.command)
        stack.setCurrentIndex(7)