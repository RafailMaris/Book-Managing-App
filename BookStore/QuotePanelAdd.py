from PyQt6.QtWidgets import QPushButton
from BookStore.PanelView import PanelView
from QuotePanelBase import QuotePanelBase


class QuotePanelAdd(QuotePanelBase):
    def __init__(self, stack, logicalLevel, view: PanelView):
        super().__init__(logicalLevel, "Citate - Add")

        self.save_button = QPushButton("Save Quote")
        self.search_button = QPushButton("Search Quote")

        self.save_button.clicked.connect(
            lambda: self.logicalLevel.addQuote(self)
        )
        self.search_button.clicked.connect(
            lambda: self.logicalLevel.searchQuote(self, stack, view)
        )

        self.buttons.addWidget(self.save_button)
        self.buttons.addWidget(self.search_button)
