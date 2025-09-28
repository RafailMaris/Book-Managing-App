from PyQt6.QtSql import QSqlQuery
from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton
)

import DB
from Entries import Quote
from Panel import Panel
import PanelView


class QuotePanelEdit(Panel):

    def __init__(self,stack,db: DB, panelView: PanelView):

        super().__init__()
        layout = QVBoxLayout()
        self.panelView = panelView
        self.previousQuote = None
        self.previousId = None

        self.setTitle(layout, "Citate - Edit")
        quoteBookAuthorLayout = QHBoxLayout()
        quoteBookLayout = QVBoxLayout()
        quoteAuthorLayout = QVBoxLayout()
        # Book title
        self.setLabel(quoteBookLayout, "Carte")
        self.quoteBookTitleText = self.setLineEdit(quoteBookLayout, self.WIDTH)
        self.quoteBookTitleError = self.setError(quoteBookLayout)

        self.setLabel(quoteAuthorLayout, "Autor")
        self.quoteAuthorText = self.setLineEdit(quoteAuthorLayout, self.WIDTH)
        self.quoteAuthorError = self.setError(quoteAuthorLayout)
        quoteBookAuthorLayout.addLayout(quoteBookLayout)
        quoteBookAuthorLayout.addLayout(quoteAuthorLayout)
        layout.addLayout(quoteBookAuthorLayout)
        self.setLabel(layout, "Citat")
        self.quoteText = self.setText(layout)
        self.quoteError = self.setError(layout)

        quoteStartEndLayout = QHBoxLayout()

        quoteStartColumn = QVBoxLayout()

        self.setLabel(quoteStartColumn, "Start")

        quoteStartLayout = QHBoxLayout()

        self.setLabel(quoteStartLayout, "Pagină:")
        self.quoteStartPageText = self.setLineEditPage(quoteStartLayout)
        self.setLabel(quoteStartLayout, "Rând:")
        self.quoteStartRowText = self.setLineEditPage(quoteStartLayout)
        quoteStartColumn.addLayout(quoteStartLayout)
        self.quoteStartError = self.setError(quoteStartColumn)

        # End column
        quoteEndColumn = QVBoxLayout()
        self.setLabel(quoteEndColumn, "Sfârșit")
        quoteEndLayout = QHBoxLayout()
        self.setLabel(quoteEndLayout, "Pagină:")
        self.quoteEndPageText = self.setLineEditPage(quoteEndLayout)
        self.setLabel(quoteEndLayout, "Rând:")
        self.quoteEndRowText = self.setLineEditPage(quoteEndLayout)
        quoteEndColumn.addLayout(quoteEndLayout)
        self.quoteEndError = self.setError(quoteEndColumn)

        quoteStartEndLayout.addLayout(quoteStartColumn)
        quoteStartEndLayout.addLayout(quoteEndColumn)
        layout.addLayout(quoteStartEndLayout)

        self.setLabel(layout, "Cuvinte cheie")
        self.quoteKeywordsText = QHBoxLayout()

        self.keyword1 = self.setLineEditPage(self.quoteKeywordsText)
        self.keyword2 = self.setLineEditPage(self.quoteKeywordsText)
        self.keyword3 = self.setLineEditPage(self.quoteKeywordsText)
        self.keyword4 = self.setLineEditPage(self.quoteKeywordsText)
        self.keyword5 = self.setLineEditPage(self.quoteKeywordsText)
        layout.addLayout(self.quoteKeywordsText)
        self.quoteKeywordError = self.setError(layout)

        self.setLabel(layout, "Notițe")
        self.quoteNotesText = self.setText(layout)
        self.quoteNotesError = self.setError(layout)

        self.save_button = QPushButton("Edit Quote")

        self.search_button = QPushButton("Search Quote")
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.search_button)
        layout.addLayout(button_layout)
        self.save_button.clicked.connect(lambda: self.saveChanges(db))
        self.search_button.clicked.connect(lambda: self.returnToSearch(stack,panelView))
        layout.addStretch()
        self.setLayout(layout)

        self.command = ""
    #TODO sa facem astea 2 metode mai ok, cica

    def setData(self, q: Quote, command:str, previousId: int):
        self.previousQuote = q
        self.previousId = previousId
        self.clearErrors("quote",self)
        self.quoteBookTitleText.setText(q.bookTitle)
        self.quoteAuthorText.setText(q.author)
        self.quoteStartPageText.setText(q.startPage)
        self.quoteEndPageText.setText(q.endPage)
        self.quoteStartRowText.setText(q.startRow)
        self.quoteEndRowText.setText(q.endRow)
        self.quoteText.setText(q.quote)
        self.quoteNotesText.setText(q.notes)
        genres = q.genres.split(",")
        kw1,kw2,kw3,kw4,kw5 = "","","","",""
        for genre in genres:
            kw5,kw4,kw3,kw2,kw1 = kw4,kw3,kw2,kw1,genre
        self.keyword1.setText(kw1)
        self.keyword2.setText(kw2)
        self.keyword3.setText(kw3)
        self.keyword4.setText(kw4)
        self.keyword5.setText(kw5)
        self.command = command
    def saveChanges(self,db:DB):
        newTitle = self.quoteBookTitleText.text().strip()
        newAuthor = self.quoteAuthorText.text().strip()
        newStartPage = self.quoteStartPageText.text().strip()
        newEndPage = self.quoteEndPageText.text().strip()
        newStartRow = self.quoteStartRowText.text().strip()
        newEndRow = self.quoteEndRowText.text().strip()
        newQuoteText = self.quoteText.toPlainText().strip()
        newNotes = self.quoteNotesText.toPlainText().strip()
        genres = [self.keyword1.text().strip(),self.keyword2.text().strip(),self.keyword3.text().strip(),self.keyword4.text().strip(),self.keyword5.text().strip()]
        notNullGenres = [s for s in genres if s!=""]
        genreString = ','.join(notNullGenres)
        newQuote = Quote.Quote(newTitle, newAuthor, newStartPage, newStartRow, newEndPage, newEndRow, newQuoteText, newNotes, genreString)
        primaryKeyChanged = False
        if newQuoteText != self.previousQuote.quote or newTitle != self.previousQuote.bookTitle or newAuthor!= self.previousQuote.author:
            primaryKeyChanged = True

        db.updateDB(self,"quotes",newQuote,self.previousId,primaryKeyChanged)

    def returnToSearch(self,stack,view: PanelView):

        model = self.panelView.table.model()
        newQuery = QSqlQuery(self.command)
        model.setQuery(newQuery)
        view.prepareContent(model, "quotes", self.command)
        stack.setCurrentIndex(7)