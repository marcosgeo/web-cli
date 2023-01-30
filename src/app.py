# app.py

from bumbo.api import API

app = API(templates_dir="src/templates", static_dir="src/static")


@app.route("/", allowed_methods=["get"])
def index(req, resp):
    resp.html = app.template("index.html")

