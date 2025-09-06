from PyQt6.QtGui import QFont
from PyQt6.QtSql import QSqlQuery
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit, QHBoxLayout
)

import DB
from Book import Book
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

        # Titlul panel ului
        self.setTitle(layout,"Carti - Edit")
        #in DB: titlu, autor, notite
        # Titlu carte
        self.setLabel(layout, "Titlu")
        self.bookTitleText = self.setLineEdit(layout, self.WIDTH)
        self.bookTitleError = self.setError(layout)
        # autor
        self.setLabel(layout, "Autor")
        self.bookAuthorText = self.setLineEdit(layout, self.WIDTH)
        self.bookAuthorError = self.setError(layout)
        # notite
        self.setLabel(layout, "Notite")
        self.bookNotesText = self.setText(layout)
        self.bookNotesError = self.setError(layout)

        # Save button
        self.buttons = QHBoxLayout()
        self.save_button = QPushButton("Edit")
        self.search_button = QPushButton("Back to search")
        self.buttons.addWidget(self.save_button)
        self.save_button.clicked.connect(lambda: self.saveChanges(db))
        self.search_button.clicked.connect(lambda: self.returnToAdd(stack))
        self.buttons.addWidget(self.search_button)
        layout.addLayout(self.buttons)
        # Add stretch to push everything to top
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
            print('changed')
        db.updateDB(self,"books",book,self.previousId,changed)
    def returnToAdd(self,stack):
        stack.setCurrentIndex(7)
        model = self.panelView.table.model()
        newQuery = QSqlQuery(self.command)
        model.setQuery(newQuery)