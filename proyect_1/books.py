from fastapi import FastAPI, Body

app = FastAPI()



BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


@app.get('/')
async def hello():                                      #Define cual es la URL
    return {'message': 'Hola Felix'}        #Funcion para cargar la vista

#Devuelvo todos los libros
@app.get('/books')
async def read_all_books():
    return BOOKS

# @app.get('/books/mybook')
# async def read_all_books():
#     return {'book_title': 'Este es mi libro favorito'}

@app.get("/books/{book_title}")                              
async def read_all_book(book_title: str):                  
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

@app.get('/books/')
async def read_category_by_query(category:str):
    book_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            book_to_return.append(book)
    return book_to_return

@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
                book.get('category').casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return

#Post a new book
@app.post('/books/create_book')
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

#Update a book
@app.put('/books/update_book')
async def update_book(update_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == update_book.get('title').casefold():
            BOOKS[i] = update_book


#Delete a book
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break

#Get all books for an specific author
@app.get("/books/get_books_author/{author}")
async def book_by_author(author : str):
    author_books = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            author_books.append(book)
    return author_books
