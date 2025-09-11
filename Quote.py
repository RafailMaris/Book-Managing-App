class Quote:
    id = ""
    bookTitle = ""
    author = ""
    startPage =""
    startRow = ""
    endPage = ""
    endRow = ""
    quote = ""
    notes = ""
    genres = ""
    def __init__(self,bookTitle,author,startPage,startRow,endPage,endRow,quote,notes,genres):
        self.bookTitle = bookTitle
        self.author = author
        self.startPage = startPage
        self.startRow = startRow
        self.endPage = endPage
        self.endRow = endRow
        self.quote = quote
        self.notes = notes
        self.genres = genres



