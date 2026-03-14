from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QTextOption
from PyQt6.QtSql import QSqlQueryModel
from PyQt6.QtWidgets import QTableView, QVBoxLayout, QHeaderView, QPushButton, \
    QStyledItemDelegate

from BookStore.Panel import Panel

from BookStore.Entries.Quote import Quote

class TopAlignDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        painter.save()
        text = str(index.data())
        rect = QRectF(option.rect)

        textOption = QTextOption()
        textOption.setWrapMode(QTextOption.WrapMode.WrapAnywhere)  # allow wrapping in the middle of words
        textOption.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        painter.drawText(rect, text, textOption)
        painter.restore()
    def sizeHint(self, option, index):
        text = str(index.data())
        metrics = option.fontMetrics

        # width available for the cell
        width = option.rect.width()

        # calculate required height for wrapped text
        bounding = metrics.boundingRect(
            0, 0, width, 10_000,
            Qt.TextFlag.TextWordWrap,
            text
        )

        return bounding.size()
class PanelView(Panel):
    def __init__(self,stack, logicalLevel):
        super().__init__(logicalLevel)
        self.currentType = ""
        self.command = ""
        self.stack = stack
        from BookStore import AuthorPanelEdit
        self.authorPanelEdit = AuthorPanelEdit.AuthorPanelEdit(stack,logicalLevel, self)
        self.stack.addWidget(self.authorPanelEdit)  # 0
        from BookStore import BookPanelEdit
        self.bookPanelEdit = BookPanelEdit.BookPanelEdit(stack,logicalLevel,self)
        self.stack.addWidget(self.bookPanelEdit) #1
        import QuotePanelEdit
        self.quotePanelEdit = QuotePanelEdit.QuotePanelEdit(stack,logicalLevel,self)
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
        #self.table.setFixedWidth(964)

        header = self.table.horizontalHeader()
        vheader = self.table.verticalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)  # allows manual sizing


        # let the "notes" column stretch
        #header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        vheader.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.layout.addWidget(self.table)
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(lambda: self.delete_row())
        self.table.doubleClicked.connect(self.setToEdit)

        self.layout.addWidget(self.deleteButton)

    def prepareContent(self,model: QSqlQueryModel, type: str, command: str):
        self.command = command
        print(command)
        self.table.setModel(model)
        #self.table.resizeColumnsToContents()
        self.currentType = type
        self.table.resizeRowsToContents()
        header = self.table.horizontalHeader()
        self.table.setColumnHidden(0, True)
        self.table.setItemDelegateForColumn(1, TopAlignDelegate(self.table))
        self.table.setItemDelegateForColumn(2, TopAlignDelegate(self.table))
        self.table.setItemDelegateForColumn(3, TopAlignDelegate(self.table))
        self.table.setItemDelegateForColumn(4, TopAlignDelegate(self.table))
        if type == "quotes":
            self.setQuoteView()
        elif type == "authors":
                self.setAuthorView(header)
        elif type == "books":
            self.setBookView(header)

    def setAuthorView(self,header):

        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)

        self.table.setColumnWidth(1, 300)
        self.table.setColumnWidth(2, 500)
        self.table.setColumnWidth(3, 70)
        self.table.setColumnWidth(4, 70)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)


    def setBookView(self,header):
        #titlu, autor, notite, nr citate
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(1, 500)
        self.table.setColumnWidth(2, 300)
        self.table.setColumnWidth(3, 800)
        self.table.setColumnWidth(4, 70)
        #header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

    def setQuoteView(self):
        header = self.table.horizontalHeader()

        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(8, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(9, QHeaderView.ResizeMode.Stretch)

        self.table.setItemDelegateForColumn(0, TopAlignDelegate(self.table))
        self.table.setItemDelegateForColumn(1, TopAlignDelegate(self.table))
        self.table.setItemDelegateForColumn(2, TopAlignDelegate(self.table))
        self.table.setItemDelegateForColumn(3, TopAlignDelegate(self.table))
        self.table.setItemDelegateForColumn(4, TopAlignDelegate(self.table))
        self.table.setItemDelegateForColumn(5, TopAlignDelegate(self.table))
        self.table.setItemDelegateForColumn(6, TopAlignDelegate(self.table))
        self.table.setItemDelegateForColumn(7, TopAlignDelegate(self.table))
        self.table.setItemDelegateForColumn(8, TopAlignDelegate(self.table))
        self.table.setItemDelegateForColumn(9, TopAlignDelegate(self.table))

        self.table.setColumnWidth(1, 500)
        self.table.setColumnWidth(2, 300)
        self.table.setColumnWidth(3, 800)
        self.table.setColumnWidth(4, 800)
        self.table.setColumnWidth(9, 300)


    def setToEdit(self,index):
        model = self.table.model()
        row = index.row()

        if self.currentType == "authors":
            identifier = str(model.index(row, 0).data())
            name = str(model.index(row, 1).data())
            notes = str(model.index(row, 2).data())
            self.authorPanelEdit.setData(name, notes,identifier,self.command)
            self.stack.setCurrentIndex(0)
        else:
            identifier = str(model.index(row, 0).data())
            title = str(model.index(row, 1).data())
            author = str(model.index(row, 2).data())
            if self.currentType == "books":
                notes = str(model.index(row, 3).data())
                self.bookPanelEdit.setData(title,author, notes,identifier,self.command)
                self.stack.setCurrentIndex(1)
            if self.currentType == "quotes":
                quote = str(model.index(row, 3).data())
                notes = str(model.index(row, 4).data())
                startPage = str(model.index(row, 5).data())
                startRow = str(model.index(row, 6).data())
                endPage = str(model.index(row, 7).data())
                endRow = str(model.index(row, 8).data())
                genres = str(model.index(row, 9).data())
                q = Quote(title,author,startPage,startRow,endPage,endRow,quote,notes,genres)

                self.quotePanelEdit.setData(q,self.command,int(identifier))
                self.stack.setCurrentIndex(2)

    def delete_row(self):
        self.logicalLevel.deleteRow(self)






