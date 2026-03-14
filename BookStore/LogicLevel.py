from PyQt6.QtSql import QSqlQueryModel, QSqlQuery
from PyQt6.QtWidgets import QMessageBox

from BookStore import Constants
from BookStore.DB import DB
from BookStore.Entries.Book import Book
from BookStore.Entries.Quote import Quote
from BookStore.TextValidation import checkDataBook, checkDataAuthor, checkDataQuote


class LogicLevel:
    _instance = None

    def __new__(cls, *args, **kwargs):  # such that only one instance is created
        if cls._instance is None:
            cls._instance = super(LogicLevel, cls).__new__(cls)
        return cls._instance

    def __init__(self,db:DB):
        if getattr(self, '_initialized', False):
            return
        self._initialized = True
        self.db = db

    def addAuthor(self,a):
        if checkDataAuthor(a):
            if self.db.getAuthorId(a.author_text.text()) == -1:  # if it does not exist, we must add
                queryStr = "INSERT INTO authors (name, notes) VALUES (?, ?)"
                name = str(a.author_text.text()).strip()
                notes = str(a.notes_text.toPlainText()).strip()
                params = (name, notes)
                self.db.executeQuery(queryStr, params)
            else:
                a.showError("name", "Author exists", "author", a)

    def searchAuthor(self,stack,authorPanelAdd,view):
        #model = QSqlQueryModel()

        command = Constants.GET_AUTHORS
        model = self.db.searchAuthors(authorPanelAdd.author_text.text())
        view.prepareContent(model, "authors", command)
        stack.setCurrentIndex(7)


    def saveChangesAPE(self,author,a):
        changedName = False
        if a.previousName != author.name:
            changedName = True

        if checkDataAuthor(a):
            if (changedName and not self.db.getAuthorId(a.author_text.text()) != -1) or not changedName:
                command = f"UPDATE authors SET name = '{author.name}', notes = '{author.notes}' WHERE id = {a.previousID}"
                print(command)
                self.db.updateDB(command)

            else:
                a.showError("name", "Author exists", "author", a)
        #self.db.updateDB(aPE, "author", author, aPE.previousID, changedName)

    def dbConnectAddBooks(self,bookPanelAdd):
        if checkDataBook(bookPanelAdd):
            authorId = self.db.getAuthorId(bookPanelAdd.bookAuthorText.text())
            if authorId == -1:
                bookPanelAdd.showError("author", "Author does not exist", "books", bookPanelAdd)
            else: #that author exists => check if maybe it already exists
                if not self.db.checkBookExist(bookPanelAdd.bookTitleText.text(),authorId):
                    #queryStr = "INSERT INTO books (title, authorId, notes) VALUES (?, ?, ?)"
                    title = str(bookPanelAdd.bookTitleText.text()).strip()
                    authorId = str(authorId)
                    notes = bookPanelAdd.bookNotesText.toPlainText()
                    params = (title,authorId,notes)
                    self.db.addBooks(params)
                    #query = self.executeQuery(queryStr, params)
                else:
                    bookPanelAdd.showError("author", "This author already has a book with this title", "books", bookPanelAdd)
        #self.db.addBooks(bookPanelAdd)

    def dbConnectSearchBook(self,stack,b,panelView):

        authorName = b.bookAuthorText.text().strip()

        command = Constants.GET_BOOKS
        if b.bookAuthorText.text().strip() != "":
            authorId = self.db.getAuthorId(b.bookAuthorText.text())
            if b.bookTitleText.text() != "":

                command+=f"WHERE b.title LIKE '%{b.bookTitleText.text()}%' COLLATE NOCASE AND a.name LIKE '%{authorName}%' COLLATE NOCASE;"
            else :
                command+=f"WHERE a.name LIKE '%{authorName}%' COLLATE NOCASE;"
        else:
            if b.bookTitleText.text().strip() != "":
                command+=f"WHERE b.title LIKE '%{b.bookTitleText.text().strip()}%' COLLATE NOCASE;"

        model = self.db.searchBooks(command)
        panelView.prepareContent(model,"books",command)


        stack.setCurrentIndex(7)

        #self.db.searchBooks(stack, bookPA, panelView)

    def saveChangesBPE(self,a):
        currentTitle = str(a.bookTitleText.text()).strip()
        currentAuthor = str(a.bookAuthorText.text()).strip()
        currentNotes = str(a.bookNotesText.toPlainText()).strip()
        book = Book(currentTitle,currentAuthor,currentNotes)
        changed = False
        if a.previousTitle != currentTitle or a.previousAuthor != currentAuthor:
            changed = True

        print('update book')
        if checkDataBook(a):
            authorId = self.db.getAuthorId(book.author)
            if authorId != -1:
                if (changed and not self.checkBookExist(book.title, authorId)) or not changed:

                    command = f"UPDATE books SET title = '{book.title}', authorId = '{authorId}', notes = '{book.notes}' WHERE id = {a.previousID}"
                    print(command)
                    self.db.updateDB(command)
                else:
                    a.showError("title", "Book exists", "books", a)
            else:
                a.showError("author", "Author doesn't exist", "books", a)

        #self.db.updateDB(bookPanelEdit,"books",book,bookPanelEdit.previousId,changed)
    def deleteRow(self,panelView):
        selected = panelView.table.selectionModel().selectedRows()
        model = panelView.table.model()

        for index in selected:
            value = str(index.sibling(index.row(), 0).data())
            print(value)
            self.db.deleteEntry(panelView.currentType, value)

        if isinstance(model, QSqlQueryModel):
            new_query = QSqlQuery(panelView.command)
            model.setQuery(new_query)

    def addQuote(self,q):
        print('adding e')
        # if inserted data ok
        # if the book exists
        # if the qoute doesn't already exist
        print('adding Quote')
        startPage = str(q.quoteStartPageText.text()).strip()
        endPage = str(q.quoteEndPageText.text()).strip()
        startRow = str(q.quoteStartRowText.text()).strip()
        endRow = str(q.quoteEndRowText.text()).strip()
        notes = str(q.quoteNotesText.toPlainText()).strip()
        quote = str(q.quoteText.toPlainText()).strip()
        if checkDataQuote(q):
            authorId = self.db.getAuthorId(q.quoteAuthorText.text())
            if authorId == -1:
                q.showError("author", "Author doesn't exist", "quotes", q)
            else:
                bookId = self.db.getBookId(q.quoteBookTitleText.text(), authorId)

                if bookId == -1:
                    q.showError("title", "Book doesn't exist for this author", "quotes", q)
                else:
                    if self.db.checkQuoteExist(bookId, quote):
                        q.showError("quote", "Quote exists", "quotes", q)
                    else:
                        genres = [q.keyword1.text(), q.keyword2.text(), q.keyword3.text(), q.keyword4.text(),
                                  q.keyword5.text()]
                        queryStr = "INSERT INTO quotes (bookId, quote, startPage, endPage, startRow, endRow, notes) VALUES (?, ?, ?, ?, ?, ?, ?)"
                        params = (bookId, quote, startPage, endPage, startRow, endRow, notes)

                        self.db.addQuote(queryStr, params,genres)
                        #query = self.executeQuery(queryStr, params)



    def searchQuote(self,quoteAdd,stack,view):
        #model = QSqlQueryModel()
        bookTitle = quoteAdd.quoteBookTitleText.text().strip()
        authorName = quoteAdd.quoteAuthorText.text().strip()
        command = Constants.GET_QUOTES
        title = quoteAdd.quoteBookTitleText.text().strip()
        author = quoteAdd.quoteAuthorText.text().strip()
        notes = quoteAdd.quoteNotesText.toPlainText().strip()
        quote = quoteAdd.quoteText.toPlainText().strip()
        genres = [quoteAdd.keyword1.text().strip(),quoteAdd.keyword2.text().strip(),quoteAdd.keyword3.text().strip(),quoteAdd.keyword4.text().strip(),quoteAdd.keyword5.text().strip()]
        notNullGenres = [s for s in genres if s!= ""]
        genreIds = [self.db.getGenreId(s) for s in notNullGenres]
        if title != "" or author != "" or notes != "" or genreIds != [] or quote != "":
            command+=" WHERE "
        isFirst = True
        if title != "":
            command+=f"b.title LIKE '%{title}%'"
            isFirst = False

        if author != "":
            if isFirst:
                isFirst = False
            else:
                command+=" AND "
            command+=f"a.name LIKE '%{author}%'"

        if notes != "":
            if isFirst:
                isFirst = False
            else:
                command+=" AND "
            command+=f"q.notes LIKE '%{notes}%'"

        if quote != "":
            if isFirst:
                isFirst = False
            else:
                command+=" AND "
            command+=f"q.quote LIKE '%{quote}%' "
        if genreIds:
            if isFirst:
                isFirst = False
            else:
                command+=" AND "
            command+="qg.genreId IN "
            genreIdList = "("
            for g in genreIds:
                genreIdList += f"{g}, "
            command+=genreIdList
            command=command[:-2]
            command+=")"

        command += " GROUP BY q.id, b.title, a.name, q.quote, q.notes"
        print(command)
        model = self.db.searchQuote(command)
        view.prepareContent(model,"quotes",command)
        stack.setCurrentIndex(7)

        #self.db.searchQuote(stack,quotePanelAdd,view)

    def saveChangesQPE(self,quotePanelEdit):
        newTitle = quotePanelEdit.quoteBookTitleText.text().strip()
        newAuthor = quotePanelEdit.quoteAuthorText.text().strip()
        newStartPage = quotePanelEdit.quoteStartPageText.text().strip()
        newEndPage = quotePanelEdit.quoteEndPageText.text().strip()
        newStartRow = quotePanelEdit.quoteStartRowText.text().strip()
        newEndRow = quotePanelEdit.quoteEndRowText.text().strip()
        newQuoteText = quotePanelEdit.quoteText.toPlainText().strip()
        newNotes = quotePanelEdit.quoteNotesText.toPlainText().strip()
        genres = [quotePanelEdit.keyword1.text().strip(), quotePanelEdit.keyword2.text().strip(), quotePanelEdit.keyword3.text().strip(),
                  quotePanelEdit.keyword4.text().strip(), quotePanelEdit.keyword5.text().strip()]
        notNullGenres = [s for s in genres if s != ""]
        genreString = ','.join(notNullGenres)
        newQuote = Quote(newTitle, newAuthor, newStartPage, newStartRow, newEndPage, newEndRow, newQuoteText,
                               newNotes, genreString)
        primaryKeyChanged = False
        if newQuoteText != quotePanelEdit.previousQuote.quote or newTitle != quotePanelEdit.previousQuote.bookTitle or newAuthor != quotePanelEdit.previousQuote.author:
            primaryKeyChanged = True

        #self.db.updateDB(quotePanelEdit, "quotes", newQuote, quotePanelEdit.previousId, primaryKeyChanged)
        if checkDataQuote(quotePanelEdit):
            authorId = self.db.getAuthorId(newQuote.author)
            if authorId == -1:
                quotePanelEdit.showError("author", "Author doesn't exist", "quotes", quotePanelEdit)
                return

            bookId = self.db.getBookId(newQuote.bookTitle, authorId)
            if bookId == -1:
                quotePanelEdit.showError("title", "Book doesn't exist", "quotes", quotePanelEdit)
                return
            print('changed: ' + str(primaryKeyChanged))
            if (primaryKeyChanged and not self.db.checkQuoteExist(bookId, newQuote.quote)) or not primaryKeyChanged:

                self.db.clearQuoteGenre(quotePanelEdit.previousId)
                genres = newQuote.genres.split(",")

                for genre in genres:
                    if genre != "":
                        gid = self.db.getGenreId(genre)
                        self.db.addQuoteGenre(quotePanelEdit.previousId, gid)
                command = f"UPDATE quotes SET bookId = {bookId}, quote = '{newQuote.quote}', startPage = {newQuote.startPage}, endPage = {newQuote.endPage},startRow = {newQuote.startRow}, endRow = {newQuote.endRow},notes = '{newQuote.notes}' WHERE id = {quotePanelEdit.previousId}"
                print(command)
                self.db.updateDB(command)
            else:
                quotePanelEdit.showError("quote", "Information conflict with existing", "quotes", a)

    def resetDB(self):

        widget = QMessageBox()
        widget.setWindowTitle("Confirm Delete")
        widget.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        response = widget.exec()
        if response == QMessageBox.StandardButton.Yes:
            self.db.createTables(True)

    def sendSummary(self,params):
        print('sending summary')
