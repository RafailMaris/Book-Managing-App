from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

import DB
import PanelView
from Panel import Panel
import TextValidation


class QuotePanelAdd(Panel):

    def __init__(self,stack,db: DB, panelView: PanelView):

        super().__init__()
        layout = QVBoxLayout()
        # Title of panel
        # self.title_label = QLabel("Citate")
        # self.title_label.setFont(QFont('Google Sans', 30))
        # self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # layout.addWidget(self.title_label)
        titleLabel = self.setTitle(layout, "Citate")
        quoteBookAuthorLayout = QHBoxLayout()
        quoteBookLayout = QVBoxLayout()
        quoteAuthorLayout = QVBoxLayout()
        # Book title
        quoteBookTitleLabel = self.setLabel(quoteBookLayout, "Carte")
        self.quoteBookTitleText = self.setLineEdit(quoteBookLayout, self.WIDTH)
        self.quoteBookTitleError = self.setError(quoteBookLayout)
        # Author
        quoteAuthorLabel = self.setLabel(quoteAuthorLayout, "Autor")
        self.quoteAuthorText = self.setLineEdit(quoteAuthorLayout, self.WIDTH)
        self.quoteAuthorError = self.setError(quoteAuthorLayout)
        quoteBookAuthorLayout.addLayout(quoteBookLayout)
        quoteBookAuthorLayout.addLayout(quoteAuthorLayout)
        layout.addLayout(quoteBookAuthorLayout)
        # Quote
        quoteLabel = self.setLabel(layout, "Citat")
        self.quoteText = self.setText(layout)
        self.quoteError = self.setError(layout)

        # Start/End layout
        quoteStartEndLayout = QHBoxLayout()

        # Start column
        quoteStartColumn = QVBoxLayout()

        quoteStartLabel = self.setLabel(quoteStartColumn, "Start")

        quoteStartLayout = QHBoxLayout()

        quoteStartPageLabel = self.setLabel(quoteStartLayout, "Pagină:")
        self.quoteStartPageText = self.setLineEditPage(quoteStartLayout)
        quoteStartRowLabel = self.setLabel(quoteStartLayout, "Rând:")
        self.quoteStartRowText = self.setLineEditPage(quoteStartLayout)
        quoteStartColumn.addLayout(quoteStartLayout)
        self.quoteStartError = self.setError(quoteStartColumn)

        # End column
        quoteEndColumn = QVBoxLayout()
        quoteEndLabel = self.setLabel(quoteEndColumn, "Sfârșit")
        quoteEndLayout = QHBoxLayout()
        quoteEndPageLabel = self.setLabel(quoteEndLayout, "Pagină:")
        self.quoteEndPageText = self.setLineEditPage(quoteEndLayout)
        quoteEndRowLabel = self.setLabel(quoteEndLayout, "Rând:")
        self.quoteEndRowText = self.setLineEditPage(quoteEndLayout)
        quoteEndColumn.addLayout(quoteEndLayout)
        self.quoteEndError = self.setError(quoteEndColumn)

        # Add both to layout
        quoteStartEndLayout.addLayout(quoteStartColumn)
        quoteStartEndLayout.addLayout(quoteEndColumn)
        layout.addLayout(quoteStartEndLayout)

        # Keywords
        quoteKeywordLabel = self.setLabel(layout, "Cuvinte cheie")
        self.quoteKeywordsText = QHBoxLayout()

        self.keyword1 = self.setLineEditPage(self.quoteKeywordsText)
        self.keyword2 = self.setLineEditPage(self.quoteKeywordsText)
        self.keyword3 = self.setLineEditPage(self.quoteKeywordsText)
        self.keyword4 = self.setLineEditPage(self.quoteKeywordsText)
        self.keyword5 = self.setLineEditPage(self.quoteKeywordsText)
        layout.addLayout(self.quoteKeywordsText)
        self.quoteKeywordError = self.setError(self.quoteKeywordsText)
        # Notes
        quoteNotesLabel = self.setLabel(layout, "Notițe")
        self.quoteNotesText = self.setText(layout)

        # Add / view button
        self.save_button = QPushButton("Save Quote")

        self.search_button = QPushButton("Search Quote")
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.search_button)
        layout.addLayout(button_layout)
        self.save_button.clicked.connect(lambda: db.addQuote(self))
        self.search_button.clicked.connect(lambda: self.prepareSearch(stack,db))
        layout.addStretch()
        self.setLayout(layout)
    #TODO sa facem astea 2 metode mai ok, cica

    def prepareSearch(self,stack,db):
        #TODO un panel in care sa poti afisa doar tabelul. unul general, sau cate unul pentru fiecare tabel?
        db.searchQuote(stack)




#fwevw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrh
