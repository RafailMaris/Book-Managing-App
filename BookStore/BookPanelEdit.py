from PyQt6.QtWidgets import QPushButton
from PyQt6.QtSql import QSqlQuery
from BookStore.PanelView import PanelView
from BookStore.LogicLevel import LogicLevel
from BookPanelBase import BookPanelBase


class BookPanelEdit(BookPanelBase):
    def __init__(self, stack, logicalLevel: LogicLevel, panelView: PanelView):
        self.command = ""
        self.previousTitle = ""
        self.previousAuthor = ""
        self.previousId = ""
        self.panelView = panelView

        super().__init__(logicalLevel, "Carti - Edit")

        self.saveButton = QPushButton("Edit")
        self.backButton = QPushButton("Back to search")

        self.saveButton.clicked.connect(self.saveChanges)
        self.backButton.clicked.connect(
            lambda: self.returnToAdd(stack, panelView)
        )

        self.buttons.addWidget(self.saveButton)
        self.buttons.addWidget(self.backButton)

    def setData(self, title, author, notes, identifier, command):
        super().setDataBase(title, author, notes)
        self.previousTitle = title
        self.previousAuthor = author
        self.previousId = identifier
        self.command = command

    def saveChanges(self):
        self.logicalLevel.saveChangesBPE(self)

    def returnToAdd(self, stack, view: PanelView):
        model = self.panelView.table.model()
        model.setQuery(QSqlQuery(self.command))
        view.prepareContent(model, "books", self.command)
        stack.setCurrentIndex(7)
