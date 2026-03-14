from PyQt6.QtWidgets import QPushButton
from PyQt6.QtSql import QSqlQuery
from BookStore.Entries import Quote
from BookStore.PanelView import PanelView
from QuotePanelBase import QuotePanelBase


class QuotePanelEdit(QuotePanelBase):
    def __init__(self, stack, logicalLevel, panelView: PanelView):
        super().__init__(logicalLevel, "Citate - Edit")

        self.panelView = panelView
        self.previousQuote = None
        self.previousId = None
        self.command = ""

        self.save_button = QPushButton("Edit Quote")
        self.search_button = QPushButton("Search Quote")

        self.save_button.clicked.connect(self.saveChanges)
        self.search_button.clicked.connect(
            lambda: self.returnToSearch(stack, panelView)
        )

        self.buttons.addWidget(self.save_button)
        self.buttons.addWidget(self.search_button)

    def setData(self, q: Quote, command: str, previousId: int):
        self.previousQuote = q
        self.previousId = previousId
        self.command = command
        self.clearAllErrors()

        self.quoteBookTitleText.setText(q.bookTitle)
        self.quoteAuthorText.setText(q.author)
        self.quoteStartPageText.setText(q.startPage)
        self.quoteEndPageText.setText(q.endPage)
        self.quoteStartRowText.setText(q.startRow)
        self.quoteEndRowText.setText(q.endRow)
        self.quoteText.setText(q.quote)
        self.quoteNotesText.setText(q.notes)

        genres = q.genres.split(",")
        kws = [""] * 5
        for g in genres[-5:]:
            kws = kws[1:] + [g]

        self.keyword5.setText(kws[0])
        self.keyword4.setText(kws[1])
        self.keyword3.setText(kws[2])
        self.keyword2.setText(kws[3])
        self.keyword1.setText(kws[4])

    def saveChanges(self):
        self.logicalLevel.saveChangesQPE(self)

    def returnToSearch(self, stack, view: PanelView):
        model = self.panelView.table.model()
        model.setQuery(QSqlQuery(self.command))
        view.prepareContent(model, "quotes", self.command)
        stack.setCurrentIndex(7)
