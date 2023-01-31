# app.py

from bumbo.api import API

from .storage import BookStorage


app = API(templates_dir="src/templates", static_dir="src/static")
book_storage = BookStorage()
book_storage.create(name="7 habits of highly effective people", author="Stephen Covey")


@app.route("/", allowed_methods=["get"])
def index(req, resp):
    books = book_storage.all()
    resp.html = app.template("index.html", context={"books": books})

