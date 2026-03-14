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

GET_BOOKS ="""SELECT 
                    b.id as Id,
                    b.title AS Titlu, 
                    a.name  AS Autor,
                    b.notes AS Notițe,
                    (SELECT COUNT(*) 
                       FROM quotes q 
                      WHERE q.bookId = b.id) AS "No citate"
                  FROM books b
                    JOIN authors a ON b.authorId = a.id """

GET_QUOTES = """
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

GET_AUTHORS = """
                  SELECT 
                    a.id AS Id,
                    a.name AS Nume,
                    a.notes AS Notițe,
                    (SELECT COUNT(*) FROM books b WHERE b.authorId = a.id) AS "No cărți",
                    (SELECT COUNT(*) 
                       FROM quotes q 
                       JOIN books b ON q.bookId = b.id
                      WHERE b.authorId = a.id) AS "No citate"
                FROM authors a
                    """