# app.py

from bumbo.api import API
from bumbo.orm import Database

from .auth import login_required, TokenMiddleware, STATIC_TOKEN, on_exception
from .models import Book
from .storage import BookStorage

app = API(templates_dir="src/templates", static_dir="src/static")
app.add_middleware(TokenMiddleware)
app.add_exception_handler(on_exception)
book_storage = BookStorage()
book_storage.create(name="7 habits of highly effective people", author="Stephen Covey")
db = Database("./myapp.db")
db.create(Book)


@app.route("/", allowed_methods=["get"])
def index(req, resp):
    books = db.all(Book)
    resp.html = app.template("index.html", context={"books": books})


@app.route("/login", allowed_methods=["post"])
def login(req, resp):
    print(f"..:: POST /login ::..\nreq: {req}\nresp: {resp}\n")
    resp.json = {"token": STATIC_TOKEN}


@app.route("/books", allowed_methods=["post"])
@login_required
def create_book(req, resp):
    print(f"..:: POST /books ::..\nreq{req}\nresp: {resp}\n")
    book = Book(**req.POST)
    db.save(book)

    resp.status_code = 201
    resp.json = {"name": book.name, "author": book.author}


@app.route("/books/{id:d}", allowed_methods=["delete"])
@login_required
def delete_book(req, resp, id):
    db.delete(Book, id)

    resp.status_code = 204


