import sys

from PyQt6.QtCore import Qt

import QuotePanel, AuthorPanelAdd
from Author import Author
from PanelView import PanelView
from TextValidation import checkDataQuote, checkDataAuthor
from PyQt6.QtSql import QSqlDatabase

from PyQt6.QtSql import *

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
       

    def addQuote(self, q: QuotePanel):
        # You should implement logic for checking if book and author exist
        print("""INSERT INTO quotes(bookId, quote ,startPage ,endPage ,startRow ,endRow ,notes) VALUES (...)""")

    def addAuthors(self, a: AuthorPanelAdd):
        if checkDataAuthor(a):
            if not self.checkAuthorExist(a.author_text.text()): # if it does not exist, we must add
                query = QSqlQuery(self.db)
                query.prepare("INSERT INTO authors (name, notes) VALUES (?, ?)")
                query.addBindValue(str(a.author_text.text()).strip())
                query.addBindValue(str(a.notes_text.toPlainText()).strip())
                query.exec()
            else:
                a.showError("name", "Author exists", "author", a)


    def checkAuthorExist(self, name: str) -> bool:
        query = QSqlQuery(self.db)
        query.prepare("SELECT id FROM authors WHERE name = ?")
        query.addBindValue(name)
        query.exec()
        if query.next():  # Move cursor to first row
            return True  # author exists
        return False

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
        stack.setCurrentIndex(5)

    def updateDB(self,a, type,newObj,previousID,isPrimaryKeyChanged: bool):
            if type == "author":
                if checkDataAuthor(a):
                    if (isPrimaryKeyChanged and not self.checkAuthorExist(a.author_text.text())) or not isPrimaryKeyChanged:
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

