import sqlite3
from datetime import datetime

from flask import Flask, abort, g, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["DATABASE"] = "board.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db():
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    db.commit()


@app.teardown_appcontext
def close_db(error):
    _ = error
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/")
def list_posts():
    db = get_db()
    posts = db.execute(
        "SELECT id, title, content, created_at FROM posts ORDER BY id DESC"
    ).fetchall()
    return render_template("list.html", posts=posts)


@app.route("/posts/new", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        title = request.form["title"].strip()
        content = request.form["content"].strip()

        db = get_db()
        cursor = db.execute(
            "INSERT INTO posts (title, content, created_at) VALUES (?, ?, ?)",
            (title, content, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        db.commit()
        return redirect(url_for("post_detail", post_id=cursor.lastrowid))

    return render_template("new.html")


@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    db = get_db()
    post = db.execute(
        "SELECT id, title, content, created_at FROM posts WHERE id = ?", (post_id,)
    ).fetchone()

    if post is None:
        abort(404)

    return render_template("detail.html", post=post)


with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run(debug=True)
