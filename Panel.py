from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QStackedWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QLineEdit, QSizePolicy,
    QFormLayout, QSpacerItem, QFrame
)
class Panel(QWidget):
    LABEL_FONT = QFont('Google Sans', 18)
    TEXT_FONT = QFont('Google Sans', 16)
    INFO_FONT = QFont('Google Sans', 12)
    WIDTH = 400
    SPACING = 20
    ERROR_STYLE = "color: red; font-size: 12px;"
    def __init__(self):
        super().__init__()
    def setTitle(self,layout,title) -> QLabel:
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont('Google Sans', 30))
        layout.addWidget(title_label)
        return title_label

    def setLabel(self,layout,text) -> QLabel:
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFont(self.LABEL_FONT)
        label.setText(text)
        layout.addWidget(label)
        return label

    def setText(self, layout) -> QTextEdit:
        text_field = QTextEdit()
        text_field.setFont(self.TEXT_FONT)
        layout.addWidget(text_field)
        return text_field

    def setLineEdit(self,layout,width) -> QLineEdit:
        text_field = QLineEdit()
        text_field.setFont(self.TEXT_FONT)
        text_field.setFixedWidth(width)
        layout.addWidget(text_field,alignment=Qt.AlignmentFlag.AlignCenter)
        return text_field

    def setError(self,layout) -> QLabel:
        error = QLabel()
        error.setStyleSheet(self.ERROR_STYLE)
        layout.addWidget(error, alignment = Qt.AlignmentFlag.AlignCenter)
        return error

    def showError(self, errorType: str, message: str, panelType: str, p):
        if panelType == "quote":
            if errorType == "start":
                p.start_error.setText(message)
            elif errorType == "end":
                p.end_error.setText(message)
            elif errorType == "author":
                p.author_error.setText(message)
            elif errorType == "title":
                p.book_title_error.setText(message)
            elif errorType == "kw":
                p.keywords_error.setText(message)
        elif panelType == "author":
            if errorType == "name":
                p.author_error.setText(message)
            elif errorType == "notes":
                p.notes_error.setText(message)

    def clearErrors(self, panelType: str, p):
        if panelType == "quote":
            p.start_error.setText("")
            p.end_error.setText("")
            p.author_error.setText("")
            p.book_title_error.setText("")
            p.keywords_error.setText("")
        elif panelType == "author":
            p.author_error.setText("")
            p.notes_error.setText("")
        elif panelType == "book":
            print('a')



