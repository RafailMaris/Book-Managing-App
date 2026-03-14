from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from BookStore.Panel import Panel


class QuotePanelBase(Panel):
    def __init__(self, logicalLevel, title: str):
        super().__init__(logicalLevel)

        self.layout = QVBoxLayout()
        self.setTitle(self.layout, title)

        # Book + Author
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
        self.layout.addLayout(quoteBookAuthorLayout)

        # Quote text
        self.setLabel(self.layout, "Citat")
        self.quoteText = self.setText(self.layout)
        self.quoteError = self.setError(self.layout)

        # Start / End
        quoteStartEndLayout = QHBoxLayout()

        # Start
        quoteStartColumn = QVBoxLayout()
        self.setLabel(quoteStartColumn, "Start")
        quoteStartLayout = QHBoxLayout()
        self.setLabel(quoteStartLayout, "Pagină:")
        self.quoteStartPageText = self.setLineEditPage(quoteStartLayout)
        self.setLabel(quoteStartLayout, "Rând:")
        self.quoteStartRowText = self.setLineEditPage(quoteStartLayout)
        quoteStartColumn.addLayout(quoteStartLayout)
        self.quoteStartError = self.setError(quoteStartColumn)

        # End
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
        self.layout.addLayout(quoteStartEndLayout)

        # Keywords
        self.setLabel(self.layout, "Cuvinte cheie")
        self.quoteKeywordsLayout = QHBoxLayout()
        self.keyword1 = self.setLineEditPage(self.quoteKeywordsLayout)
        self.keyword2 = self.setLineEditPage(self.quoteKeywordsLayout)
        self.keyword3 = self.setLineEditPage(self.quoteKeywordsLayout)
        self.keyword4 = self.setLineEditPage(self.quoteKeywordsLayout)
        self.keyword5 = self.setLineEditPage(self.quoteKeywordsLayout)
        self.layout.addLayout(self.quoteKeywordsLayout)
        self.quoteKeywordError = self.setError(self.layout)

        # Notes
        self.setLabel(self.layout, "Notițe")
        self.quoteNotesText = self.setText(self.layout)
        self.quoteNotesError = self.setError(self.layout)

        # Buttons placeholder
        self.buttons = QHBoxLayout()
        self.layout.addLayout(self.buttons)

        self.layout.addStretch()
        self.setLayout(self.layout)

    def clearAllErrors(self):
        self.clearErrors("quote", self)
