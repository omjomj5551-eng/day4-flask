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

    def test_detail_page_has_edit_delete_buttons_and_confirm_dialog(self):
        create_response = self.client.post(
            "/posts/new",
            data={"title": "수정삭제 테스트", "content": "원본 내용"},
            follow_redirects=False,
        )
        location = create_response.headers.get("Location", "")

        detail_response = self.client.get(location)
        self.assertEqual(detail_response.status_code, 200)
        body = detail_response.data.decode()
        self.assertIn("수정", body)
        self.assertIn("삭제", body)
        self.assertIn("정말 삭제할까요?", body)

    def test_edit_page_reuses_new_form_and_updates_post(self):
        create_response = self.client.post(
            "/posts/new",
            data={"title": "원제목", "content": "원내용"},
            follow_redirects=False,
        )
        location = create_response.headers.get("Location", "")
        post_id = int(location.rsplit("/", 1)[-1])

        edit_get_response = self.client.get(f"/posts/{post_id}/edit")
        self.assertEqual(edit_get_response.status_code, 200)
        edit_body = edit_get_response.data.decode()
        self.assertIn("글 수정", edit_body)
        self.assertIn("수정 완료", edit_body)
        self.assertIn("value=\"원제목\"", edit_body)
        self.assertIn("원내용", edit_body)

        edit_post_response = self.client.post(
            f"/posts/{post_id}/edit",
            data={"title": "수정된 제목", "content": "수정된 내용"},
            follow_redirects=False,
        )
        self.assertEqual(edit_post_response.status_code, 302)

        detail_response = self.client.get(f"/posts/{post_id}")
        self.assertEqual(detail_response.status_code, 200)
        detail_body = detail_response.data.decode()
        self.assertIn("수정된 제목", detail_body)
        self.assertIn("수정된 내용", detail_body)

    def test_delete_post_removes_post(self):
        create_response = self.client.post(
            "/posts/new",
            data={"title": "삭제될 글", "content": "삭제될 내용"},
            follow_redirects=False,
        )
        location = create_response.headers.get("Location", "")
        post_id = int(location.rsplit("/", 1)[-1])

        delete_response = self.client.post(
            f"/posts/{post_id}/delete",
            follow_redirects=False,
        )
        self.assertEqual(delete_response.status_code, 302)

        detail_response = self.client.get(f"/posts/{post_id}")
        self.assertEqual(detail_response.status_code, 404)

    def test_detail_page_returns_404_for_missing_post(self):
        response = self.client.get("/posts/999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
