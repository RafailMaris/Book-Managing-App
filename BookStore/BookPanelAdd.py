from PyQt6.QtWidgets import QPushButton
from BookStore.PanelView import PanelView
from BookStore.LogicLevel import LogicLevel
from BookPanelBase import BookPanelBase


class BookPanelAdd(BookPanelBase):
    def __init__(self, stack, logicalLevel: LogicLevel, panelView: PanelView):
        super().__init__(logicalLevel, "Carti - Add")

        self.saveButton = QPushButton("Save")
        self.searchButton = QPushButton("Search")

        self.saveButton.clicked.connect(
            lambda: self.logicalLevel.dbConnectAddBooks(self)
        )
        self.searchButton.clicked.connect(
            lambda: self.logicalLevel.dbConnectSearchBook(stack, self, panelView)
        )

        self.buttons.addWidget(self.saveButton)
        self.buttons.addWidget(self.searchButton)
