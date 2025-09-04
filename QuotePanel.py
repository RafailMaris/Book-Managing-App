from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

import DB
from Panel import Panel
import TextValidation


class QuotePanel(Panel):

    def __init__(self,stack,db: DB):

        super().__init__()
        layout = QVBoxLayout()
        # Title of panel
        # self.title_label = QLabel("Citate")
        # self.title_label.setFont(QFont('Google Sans', 30))
        # self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # layout.addWidget(self.title_label)
        self.title_label = self.setTitle(layout, "Citate")

        # Book title
        self.book_title_text = QLineEdit()
        self.book_title_error = QLabel()
        layout.addLayout(self.initBookTitle())
        # Author
        self.author_text = QLineEdit()
        self.author_error = QLabel()
        self.initAuthor(layout)
        # Quote
        self.quote = QVBoxLayout()
        self.quote_label = QLabel("Citat")
        self.quote_label.setFont(self.LABEL_FONT)
        self.quote_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.quote_text = QTextEdit()
        self.quote_text.setFont(self.TEXT_FONT)

        self.quote.addWidget(self.quote_label)
        self.quote.addWidget(self.quote_text)
        layout.addLayout(self.quote)

        # Start/End layout
        self.start_end_layout = QHBoxLayout()

        # Start column
        self.start_column = QVBoxLayout()

        self.start_label = QLabel("Start")
        self.start_label.setFont(self.LABEL_FONT)
        self.start_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #TODO page label si page text trebuie sa aiba sub ele un error
        self.start_page_label = QLabel("Pagină:")
        self.start_page_label.setFont(self.TEXT_FONT)

        self.start_row_label = QLabel("Rând:")
        self.start_row_label.setFont(self.TEXT_FONT)

        self.start_page_text = QLineEdit()
        self.start_page_text.setFont(self.TEXT_FONT)

        self.start_row_text = QLineEdit()
        self.start_row_text.setFont(self.TEXT_FONT)

        self.start_text_edit = QHBoxLayout()
        self.start_text_edit.addWidget(self.start_page_label)
        self.start_text_edit.addWidget(self.start_page_text)
        self.start_text_edit.addWidget(self.start_row_label)
        self.start_text_edit.addWidget(self.start_row_text)

        self.start_column.addWidget(self.start_label)
        self.start_column.addLayout(self.start_text_edit)

        self.start_error = QLabel()
        self.start_error.setStyleSheet(self.ERROR_STYLE)
        self.start_error.setText("")

        self.start_column.addWidget(self.start_error,alignment=Qt.AlignmentFlag.AlignCenter)
        # End column
        self.end_column = QVBoxLayout()
        self.end_label = QLabel("Sfârșit")
        self.end_label.setFont(self.LABEL_FONT)
        self.end_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.end_page_label = QLabel("Pagină:")
        self.end_page_label.setFont(self.TEXT_FONT)
        self.end_row_label = QLabel("Rând:")
        self.end_row_label.setFont(self.TEXT_FONT)
        self.end_page_text = QLineEdit()
        self.end_page_text.setFont(self.TEXT_FONT)
        self.end_row_text = QLineEdit()
        self.end_row_text.setFont(self.TEXT_FONT)

        self.end_text_edit = QHBoxLayout()
        self.end_text_edit.addWidget(self.end_page_label)
        self.end_text_edit.addWidget(self.end_page_text)
        self.end_text_edit.addWidget(self.end_row_label)
        self.end_text_edit.addWidget(self.end_row_text)

        self.end_column.addWidget(self.end_label)
        self.end_column.addLayout(self.end_text_edit)

        self.end_error = QLabel()
        self.end_error.setStyleSheet(self.ERROR_STYLE)
        self.end_error.setText("")

        self.end_column.addWidget(self.end_error,alignment=Qt.AlignmentFlag.AlignCenter)
        # Add both to layout
        self.start_end_layout.addLayout(self.start_column)
        self.start_end_layout.addSpacing(self.SPACING)
        self.start_end_layout.addLayout(self.end_column)
        layout.addLayout(self.start_end_layout)

        # Keywords
        self.keywords_label = QLabel("Cuvinte cheie")
        self.keywords_label.setFont(self.LABEL_FONT)
        self.keywords_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.keywords_text = QHBoxLayout()
        self.keywords = QVBoxLayout()
        self.keyword1 = QLineEdit(); self.keyword1.setFont(self.TEXT_FONT)
        self.keyword2 = QLineEdit(); self.keyword2.setFont(self.TEXT_FONT)
        self.keyword3 = QLineEdit(); self.keyword3.setFont(self.TEXT_FONT)
        self.keyword4 = QLineEdit(); self.keyword4.setFont(self.TEXT_FONT)
        self.keyword5 = QLineEdit(); self.keyword5.setFont(self.TEXT_FONT)
        self.keywords_text.addWidget(self.keyword1)
        self.keywords_text.addWidget(self.keyword2)
        self.keywords_text.addWidget(self.keyword3)
        self.keywords_text.addWidget(self.keyword4)
        self.keywords_text.addWidget(self.keyword5)

        self.keywords_error = QLabel()
        self.keywords_error.setStyleSheet(self.ERROR_STYLE)
        self.keywords_error.setText("")
        self.keywords.addLayout(self.keywords_text)
        self.keywords.addWidget(self.keywords_error,alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.keywords_label)
        layout.addLayout(self.keywords)

        # Notes
        self.personal_notes_label = QLabel("Notițe")
        self.personal_notes_label.setFont(self.LABEL_FONT)
        self.personal_notes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.personal_notes_text_edit = QTextEdit()
        self.personal_notes_text_edit.setFont(self.TEXT_FONT)
        layout.addWidget(self.personal_notes_label)
        layout.addWidget(self.personal_notes_text_edit)

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
    def initBookTitle(self):
        book_title = QVBoxLayout()

        book_title_label = QLabel("Titlu")
        book_title_label.setFont(self.LABEL_FONT)
        book_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.book_title_text.setFont(self.TEXT_FONT)
        self.book_title_text.setFixedWidth(self.WIDTH)
        #self.book_title_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.book_title_error.setStyleSheet(self.ERROR_STYLE)
        self.book_title_error.setText("")

        book_title.addWidget(book_title_label)
        book_title.addWidget(self.book_title_text, alignment=Qt.AlignmentFlag.AlignCenter)
        book_title.addWidget(self.book_title_error, alignment=Qt.AlignmentFlag.AlignCenter)
        return book_title


    def initAuthor(self,layout):
        author = QVBoxLayout()

        author_label = QLabel("Autor")
        author_label.setFont(self.LABEL_FONT)
        author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.author_text.setFont(self.TEXT_FONT)
        self.author_text.setFixedWidth(self.WIDTH)

        self.author_error.setStyleSheet(self.ERROR_STYLE)
        self.author_error.setText("")

        author.addWidget(author_label)
        author.addWidget(self.author_text, alignment=Qt.AlignmentFlag.AlignCenter)
        author.addWidget(self.author_error, alignment=Qt.AlignmentFlag.AlignCenter)
        # layout.addWidget(self.author_label)
        # layout.addWidget(self.author_text, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(author)



    def prepareSearch(self,stack,db):
        #TODO un panel in care sa poti afisa doar tabelul. unul general, sau cate unul pentru fiecare tabel?
        db.searchQuote(stack)




#fwevw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrhvw4egehrh
