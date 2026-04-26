import os
import sqlite3
from datetime import datetime

from flask import Flask, abort, g, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["DATABASE"] = os.getenv("DATABASE_PATH", "board.db")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db():
    database_dir = os.path.dirname(app.config["DATABASE"])
    if database_dir:
        os.makedirs(database_dir, exist_ok=True)

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
    per_page = 10

    page = request.args.get("page", default=1, type=int)
    if page < 1:
        page = 1

    query = request.args.get("q", default="", type=str).strip()
    sort = request.args.get("sort", default="latest", type=str)

    order_by = "id DESC"
    if sort == "oldest":
        order_by = "id ASC"
    elif sort == "title":
        order_by = "title ASC"
    else:
        sort = "latest"

    where_clause = ""
    params = []
    if query:
        where_clause = "WHERE title LIKE ? OR content LIKE ?"
        keyword = f"%{query}%"
        params.extend([keyword, keyword])

    total_posts = db.execute(
        f"SELECT COUNT(*) FROM posts {where_clause}",
        params,
    ).fetchone()[0]
    total_pages = max(1, (total_posts + per_page - 1) // per_page)

    if page > total_pages:
        page = total_pages

    offset = (page - 1) * per_page
    posts = db.execute(
        f"SELECT id, title, content, created_at FROM posts {where_clause} ORDER BY {order_by} LIMIT ? OFFSET ?",
        [*params, per_page, offset],
    ).fetchall()

    return render_template(
        "list.html",
        posts=posts,
        page=page,
        total_pages=total_pages,
        has_prev=(page > 1),
        has_next=(page < total_pages),
        query=query,
        sort=sort,
    )


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

    return render_template(
        "new.html",
        post=None,
        form_title="글쓰기",
        submit_label="발행",
        form_action=url_for("create_post"),
    )


@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    db = get_db()
    post = db.execute(
        "SELECT id, title, content, created_at FROM posts WHERE id = ?", (post_id,)
    ).fetchone()

    if post is None:
        abort(404)

    return render_template("detail.html", post=post)


@app.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    db = get_db()
    post = db.execute(
        "SELECT id, title, content, created_at FROM posts WHERE id = ?", (post_id,)
    ).fetchone()

    if post is None:
        abort(404)

    if request.method == "POST":
        title = request.form["title"].strip()
        content = request.form["content"].strip()

        db.execute(
            "UPDATE posts SET title = ?, content = ? WHERE id = ?",
            (title, content, post_id),
        )
        db.commit()
        return redirect(url_for("post_detail", post_id=post_id))

    return render_template(
        "new.html",
        post=post,
        form_title="글 수정",
        submit_label="수정 완료",
        form_action=url_for("edit_post", post_id=post_id),
    )


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    db = get_db()
    db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    db.commit()
    return redirect(url_for("list_posts"))


with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run(debug=True)
