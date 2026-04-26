import os
import sqlite3
import sys
from datetime import datetime

from crawler import LIMIT, RSS_URL, fetch_rss, parse_items


def ensure_posts_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()


def seed_posts() -> int:
    database_path = os.getenv("DATABASE_PATH", "board.db")
    database_dir = os.path.dirname(database_path)
    if database_dir:
        os.makedirs(database_dir, exist_ok=True)

    conn = sqlite3.connect(database_path)
    try:
        ensure_posts_table(conn)

        xml_text = fetch_rss(RSS_URL)
        items = parse_items(xml_text, LIMIT)

        added_count = 0
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for item in items:
            title = item["title"].strip()
            summary = item["summary"].strip()
            link = item["link"].strip()
            content = f"{summary}\n\n원문 링크: {link}" if link else summary

            exists = conn.execute(
                "SELECT 1 FROM posts WHERE title = ? LIMIT 1",
                (title,),
            ).fetchone()
            if exists:
                continue

            conn.execute(
                "INSERT INTO posts (title, content, created_at) VALUES (?, ?, ?)",
                (title, content, now),
            )
            added_count += 1

        conn.commit()
        return added_count
    finally:
        conn.close()


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    added_count = seed_posts()
    print(f"{added_count}건 추가됨")


if __name__ == "__main__":
    main()
