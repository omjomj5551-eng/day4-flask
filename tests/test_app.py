import os
import re
import sqlite3
import tempfile
import unittest

from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        fd, path = tempfile.mkstemp()
        os.close(fd)
        self.db_path = path

        app.config.update(TESTING=True, DATABASE=self.db_path)
        self.client = app.test_client()

        connection = sqlite3.connect(self.db_path)
        connection.execute(
            """
            CREATE TABLE posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        connection.commit()
        connection.close()

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_list_page_uses_journal_design(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        body = response.data.decode()
        self.assertIn("모아 둔 생각", body)
        self.assertIn("글쓰기", body)

    def test_create_post_redirects_to_detail(self):
        response = self.client.post(
            "/posts/new",
            data={"title": "첫 글", "content": "내용입니다."},
            follow_redirects=False,
        )

        self.assertEqual(response.status_code, 302)
        location = response.headers.get("Location", "")
        self.assertRegex(location, r"/posts/\d+$")

        detail_response = self.client.get(location)
        self.assertEqual(detail_response.status_code, 200)
        body = detail_response.data.decode()
        self.assertIn("첫 글", body)
        self.assertIn("내용입니다.", body)

    def test_new_page_uses_korean_labels(self):
        response = self.client.get("/posts/new")
        self.assertEqual(response.status_code, 200)
        body = response.data.decode()
        self.assertIn("목록으로", body)
        self.assertIn("제목을 입력하세요", body)
        self.assertIn("내용을 입력하세요", body)
        self.assertIn("발행", body)

    def test_detail_page_returns_404_for_missing_post(self):
        response = self.client.get("/posts/999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
