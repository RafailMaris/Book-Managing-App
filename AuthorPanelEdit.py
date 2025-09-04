from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtSql import QSqlQuery
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QHBoxLayout

import Author
import DB
from Panel import Panel
import MainWindow
import PanelView


class AuthorPanelEdit(Panel):
    def __init__(self,stack,db: DB, panelView: PanelView):
        self.panelView = panelView
        self.originalName =""
        layout = QVBoxLayout()
        super().__init__()
        self.previousID = ""
        self.command = ""
        self.title_label = self.setTitle(layout, "Autor - Edit")
        self.author_label = self.setLabel(layout,"Nume")
        self.author_text = self.setLineEdit(layout,self.WIDTH)
        self.author_error = self.setError(layout)
        self.notes_label = self.setLabel(layout,"Notițe")
        self.notes_text = self.setText(layout)

        self.notes_error = self.setError(layout)
        self.save_button = QPushButton("Edit")
        self.save_button.clicked.connect(lambda: self.saveChanges(db))
        self.search_button = QPushButton("Back to Menu")
        self.search_button.clicked.connect(lambda: self.returnToAdd(stack))
        self.buttons = QHBoxLayout()
        self.buttons.addWidget(self.save_button)
        self.buttons.addWidget(self.search_button)
        layout.addLayout(self.buttons)
        layout.addStretch()
        self.setLayout(layout)

    def setData(self,name: str,notes: str,id: str, command: str):
        self.command = command
        self.previousID = id
        self.author_text.setText(name)
        self.notes_text.setText(notes)

    def saveChanges(self,db: DB):
        author = Author.Author(str(self.author_text.text()).strip(),str(self.notes_text.toPlainText()).strip())
        print(author.name,author.notes)
        changedName = False
        if self.originalName != author.name:
            changedName = True
        db.updateDB(self,"author",author,self.previousID,changedName)

    def returnToAdd(self,stack):
        stack.setCurrentIndex(5)
        model = self.panelView.table.model()
        print(self.command)
        new_query = QSqlQuery(self.command)
        model.setQuery(new_query)



