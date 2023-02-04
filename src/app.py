# app.py

from bumbo.api import API
from .auth import login_required, TokenMiddleware, STATIC_TOKEN, on_exception
from .storage import BookStorage


app = API(templates_dir="src/templates", static_dir="src/static")
app.add_middleware(TokenMiddleware)
app.add_exception_handler(on_exception)
book_storage = BookStorage()
book_storage.create(name="7 habits of highly effective people", author="Stephen Covey")


@app.route("/", allowed_methods=["get"])
def index(req, resp):
    books = book_storage.all()
    resp.html = app.template("index.html", context={"books": books})


@app.route("/login", allowed_methods=["post"])
def login(req, resp):
    print(f"..:: POST /login ::..\nreq: {req}\nresp: {resp}\n")
    resp.json = {"token": STATIC_TOKEN}


@app.route("/books", allowed_methods=["post"])
@login_required
def create_book(req, resp):
    print(f"..:: POST /books ::..\nreq{req}\nresp: {resp}\n")
    book = book_storage.create(**req.POST)

    resp.status_code = 201
    resp.json = book._asdict()


@app.route("/books/{id:d}", allowed_methods=["delete"])
@login_required
def delete_book(req, resp, id):
    book_storage.delete(id)

    resp.status_code = 204


