DB_OPEN_ERROR = 1
BOOK_TABLE_CREATE = """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                authorId INTEGER,
                notes TEXT,
                FOREIGN KEY(authorId) REFERENCES authors(id)
            )
        """
AUTHOR_TABLE_CREATE = """
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                notes TEXT
            )
        """
GENRE_TABLE_CREATE = """
            CREATE TABLE IF NOT EXISTS genres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """
QUOTE_TABLE_CREATE = """
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
        """
GENRE_QUOTE_TABLE_CREATE = """
        CREATE TABLE IF NOT EXISTS genresQuote (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quoteId INTEGER NOT NULL,
            genreId INTEGER NOT NULL,
            FOREIGN KEY(quoteId) REFERENCES quotes(id),
            FOREIGN KEY(genreId) REFERENCES genres(id)
        )
        
            """
