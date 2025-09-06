import re

def is_numeric(string: str) -> bool:
    return bool(re.match(r"^-?\d+$", string))
def checkRowPage(row: str,page:str) -> str:
    if len(row) == 0 or len(page) == 0:
        return "Empty space detected"
    if len(row)>4 or len(page)>4:
        return "String too long"
    if not is_numeric(page) or not is_numeric(row):
        return "Numeric string required"
    return ""

def checkDataQuote(q) -> bool:

    dataOk = True
    """Validate page and row input from QuotePanel."""
    q.clearErrors()
    # -- Start check --
    start_page = q.start_page_text.text()
    start_row = q.start_row_text.text()
    start_message = checkRowPage(start_row,start_page)

    end_page = q.end_page_text.text()
    end_row = q.end_row_text.text()
    end_message = checkRowPage(end_row,end_page)

    if start_message == "" and end_message == "":
        if int(start_page) > int(end_page):
            end_message = "End page must be greater than start page"
            dataOk = False
        elif int(start_page) == int(end_page) and (int(end_row) < int(start_row)):
            end_message = "End row must be greater than start row"
            dataOk = False
    q.showError("start", start_message, "quote", q)
    q.showError("end",end_message, "quote", q)

    if len( q.keyword1.text() ) > 100 or len( q.keyword2.text() ) > 100 or len( q.keyword3.text() ) > 100 or len( q.keyword4.text() ) > 100 or len( q.keyword5.text() ) > 100 :
        dataOk = False
        q.showError("kw", "String too long", "quote", q)
    #TODO title from DB
    if 1:
        if len(q.book_title_text.text()) > 100:
            q.showError("title", "Title too long", "quote", q)
            dataOk = False
        else:
            q.showError("title", "Title does not exist", "quote", q)
            dataOk = False
    #TODO author from DB + check if good title
    if 1:
        if len(q.author_text.text()) > 100:
            q.showError("author", "Author name too long", "quote", q)
            dataOk = False
        else :
            q.showError("author", "Author does not exist", "quote", q)
            dataOk = False
        if 0:
            q.showError("title", "Title does not have this author", "quote", q)
            dataOk = False
    return dataOk

def checkDataAuthor(a)->bool:

    ok = True
    a.clearErrors("author",a)
    if a.author_text.text() == "":
        a.showError("name", "Empty string detected", "author", a)
        ok = False
    elif len(a.author_text.text())>100:
        a.showError("name", "Name too long", "author", a)
        ok = False
    if len(a.notes_text.toPlainText())>3000:
        a.showError("notes", "Notes too long", "author", a)
        ok = False
    #TODO check if the author exists in the DB
    return ok

def checkDataBook(b)->bool:
    ok = True
    b.clearErrors("books",b)
    if b.bookTitleText.text() == "":
        b.showError("title", "Empty string detected", "book", b)
        ok = False
    elif len(b.bookTitleText.text())>100:
        b.showError("title", "Title too long", "book", b)
    if b.bookAuthorText.text() == "":
        b.showError("author", "Empty string detected", "book", b)
        ok = False
    elif len(b.bookAuthorText.text())>100:
        b.showError("author", "Author name too long", "book", b)
    if len(b.bookNotesText.toPlainText())>3000:
        b.showError("notes", "Notes too long", "book", b)
    return ok

