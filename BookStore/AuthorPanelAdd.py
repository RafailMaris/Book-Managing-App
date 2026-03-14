from PyQt6.QtWidgets import QPushButton
from PanelView import PanelView
from AuthorPanelBase import AuthorPanelBase


class AuthorPanelAdd(AuthorPanelBase):
    def __init__(self, stack, logicalLevel, view: PanelView):
        super().__init__(logicalLevel, "Autor - Add")

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(
            lambda: self.logicalLevel.addAuthor(self)
        )

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(
            lambda: self.logicalLevel.searchAuthor(stack, self, view)
        )

        self.buttons.addWidget(self.save_button)
        self.buttons.addWidget(self.search_button)
