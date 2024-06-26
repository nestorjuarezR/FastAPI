from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
app = FastAPI()



class Book:
    id : int
    title : str
    author : str
    description : str
    rating : int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)  
    published_date: int = Field(min_length=6)

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'A new Book',
                'author': 'hola123',
                'description': 'Esta es una nueva descripcion',
                'rating': 5,
                'published_date': 'mmddyy'
            }
        }


BOOKS = [
    Book(1,'Libro de ejemplo', 'Nestor', 'Un muy buen libro', 5, 123456),
    Book(2,'Libro segundo', 'Felix', 'Un muy buen libro', 1, 123456),
    Book(3,'Libro de tercer', 'Nestor', 'Un muy buen libro', 5, 234567),
    Book(4,'Libro de cuarto', 'Felix', 'Un muy buen libro', 2, 234567),
    Book(5,'Libro de quinto', 'Nestor', 'Un muy buen libro', 3, 123456),
]



@app.get("/books")
async def read_all_book():
    return BOOKS



#Get a book by id
@app.get("/books/{book_id}")
async def read_book(book_id:int):
    for book in BOOKS:
        if book.id == book_id:
            return book



@app.get("/books/")
async def read_book_by_rating(book_rating:int):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return



@app.get("/books/publish/")
async def get_by_published_date(published_date:int):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))



def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book



@app.put("/books/update_book")
async def update_book(book:BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = Book(**book.model_dump())


@app.delete("/books/{book_id}")
async def delete_book(book_id:int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break