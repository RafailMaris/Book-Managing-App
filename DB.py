from PyQt6.QtCore import Qt

import QuotePanelAdd, AuthorPanelAdd
from PyQt6.QtSql import *
from PyQt6.QtSql import QSqlDatabase

import AuthorPanelAdd
import QuotePanelAdd
from BookPanelAdd import BookPanelAdd
from PanelView import PanelView
from TextValidation import checkDataAuthor, checkDataBook


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
        self.createTables()

    def dropTables(self):
        query = QSqlQuery(self.db)
        query.exec("DROP TABLE IF EXISTS quotes")
        query.exec("DROP TABLE IF EXISTS books")
        query.exec("DROP TABLE IF EXISTS authors")
        query.exec("DROP TABLE IF EXISTS genres")
       

    def createTables(self):
        #self.dropTables()
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
        CREATE TABLE IF NOT EXISTS bookGenres(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bookId INTEGER NOT NULL,
            genreId INTEGER NOT NULL,
            FOREIGN KEY(bookId) REFERENCES books(id),
            FOREIGN KEY(genreId) REFERENCES genres(id)
        )
        
            """)
       

    def addQuote(self, q: QuotePanelAdd):
        # You should implement logic for checking if book and author exist
        print("""
        INSERT INTO quotes(bookId, quote ,startPage ,endPage ,startRow ,endRow ,notes) VALUES (...)""")

    def getAuthorId(self, name: str) -> int:
        query = QSqlQuery(self.db)
        query.prepare("SELECT id FROM authors WHERE name = ?")
        query.addBindValue(name)
        query.exec()
        if query.next():  # Move cursor to first row
            return query.value(0)  # author exists
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

    def checkBookExist(self, title: str, authorId: int) -> bool:
        query = QSqlQuery(self.db)
        query.prepare("SELECT id FROM books WHERE title = ? AND authorId = ?")
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
                #TODO la authorId: ce sa facem ca sa poata fi posibila un search nu foarte accurate: sa scrii si si tot sa iti dea ce trebuie
                command+=f"WHERE b.title LIKE '%{b.bookTitleText.text()}%' AND a.name LIKE '%{authorName}%'"
            else :
                command+=f"WHERE a.name LIKE '%{authorName}%'"
        else:
            if b.bookTitleText.text().strip() != "":
                command+=f"WHERE b.title LIKE '%{b.bookTitleText.text().strip()}%'"
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


    def searchQuote(self, stack):
        print("Search Quote")

    def searchAuthors(self, stack, authorAdd: AuthorPanelAdd, view: PanelView):
        model = QSqlQueryModel()

        command = "SELECT * FROM authors"
        if authorAdd.author_text.text() != "":
            query = QSqlQuery(self.db)
            command = f"SELECT * FROM authors WHERE name LIKE '%{str(authorAdd.author_text.text())}%'"
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
                    if(isPrimaryKeyChanged and not self.checkBookExist(newObj.title,authorId)):

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
