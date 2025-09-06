from PyQt6.QtSql import QSqlQuery
from PyQt6.QtSql import QSqlQuery
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout

import Author
import DB
import PanelView
from Panel import Panel


class AuthorPanelEdit(Panel):
    def __init__(self,stack,db: DB, panelView: PanelView):
        super().__init__()
        self.layout = QVBoxLayout()

        self.panelView = panelView
        self.previousName =""
        self.previousID = ""
        self.command = ""
        self.title_label = self.setTitle(self.layout, "Autor - Edit")
        self.author_label = self.setLabel(self.layout,"Nume")
        self.author_text = self.setLineEdit(self.layout,self.WIDTH)
        self.author_error = self.setError(self.layout)
        self.notes_label = self.setLabel(self.layout,"Notițe")
        self.notes_text = self.setText(self.layout)

        self.notes_error = self.setError(self.layout)
        self.save_button = QPushButton("Edit")
        self.save_button.clicked.connect(lambda: self.saveChanges(db))
        self.search_button = QPushButton("Back to search")
        self.search_button.clicked.connect(lambda: self.returnToAdd(stack))
        self.buttons = QHBoxLayout()
        self.buttons.addWidget(self.save_button)
        self.buttons.addWidget(self.search_button)
        self.layout.addLayout(self.buttons)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def setData(self,name: str,notes: str,id: str, command: str):
        self.command = command
        self.previousID = id
        self.author_text.setText(name)
        self.notes_text.setText(notes)
        self.previousName = name
        self.clearErrors("author",self)

    def saveChanges(self,db: DB):
        author = Author.Author(str(self.author_text.text()).strip(),str(self.notes_text.toPlainText()).strip())
        print(author.name,author.notes)
        changedName = False
        print('og: '+self.previousName+' current: '+author.name)
        if self.previousName != author.name:

            changedName = True
        db.updateDB(self,"author",author,self.previousID,changedName)

    def returnToAdd(self,stack):
        stack.setCurrentIndex(7)
        model = self.panelView.table.model()
        print(self.command)
        new_query = QSqlQuery(self.command)
        model.setQuery(new_query)



