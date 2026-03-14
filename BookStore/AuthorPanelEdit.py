from PyQt6.QtWidgets import QPushButton
from PyQt6.QtSql import QSqlQuery
from BookStore.Entries import Author
from AuthorPanelBase import AuthorPanelBase
from PanelView import PanelView


class AuthorPanelEdit(AuthorPanelBase):
    def __init__(self, stack, logicalLevel, panelView: PanelView):
        super().__init__(logicalLevel, "Autor - Edit")

        self.panelView = panelView
        self.previousName = ""
        self.previousID = ""
        self.command = ""

        self.save_button = QPushButton("Edit")
        self.save_button.clicked.connect(self.saveChanges)

        self.search_button = QPushButton("Back to search")
        self.search_button.clicked.connect(
            lambda: self.returnToSearch(stack, panelView)
        )

        self.buttons.addWidget(self.save_button)
        self.buttons.addWidget(self.search_button)

    def setData(self, name: str, notes: str, identificator: str, command: str):
        super().setDataBase(name, notes)
        self.previousID = identificator
        self.previousName = name
        self.command = command

    def saveChanges(self):
        author = Author.Author(
            self.author_text.text().strip(),
            self.notes_text.toPlainText().strip()
        )
        self.logicalLevel.saveChangesAPE(author, self)

    def returnToSearch(self, stack, view: PanelView):
        model = self.panelView.table.model()
        model.setQuery(QSqlQuery(self.command))
        view.prepareContent(model, "authors", self.command)
        stack.setCurrentIndex(7)
