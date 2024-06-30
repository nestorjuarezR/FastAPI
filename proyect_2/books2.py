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

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)  

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'A new Book',
                'author': 'hola123',
                'description': 'Esta es una nueva descripcion',
                'rating': 5
            }
        }


BOOKS = [
    Book(1,'Libro de ejemplo', 'Nestor', 'Un muy buen libro', 5),
    Book(2,'Libro segundo', 'Felix', 'Un muy buen libro', 1),
    Book(3,'Libro de tercer', 'Nestor', 'Un muy buen libro', 5),
    Book(4,'Libro de cuarto', 'Felix', 'Un muy buen libro', 2),
    Book(5,'Libro de quinto', 'Nestor', 'Un muy buen libro', 3),
]


@app.get("/books")
async def read_all_book():
    return BOOKS



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