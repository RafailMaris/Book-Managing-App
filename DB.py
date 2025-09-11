from PyQt6.QtCore import Qt, QModelIndex

import QuotePanelAdd, AuthorPanelAdd
from PyQt6.QtSql import *
from PyQt6.QtSql import QSqlDatabase

import AuthorPanelAdd
import QuotePanelAdd
from BookPanelAdd import BookPanelAdd
from PanelView import PanelView
from TextValidation import checkDataAuthor, checkDataBook, checkDataQuote


class DB:
    def __init__(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("text.db")
        if not self.db.open():
            print('can not open DB')
            exit(1)
        else:
            print('aaaa')
        # self.db = sqlite3.connect('books.db')
        # self.cursor = self.db.cursor()
       # self.db.open()
        self.createTables(False)

    def dropTables(self):
        query = QSqlQuery(self.db)
        query.exec("DROP TABLE IF EXISTS quotes")
        query.exec("DROP TABLE IF EXISTS books")
        query.exec("DROP TABLE IF EXISTS authors")
        query.exec("DROP TABLE IF EXISTS genres")
        query.exec("DROP TABLE IF EXISTS genresQuote")
       

    def createTables(self,dropQ:bool):
        if dropQ:
            self.dropTables()
        query = QSqlQuery(self.db)
        query.exec("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                authorId INTEGER,
                notes TEXT,
                FOREIGN KEY(authorId) REFERENCES authors(id)
            )
        """)
        query.exec("""
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                notes TEXT
            )
        """)
        query.exec("""
            CREATE TABLE IF NOT EXISTS genres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        query.exec("""
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bookId INTEGER NOT NULL,
                quote TEXT NOT NULL,
                startPage VARCHAR(4) NOT NULL,
                endPage VARCHAR(4) NOT NULL,
                startRow VARCHAR(4) NOT NULL,
                endRow VARCHAR(4) NOT NULL,
                notes TEXT NOT NULL,
                FOREIGN KEY(bookId) REFERENCES books(id)
            )
        """)

        query.exec("""
        CREATE TABLE IF NOT EXISTS genresQuote (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quoteId INTEGER NOT NULL,
            genreId INTEGER NOT NULL,
            FOREIGN KEY(quoteId) REFERENCES quotes(id),
            FOREIGN KEY(genreId) REFERENCES genres(id)
        )
        
            """)


    def getAuthorId(self, name: str) -> int:
        query = QSqlQuery(self.db)
        query.prepare("SELECT id FROM authors WHERE name = ? COLLATE NOCASE;")
        query.addBindValue(name)
        query.exec()
        if query.next():  # Move cursor to first row
            return query.value(0)  # author exists
        return -1
    def getBookId(self, title: str,authorId: int) -> int:
        query = QSqlQuery(self.db)
        print(f"authorId is {authorId} title is {title}")
        query.prepare("SELECT id FROM books WHERE title = ? COLLATE NOCASE AND authorId = ?;")
        query.addBindValue(title)
        query.addBindValue(authorId)
        query.exec()
        if query.next(): return query.value(0)
        return -1
    def getGenreId(self, name: str) -> int:
        if name!="":
            query = QSqlQuery(self.db)
            query.prepare("SELECT id FROM genres WHERE name = ? COLLATE NOCASE;")
            query.addBindValue(name)
            query.exec()
            if query.next():
                return query.value(0)
            return self.addGenres(name)
        return -1


    def addAuthors(self, a: AuthorPanelAdd):
        if checkDataAuthor(a):
            if self.getAuthorId(a.author_text.text()) == -1: # if it does not exist, we must add
                query = QSqlQuery(self.db)
                query.prepare("INSERT INTO authors (name, notes) VALUES (?, ?)")
                query.addBindValue(str(a.author_text.text()).strip())
                query.addBindValue(str(a.notes_text.toPlainText()).strip())
                query.exec()

            else:
                a.showError("name", "Author exists", "author", a)

    def checkQuoteExist(self, bookId: int, quote:str) -> bool:
        query = QSqlQuery(self.db)
        query.prepare("SELECT id FROM quotes WHERE bookId = ? AND quote = ? COLLATE NOCASE;")
        print(f"SELECT id FROM quotes WHERE bookId = {bookId} AND quote = {quote} COLLATE NOCASE;")
        query.addBindValue(str(bookId).strip())
        query.addBindValue(str(quote).strip())
        query.exec()
        if query.next(): return True
        return False
    def checkGenreExist(self, name: str) -> bool:
        genreId = self.getGenreId(name)
        if genreId == -1:
            return False
        return True
    def addGenres(self, name: str)->int:
        query = QSqlQuery(self.db)
        query.prepare("INSERT INTO genres (name) VALUES (?)")
        query.addBindValue(name)
        if not query.exec():
            exit(-1)
        return query.lastInsertId()

    def addQuoteGenre(self, quoteId: int, genreId: int):
        query = QSqlQuery(self.db)
        query.prepare("INSERT INTO genresQuote (quoteId, genreId) VALUES (?, ?)")
        query.addBindValue(quoteId)
        query.addBindValue(genreId)

        if not query.exec():
            exit(-1)
    #def manageGenres(self,quoteId: int, ):
    def clearQuoteGenre(self, quoteId: int):
        query = QSqlQuery(self.db)
        query.prepare("DELETE FROM genresQuote WHERE quoteId = ?")
        query.addBindValue(quoteId)
        if not query.exec():
            exit(-1)
    def addQuote(self, q: QuotePanelAdd):
        #if inserted data ok
        #if the book exists
        #if the qoute doesn't already exist
        startPage = str(q.quoteStartPageText.text()).strip()
        endPage = str(q.quoteEndPageText.text()).strip()
        startRow = str(q.quoteStartRowText.text()).strip()
        endRow = str(q.quoteEndRowText.text()).strip()
        notes = str(q.quoteNotesText.toPlainText()).strip()
        quote = str(q.quoteText.toPlainText()).strip()
        if checkDataQuote(q):
            authorId = self.getAuthorId(q.quoteAuthorText.text())
            if authorId == -1:
                q.showError("author", "Author doesn't exist", "quotes", q)
            else:
                bookId = self.getBookId(q.quoteBookTitleText.text(),authorId)
                print(f"bookId is {bookId}")
                if bookId == -1:
                    q.showError("title", "Book doesn't exist for this author", "quotes", q)
                else:
                    if self.checkQuoteExist(bookId, quote):
                        q.showError("quote", "Quote exists", "quotes", q)
                    else:
                        command = f"INSERT INTO quotes (bookId, quote, startPage, endPage, startRow, endRow, notes) VALUES ({bookId}, '{quote}', {startPage}, {endPage}, {startRow}, {endRow}, '{notes}')"
                        print(command)
                        query = QSqlQuery(self.db)
                        query.prepare(command)
                        if not query.exec():
                            exit(-1)
                        quoteId = query.lastInsertId()
                        genres = [q.keyword1.text(), q.keyword2.text(), q.keyword3.text(), q.keyword4.text(), q.keyword5.text()]
                        notNullGenresId = [self.getGenreId(s) for s in genres if s!=""]
                        for genreId in notNullGenresId:
                            self.addQuoteGenre(quoteId, genreId)


            #TODO INSERTION
    def checkBookExist(self, title: str, authorId: int) -> bool:
        query = QSqlQuery(self.db)
        query.prepare("SELECT id FROM books WHERE title = ? COLLATE NOCASE AND authorId = ? ;")
        query.addBindValue(title)
        query.addBindValue(authorId)
        query.exec()
        if query.next(): return True
        return False

    def addBooks(self, b: BookPanelAdd):
        # if check book ok:
        # get id of author => change method to check author to return the id, else -1
        # search for the book with the name and the author
        # if exist: bad.
        # else: insert it
        if checkDataBook(b):
            authorId = self.getAuthorId(b.bookAuthorText.text())
            if authorId == -1:
                b.showError("author", "Author does not exist", "books", b)
            else: #that author exists => check if maybe it already exists
                if not self.checkBookExist(b.bookTitleText.text(),authorId):
                    query = QSqlQuery(self.db)
                    query.prepare("INSERT INTO books (title, authorId, notes) VALUES (?, ?, ?)")
                    query.addBindValue(str(b.bookTitleText.text()).strip())
                    query.addBindValue(str(authorId))
                    query.addBindValue(b.bookNotesText.toPlainText())
                    query.exec()

                else:
                    b.showError("author", "This author already has a book with this title", "books", b)

    def searchBooks(self,stack, b: BookPanelAdd, view: PanelView):
        # what to show: id, title, author NAME, notes => put in the query the name instead of id
        authorName = b.bookAuthorText.text().strip()
        model = QSqlQueryModel()
        command = """
                  SELECT 
                    b.id AS No,
                    b.title AS Titlu, 
                    a.name  AS Autor,
                    b.notes AS Notițe
                  FROM books b
                    JOIN authors a ON b.authorId = a.id
                  """
        if b.bookAuthorText.text().strip() != "":
            authorId = self.getAuthorId(b.bookAuthorText.text())
            if b.bookTitleText.text() != "":
               
                command+=f"WHERE b.title LIKE '%{b.bookTitleText.text()}%' COLLATE NOCASE AND a.name LIKE '%{authorName}%' COLLATE NOCASE;"
            else :
                command+=f"WHERE a.name LIKE '%{authorName}%' COLLATE NOCASE;"
        else:
            if b.bookTitleText.text().strip() != "":
                command+=f"WHERE b.title LIKE '%{b.bookTitleText.text().strip()}%' COLLATE NOCASE;"
        print(command)
        query =QSqlQuery(self.db)
        query.prepare(command)
        query.exec()
        model.setQuery(command)
        view.prepareContent(model,"books",command)
        model.setHeaderData(0,Qt.Orientation.Horizontal,"No")
        model.setHeaderData(1,Qt.Orientation.Horizontal,"Title")
        model.setHeaderData(2,Qt.Orientation.Horizontal,"Author")
        model.setHeaderData(3,Qt.Orientation.Horizontal,"Notes")
        stack.setCurrentIndex(7)


    def searchQuote(self, quoteAdd: QuotePanelAdd,stack, view: PanelView):
        model = QSqlQueryModel()
        bookTitle = quoteAdd.quoteBookTitleText.text().strip()
        authorName = quoteAdd.quoteAuthorText.text().strip()
        command ="""
            SELECT
            q.id AS Id,
            b.title AS Titlu, 
            a.name  AS Autor,
            q.quote as Citat,
            q.notes AS Notes,
            q.startPage AS StartPage,
            q.startRow AS StartRow,
            q.endPage AS EndPage,
            q.endRow AS EndRow,
            GROUP_CONCAT(DISTINCT g.name ORDER BY g.name) AS Genres
            FROM quotes q
                JOIN books b ON q.bookId = b.id
                JOIN authors a ON b.authorId = a.id
                LEFT JOIN genresQuote qg ON q.id = qg.quoteId
                LEFT JOIN genres g ON g.id = qg.genreId
                
        """
        title = quoteAdd.quoteBookTitleText.text().strip()
        author = quoteAdd.quoteAuthorText.text().strip()
        notes = quoteAdd.quoteNotesText.toPlainText().strip()
        quote = quoteAdd.quoteText.toPlainText().strip()
        genres = [quoteAdd.keyword1.text().strip(),quoteAdd.keyword2.text().strip(),quoteAdd.keyword3.text().strip(),quoteAdd.keyword4.text().strip(),quoteAdd.keyword5.text().strip()]
        notNullGenres = [s for s in genres if s!= ""]
        genreIds = [self.getGenreId(s) for s in notNullGenres]
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
        query =QSqlQuery(self.db)
        query.prepare(command)
        query.exec()
        model.setQuery(query)
        view.prepareContent(model,"quotes",command)
        stack.setCurrentIndex(7)

    def searchAuthors(self, stack, authorAdd: AuthorPanelAdd, view: PanelView):
        model = QSqlQueryModel()

        command = "SELECT * FROM authors"
        if authorAdd.author_text.text() != "":
            query = QSqlQuery(self.db)
            command = f"SELECT * FROM authors WHERE name LIKE '%{str(authorAdd.author_text.text())}%' COLLATE NOCASE;"
            print(command)
            query.prepare(command)
            #query.addBindValue(f"%{authorAdd.author_text.text()}%")
            query.exec()
            model.setQuery(query)
        else:
            model.setQuery("SELECT * FROM authors",self.db)
            print("all")
        view.prepareContent(model,"authors",command)
        model.setHeaderData(0, Qt.Orientation.Horizontal, "No")
        model.setHeaderData(1, Qt.Orientation.Horizontal, "Nume")
        model.setHeaderData(2, Qt.Orientation.Horizontal, "Notite")
        stack.setCurrentIndex(7)

    def updateDB(self,a, type,newObj,previousID,isPrimaryKeyChanged: bool):
            if type == "author":
                if checkDataAuthor(a):
                    if (isPrimaryKeyChanged and not self.getAuthorId(a.author_text.text()) != -1) or not isPrimaryKeyChanged:
                        command = f"UPDATE authors SET name = '{newObj.name}', notes = '{newObj.notes}' WHERE id = {previousID}"
                        print(command)
                        query = QSqlQuery(self.db)
                        query.prepare(command)
                        if not query.exec():
                            print('not ok')
                        else:
                            print("ok")
                    else:
                        a.showError("name", "Author exists", "author", a)

            if type == "books":
                print('update book')
                if checkDataBook(a):
                    authorId = self.getAuthorId(newObj.author)
                    if authorId != -1:
                        if (isPrimaryKeyChanged and not self.checkBookExist(newObj.title, authorId)) or not isPrimaryKeyChanged:

                            command = f"UPDATE books SET title = '{newObj.title}', authorId = '{authorId}', notes = '{newObj.notes}' WHERE id = {previousID}"
                            print(command)
                            query = QSqlQuery(self.db)
                            query.prepare(command)
                            if not query.exec():
                                print('not ok')
                            else:
                                print("ok")
                        else:
                            a.showError("title", "Book exists", "books", a)
                    else:
                        a.showError("author", "Author doesn't exist", "books", a)

            if type == "quotes":
                if checkDataQuote(a):
                    authorId = self.getAuthorId(newObj.author)
                    if authorId == -1:
                        a.showError("author", "Author doesn't exist", "quotes", a)
                        return

                    bookId = self.getBookId(newObj.bookTitle, authorId)
                    if bookId == -1:
                        a.showError("title", "Book doesn't exist", "quotes", a)
                        return 
                    print('changed: '+str(isPrimaryKeyChanged))
                    if (isPrimaryKeyChanged and not self.checkQuoteExist(bookId,newObj.quote)) or not isPrimaryKeyChanged:

                        self.clearQuoteGenre(previousID)
                        genres = newObj.genres.split(",")

                        for genre in genres:
                            if genre != "":
                                gid = self.getGenreId(genre)
                                self.addQuoteGenre(previousID, gid)
                        command = f"UPDATE quotes SET bookId = {bookId}, quote = '{newObj.quote}', startPage = {newObj.startPage}, endPage = {newObj.endPage},startRow = {newObj.startRow}, endRow = {newObj.endRow},notes = '{newObj.notes}' WHERE id = {previousID}"
                        print(command)
                        query = QSqlQuery(self.db)
                        query.prepare(command)
                        if not query.exec():
                            print('not ok')
                        else:
                            print("ok")
                    else:
                        a.showError("quote", "Information conflict with existing", "quotes", a)
    def deleteEntry(self, currentType:str,identificator:int):
        query = QSqlQuery(self.db)
        principalCommand = f"DELETE FROM {currentType} WHERE id = {identificator}"
        if currentType == "authors":
            command = f"SELECT * FROM books WHERE authorId = {identificator}"

            query.prepare(command)
            if not query.exec():
                exit(-2)
            while query.next():
                command = f"DELETE FROM quotes WHERE bookId = {query.value('id')}"
                print(command)
                queryDelete = QSqlQuery(self.db)
                queryDelete.prepare(command)
                if not queryDelete.exec():
                    exit(-3)
            command = f"DELETE FROM books WHERE authorId = {identificator}"
            query.prepare(command)
            if not query.exec():
                exit(-4)


        elif currentType == "books":
            command = f"DELETE FROM quotes WHERE bookId = {identificator}"
            query.prepare(command)
            if not query.exec():
                exit(-5)

        query.prepare(principalCommand)

        if not query.exec():
            exit(-5)


