from fastapi import FastAPI, Body

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
async def create_book(book_request= Body()):
    BOOKS.append(book_request)


