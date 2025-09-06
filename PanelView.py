from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel, QSqlQueryModel
from PyQt6.QtWidgets import QWidget, QTableView, QVBoxLayout, QHeaderView, QAbstractItemView, QPushButton

import AuthorPanelEdit
import BookPanelEdit
import DB
from Author import Author
from Panel import Panel

import QuotePanelEdit


class PanelView(Panel):
    def __init__(self,stack, db: DB):
        super().__init__()
        self.currentType = ""
        self.command = ""
        self.stack = stack
        self.authorPanelEdit = AuthorPanelEdit.AuthorPanelEdit(stack,db,self)
        self.stack.addWidget(self.authorPanelEdit)  # 0

        self.bookPanelEdit = BookPanelEdit.BookPanelEdit(stack,db,self)
        self.stack.addWidget(self.bookPanelEdit) #1

        self.quotePanelEdit = QuotePanelEdit.QuotePanelEdit(stack,db,self)
        self.stack.addWidget(self.quotePanelEdit) #2
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.table = QTableView()
        self.table.resizeColumnsToContents()
        self.table.setAlternatingRowColors(True)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.setStyleSheet("""
            QTableView::item:selected { background-color: transparent; }
            QTableView::item:hover { background-color: transparent; }
            QtableView {
            grid-line-width: 3px;
            }
        """)

        self.table.setFont(self.TEXT_FONT)

        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.table.setVerticalScrollMode(QTableView.ScrollMode.ScrollPerPixel)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.table.setHorizontalScrollMode(QTableView.ScrollMode.ScrollPerPixel)
        self.table.setWordWrap(True)
        self.table.setShowGrid(True)
        self.table.setFixedWidth(964)

        header = self.table.horizontalHeader()
        vheader = self.table.verticalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)  # allows manual sizing


        # let the "notes" column stretch
        #header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        vheader.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.layout.addWidget(self.table)
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.delete_row)
        self.table.doubleClicked.connect(self.setToEdit)

        self.layout.addWidget(self.deleteButton)

    def prepareContent(self,model: QSqlQueryModel, type: str, command: str):
        self.command = command
        self.table.setModel(model)
        self.table.resizeColumnsToContents()
        self.currentType = type
        if type == "authors":
            self.setAuthorView()
        elif type == "books":
            self.setBookView()

    def setAuthorView(self):
        header = self.table.horizontalHeader()

        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 50)  # ID
        self.table.setColumnWidth(1, 150)  # Name

        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

    def setBookView(self):
        header = self.table.horizontalHeader()

        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 150)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
    def setToEdit(self,index):
        model = self.table.model()
        row = index.row()
        if self.currentType == "authors":
            identifier = str(model.index(row, 0).data())
            name = str(model.index(row, 1).data())
            notes = str(model.index(row, 2).data())
            self.authorPanelEdit.setData(name, notes,identifier,self.command)
            self.stack.setCurrentIndex(0)
            print(name)
        if self.currentType == "books":
            identifier = str(model.index(row, 0).data())
            title = str(model.index(row, 1).data())
            author = str(model.index(row, 2).data())
            notes = str(model.index(row, 3).data())
            self.bookPanelEdit.setData(title,author, notes,identifier,self.command)
            self.stack.setCurrentIndex(1)
            print(title)

    def delete_row(self):
        selected = self.table.selectionModel().selectedRows()
        model = self.table.model()

        for index in selected:
            value = str(index.sibling(index.row(), 0).data())
            query = QSqlQuery()
            sql = f"DELETE FROM {self.currentType} WHERE ID = ?"
            print(sql)
            query.prepare(sql)
            query.addBindValue(value)
            if not query.exec():
                print("Delete failed:", query.lastError().text())
            else:
                print(f"Deleted {value}")

        if isinstance(model, QSqlQueryModel):
            print(self.command)
            new_query = QSqlQuery(self.command)
            model.setQuery(new_query)






