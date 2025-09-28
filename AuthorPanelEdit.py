from PyQt6.QtSql import QSqlQuery
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout

from Entries import Author
import DB
import PanelView
from Panel import Panel


class AuthorPanelEdit(Panel):
    def __init__(self,stack,db: DB, panelView: PanelView):
        super().__init__()
        layout = QVBoxLayout()

        self.panelView = panelView
        self.previousName =""
        self.previousID = ""
        self.command = ""
        self.setTitle(layout, "Autor - Edit")
        self.setLabel(layout,"Nume")
        self.author_text = self.setLineEdit(layout,self.WIDTH)
        self.author_error = self.setError(layout)
        self.setLabel(layout,"Notițe")
        self.notes_text = self.setText(layout)

        self.notes_error = self.setError(layout)
        self.save_button = QPushButton("Edit")
        self.save_button.clicked.connect(lambda: self.saveChanges(db))
        self.search_button = QPushButton("Back to search")
        self.search_button.clicked.connect(lambda: self.returnToSearch(stack,panelView))
        self.buttons = QHBoxLayout()
        self.buttons.addWidget(self.save_button)
        self.buttons.addWidget(self.search_button)
        layout.addLayout(self.buttons)
        layout.addStretch()
        self.setLayout(layout)

    def setData(self,name: str,notes: str,identificator: str, command: str):
        self.command = command
        self.previousID = identificator
        self.author_text.setText(name)
        self.notes_text.setText(notes)
        self.previousName = name
        self.clearErrors("author",self)

    def saveChanges(self,db: DB):
        author = Author.Author(str(self.author_text.text()).strip(), str(self.notes_text.toPlainText()).strip())
        changedName = False
        if self.previousName != author.name:
            changedName = True
        db.updateDB(self,"author",author,self.previousID,changedName)

    def returnToSearch(self,stack,view: PanelView):

        model = self.panelView.table.model()
        new_query = QSqlQuery(self.command)
        model.setQuery(new_query)
        view.prepareContent(model, "authors", self.command)
        stack.setCurrentIndex(7)



