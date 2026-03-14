from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtWidgets import QApplication


from PyQt6.QtSql import *
from PyQt6.QtSql import QSqlDatabase


from BookStore import Constants
import sys
import os

class DB:
    _instance = None
    def __new__(cls, *args, **kwargs):#such that only one instance is created
        if cls._instance is None:
            cls._instance = super(DB, cls).__new__(cls)
        return cls._instance

    def __init__(self): #done just one once by using the getattr and initialized
        if getattr(self, '_initialized', False):
            return
        self._initialized = True

        self.authorIdCache = {}
        self.bookIdCache = {}
        self.genreIdCache = {}

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("books.db")

        if not self.db.open():
            exit(Constants.DB_OPEN_ERROR)

        self.createTables(False)

    def executeQuery(self, queryStr: str, params = None) -> QSqlQuery:
        query = QSqlQuery(self.db)
        query.prepare(queryStr)
        for p in params:
            query.addBindValue(p)
        query.exec()
        return query

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
        query.exec(Constants.BOOK_TABLE_CREATE)
        query.exec(Constants.AUTHOR_TABLE_CREATE)
        query.exec(Constants.GENRE_TABLE_CREATE)
        query.exec(Constants.QUOTE_TABLE_CREATE)
        query.exec(Constants.GENRE_QUOTE_TABLE_CREATE)

    def getAuthorId(self, name: str) -> int:
        if name in self.authorIdCache:
            return self.authorIdCache[name]
        queryStr = "SELECT id FROM authors WHERE name = ? COLLATE NOCASE;"
        params = (name,)
        query = self.executeQuery(queryStr, params)

        if query.next():  # Move cursor to first row
            authorId = query.value(0)
            self.authorIdCache[name] = authorId
            return authorId
        return -1
    def getBookId(self, title: str,authorId: int) -> int:
        if title in self.bookIdCache:
            return self.bookIdCache[title]
        queryStr = "SELECT id FROM books WHERE title = ? COLLATE NOCASE AND authorId = ?;"
        params = (title,authorId)
        query = self.executeQuery(queryStr, params)
        if query.next():
            bookId = query.value(0)
            self.bookIdCache[title] = bookId
            return bookId
        return -1
    def getGenreId(self, name: str) -> int:
        if name!="":
            if name in self.genreIdCache:
                return self.genreIdCache[name]
            queryStr = "SELECT id FROM genres WHERE name = ? COLLATE NOCASE;"
            params = (name,)
            query = self.executeQuery(queryStr, params)
            if query.next():
                genreId = query.value(0)
                self.genreIdCache[name] = genreId
                return genreId
            return self.addGenres(name)
        return -1



    def addGenres(self, name: str)->int:
        queryStr = "INSERT INTO genres (name) VALUES (?)"
        params = (name,)
        query = self.executeQuery(queryStr, params)
        if not query:
            exit(-1)
        return query.lastInsertId()

    def addQuoteGenre(self, quoteId: int, genreId: int):
        queryStr = "INSERT INTO genresQuote (quoteId, genreId) VALUES (?, ?)"
        params = (quoteId, genreId)
        query = self.executeQuery(queryStr, params)

        if not query:
            exit(-1)
    def addQuote(self, queryStr,params,genres):
        query = self.executeQuery(queryStr, params)
        if not query:
            exit(-1)
        quoteId = query.lastInsertId()

        notNullGenresId = [self.getGenreId(s) for s in genres if s != ""]
        for genreId in notNullGenresId:
            self.addQuoteGenre(quoteId, genreId)
    def addBooks(self, params):

        queryStr = "INSERT INTO books (title, authorId, notes) VALUES (?, ?, ?)"
        query = self.executeQuery(queryStr, params)


    def checkQuoteExist(self, bookId: int, quote:str) -> bool:
        queryStr = "SELECT id FROM quotes WHERE bookId = ? AND quote = ? COLLATE NOCASE;"
        bookId = str(bookId).strip()
        quote = str(quote).strip()
        params = (bookId, quote)
        query = self.executeQuery(queryStr, params)
        if query.next(): return True
        return False
    def checkBookExist(self, title: str, authorId: int) -> bool:
        query = QSqlQuery(self.db)
        query.prepare("SELECT id FROM books WHERE title = ? COLLATE NOCASE AND authorId = ? ;")
        query.addBindValue(title)
        query.addBindValue(authorId)
        query.exec()
        if query.next(): return True
        return False
    def clearQuoteGenre(self, quoteId: int):
        query = QSqlQuery(self.db)
        query.prepare("DELETE FROM genresQuote WHERE quoteId = ?")
        query.addBindValue(quoteId)
        if not query.exec():
            exit(-1)

    def searchBooks(self, command):

        model = QSqlQueryModel()
        query =QSqlQuery(self.db)
        query.prepare(command)
        query.exec()
        model.setQuery(command)
        return model

    def searchQuote(self, command):
        model = QSqlQueryModel()

        query =QSqlQuery(self.db)
        query.prepare(command)
        query.exec()
        model.setQuery(query)
        return model

    def searchAuthors(self, authorText):
        model = QSqlQueryModel()

        command = Constants.GET_AUTHORS
        if authorText != "":
            query = QSqlQuery(self.db)
            command += f"WHERE name LIKE '%{str(authorText)}%' COLLATE NOCASE;"
            print(command)
            query.prepare(command)

            query.exec()
            model.setQuery(query)
        else:

            model.setQuery(command,self.db)
            print(command)
        return model


    def updateDB(self,command):
        #a type newObj, previousId, primaryKeyChanged
        #self.db.updateDB(quotePanelEdit, "quotes", newQuote, quotePanelEdit.previousId, primaryKeyChanged)

        query = QSqlQuery(self.db)
        query.prepare(command)
        if not query.exec():
            print('not ok')
        else:
            print("ok")

    def deleteEntry(self, currentType:str,identificator: int):

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



# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     print("main")
#     db = DB()
#     print("db")
#     print(db.getLatestEntries("quotes"))
import sqlite3
def get_entries(table):
    conn = sqlite3.connect(r"D:\Rafail\Python_projects\Book-Managing-App\BookStore\books.db")
    cursor = conn.cursor()
    if table == "authors":
        command = Constants.GET_AUTHORS
    elif table == "books":
        command = Constants.GET_BOOKS
    elif table == "quotes":
        command = Constants.GET_QUOTES
        command +="GROUP BY q.id, b.title, a.name, q.quote, q.notes"
    else:
        return -6
    cursor.execute(command)

    rows = cursor.fetchall()
    conn.close()

    return rows