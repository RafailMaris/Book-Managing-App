import re

import QuotePanelAdd


def is_numeric(string: str) -> bool:
    return bool(re.match(r"^-?\d+$", string))
def checkRowPage(row: str,page:str) -> str:
    if not is_numeric(page) or not is_numeric(row):
        return "Numeric string required"
    return ""

def checkDataQuote(q: QuotePanelAdd) -> bool:

    dataOk = True
    """Validate page and row input from QuotePanel."""
    q.clearErrors("quotes",q)
    if str(q.quoteBookTitleText.text()).strip() == "":
        q.showError("title", "Empty string detected", "quotes", q)
        dataOk = False
    elif len(str(q.quoteBookTitleText.text()).strip()) > 200:
        q.showError("title", "Too long", "quotes", q)
        dataOk = False
    if str(q.quoteAuthorText.text()).strip() == "":
        q.showError("author","Empty string detected","quotes",q)
        dataOk = False
    elif len(str(q.quoteAuthorText.text()).strip())>200:
        q.showError("author","Too long","quotes",q)
        dataOk = False
    if str(q.quoteStartPageText.text()).strip() == "" or len(str(q.quoteStartRowText.text()).strip())==0:
        q.showError("start","Empty string detected","quotes",q)
        dataOk = False
    elif len(str(q.quoteStartPageText.text()).strip())>4 or len(str(q.quoteStartRowText.text()).strip())==0:
        q.showError("start","Too long","quotes",q)
        dataOk = False
    if str(q.quoteEndPageText.text()).strip() == "" or len(str(q.quoteEndRowText.text()).strip())>3:
        q.showError("end","Empty string detected","quotes",q)
        dataOk = False
    elif len(str(q.quoteEndPageText.text()).strip())>4 or len(str(q.quoteEndRowText.text()).strip())>3:
        q.showError("start","Too long","quotes",q)
        dataOk = False
    if len(str(q.keyword1.text()).strip()) > 30 or len(str(q.keyword2.text()).strip()) > 30 or len(str(q.keyword3.text()).strip()) > 30 or len(str(q.keyword4.text()).strip()) > 30 or len(str(q.keyword5.text()).strip()) > 30:
        q.showError("keyword","Too long","quotes",q)
        dataOk = False
    if q.quoteText.toPlainText().strip() == "":
        q.showError("quote","Empty string detected","quotes",q)
    if len(str(q.quoteNotesText.toPlainText()).strip()) > 3000:
        q.showError("notes","Too long","quotes",q)
        dataOk = False
    startPage = q.quoteStartPageText.text()
    startRow = q.quoteStartRowText.text()
    endPage = q.quoteEndPageText.text()
    endRow = q.quoteEndRowText.text()
    startNum = False
    endNum = False
    print(startPage)
    if not is_numeric(startPage) or not is_numeric(startRow):
        q.showError("start","Not numeric","quotes",q)
        dataOk = False
    elif startPage[0]=='-':
        q.showError("start", "Page can't be negative", "quotes", q)
        dataOk = False
    else:
        startNum = True
    if not is_numeric(endPage) or not is_numeric(endRow):
        q.showError("end","Not numeric","quotes",q)
        dataOk = False
    elif endPage[0]=='-':
        q.showError("end", "Page can't be negative", "quotes", q)
        dataOk = False
    else:
        endNum = True
    if endNum and startNum:
        if int(startPage) > int(endPage) or int(startRow) > int(endRow):
            q.showError("start","Starts after end","quotes",q)
            dataOk = False

    #TODO if any 2 genres are the same
    genres = [q.keyword1.text(), q.keyword2.text(), q.keyword3.text(), q.keyword4.text(), q.keyword5.text()]
    nonEmptyGenres =[s for s in genres if s!=""]
    isAllDifferent = len(nonEmptyGenres) == len(set(nonEmptyGenres))
    if not isAllDifferent:
        q.showError("kw","Not all genres unique","quotes",q)
        dataOk = False
    return dataOk


def checkDataAuthor(a)->bool:

    ok = True
    a.clearErrors("author",a)
    if a.author_text.text() == "":
        a.showError("name", "Empty string detected", "author", a)
        ok = False
    elif len(a.author_text.text())>1200:
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
        b.showError("title", "Empty string detected", "books", b)
        print('empty book title')
        ok = False
    elif len(b.bookTitleText.text())>200:
        b.showError("title", "Title too long", "books", b)
    if b.bookAuthorText.text() == "":
        b.showError("author", "Empty string detected", "books", b)
        ok = False
    elif len(b.bookAuthorText.text())>200:
        b.showError("author", "Author name too long", "books", b)
    if len(b.bookNotesText.toPlainText())>3000:
        b.showError("notes", "Notes too long", "books", b)
    return ok

