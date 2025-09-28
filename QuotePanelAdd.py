from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton
)

import DB
import PanelView
from Panel import Panel


class QuotePanelAdd(Panel):

    def __init__(self,stack,db: DB, view: PanelView):

        super().__init__()
        layout = QVBoxLayout()

        self.setTitle(layout, "Citate - Add")
        quoteBookAuthorLayout = QHBoxLayout()
        quoteBookLayout = QVBoxLayout()
        quoteAuthorLayout = QVBoxLayout()

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

        self.save_button = QPushButton("Save Quote")

        self.search_button = QPushButton("Search Quote")
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.search_button)
        layout.addLayout(button_layout)
        self.save_button.clicked.connect(lambda: db.addQuote(self))
        self.search_button.clicked.connect(lambda: db.searchQuote(self,stack,view))
        layout.addStretch()
        self.setLayout(layout)
