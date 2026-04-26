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

    def test_list_page_pagination_shows_10_posts_per_page(self):
        for i in range(1, 26):
            self.client.post(
                "/posts/new",
                data={"title": f"제목 {i}", "content": f"내용 {i}"},
                follow_redirects=False,
            )

        page_1_response = self.client.get("/?page=1")
        self.assertEqual(page_1_response.status_code, 200)
        page_1_body = page_1_response.data.decode()
        self.assertIn("1 / 3", page_1_body)
        self.assertIn("제목 25", page_1_body)
        self.assertIn("제목 16", page_1_body)
        self.assertNotIn("제목 15", page_1_body)
        self.assertIn("cursor-not-allowed\">이전", page_1_body)
        self.assertIn("/?page=2", page_1_body)

        page_2_response = self.client.get("/?page=2")
        self.assertEqual(page_2_response.status_code, 200)
        page_2_body = page_2_response.data.decode()
        self.assertIn("2 / 3", page_2_body)
        self.assertIn("제목 15", page_2_body)
        self.assertIn("제목 6", page_2_body)
        self.assertNotIn("제목 16", page_2_body)
        self.assertNotIn("제목 5", page_2_body)
        self.assertIn("/?page=1", page_2_body)
        self.assertIn("/?page=3", page_2_body)

        page_3_response = self.client.get("/?page=3")
        self.assertEqual(page_3_response.status_code, 200)
        page_3_body = page_3_response.data.decode()
        self.assertIn("3 / 3", page_3_body)
        self.assertIn("제목 5", page_3_body)
        self.assertIn("제목 1", page_3_body)
        self.assertNotIn("제목 6", page_3_body)
        self.assertIn("cursor-not-allowed\">다음", page_3_body)

    def test_list_page_search_filters_title_or_content_with_pagination(self):
        for i in range(1, 13):
            self.client.post(
                "/posts/new",
                data={"title": f"파이썬 팁 {i}", "content": f"검색 대상 내용 {i}"},
                follow_redirects=False,
            )

        for i in range(1, 6):
            self.client.post(
                "/posts/new",
                data={"title": f"일반 글 {i}", "content": f"파이썬 관련 메모 {i}"},
                follow_redirects=False,
            )

        for i in range(1, 8):
            self.client.post(
                "/posts/new",
                data={"title": f"기타 글 {i}", "content": f"무관한 내용 {i}"},
                follow_redirects=False,
            )

        page_1_response = self.client.get('/?q=파이썬&page=1')
        self.assertEqual(page_1_response.status_code, 200)
        page_1_body = page_1_response.data.decode()
        self.assertIn("1 / 2", page_1_body)
        self.assertIn("일반 글 5", page_1_body)
        self.assertIn("파이썬 팁 12", page_1_body)
        self.assertIn("파이썬 팁 8", page_1_body)
        self.assertNotIn("파이썬 팁 7", page_1_body)
        self.assertNotIn("기타 글 1", page_1_body)
        self.assertIn("/?page=2&amp;q=", page_1_body)

        page_2_response = self.client.get('/?q=파이썬&page=2')
        self.assertEqual(page_2_response.status_code, 200)
        page_2_body = page_2_response.data.decode()
        self.assertIn("2 / 2", page_2_body)
        self.assertIn("파이썬 팁 7", page_2_body)
        self.assertIn("파이썬 팁 1", page_2_body)
        self.assertIn("cursor-not-allowed\">다음", page_2_body)
        self.assertIn("/?page=1&amp;q=", page_2_body)

    def test_list_page_search_shows_empty_message_when_no_result(self):
        self.client.post(
            "/posts/new",
            data={"title": "테스트 제목", "content": "테스트 내용"},
            follow_redirects=False,
        )

        response = self.client.get('/?q=없는검색어')
        self.assertEqual(response.status_code, 200)
        body = response.data.decode()
        self.assertIn("검색 결과가 없습니다", body)

    def test_list_page_sort_defaults_to_latest_and_can_change(self):
        self.client.post(
            "/posts/new",
            data={"title": "다", "content": "내용 C"},
            follow_redirects=False,
        )
        self.client.post(
            "/posts/new",
            data={"title": "가", "content": "내용 A"},
            follow_redirects=False,
        )
        self.client.post(
            "/posts/new",
            data={"title": "나", "content": "내용 B"},
            follow_redirects=False,
        )

        default_response = self.client.get("/")
        self.assertEqual(default_response.status_code, 200)
        default_body = default_response.data.decode()
        self.assertIn("value=\"latest\" selected", default_body)
        self.assertIn('<a href="/posts/3">나</a>', default_body)
        self.assertIn('<a href="/posts/2">가</a>', default_body)
        self.assertIn('<a href="/posts/1">다</a>', default_body)
        self.assertTrue(default_body.index('<a href="/posts/3">나</a>') < default_body.index('<a href="/posts/2">가</a>'))

        oldest_response = self.client.get('/?sort=oldest')
        self.assertEqual(oldest_response.status_code, 200)
        oldest_body = oldest_response.data.decode()
        self.assertIn("value=\"oldest\" selected", oldest_body)
        self.assertTrue(oldest_body.index('<a href="/posts/1">다</a>') < oldest_body.index('<a href="/posts/2">가</a>'))

        title_response = self.client.get('/?sort=title')
        self.assertEqual(title_response.status_code, 200)
        title_body = title_response.data.decode()
        self.assertIn("value=\"title\" selected", title_body)
        self.assertTrue(title_body.index('<a href="/posts/2">가</a>') < title_body.index('<a href="/posts/3">나</a>'))
        self.assertTrue(title_body.index('<a href="/posts/3">나</a>') < title_body.index('<a href="/posts/1">다</a>'))

    def test_list_page_sort_works_with_search_and_pagination(self):
        for title in [
            "사과 12", "사과 11", "사과 10", "사과 9", "사과 8", "사과 7",
            "사과 6", "사과 5", "사과 4", "사과 3", "사과 2", "사과 1",
        ]:
            self.client.post(
                "/posts/new",
                data={"title": title, "content": "과일"},
                follow_redirects=False,
            )

        response = self.client.get('/?q=사과&sort=title&page=1')
        self.assertEqual(response.status_code, 200)
        body = response.data.decode()
        self.assertIn("1 / 2", body)
        self.assertIn("사과 1", body)
        self.assertIn("사과 7", body)
        self.assertNotIn("사과 8", body)
        self.assertIn("/?page=2&amp;q=%EC%82%AC%EA%B3%BC&amp;sort=title", body)


if __name__ == "__main__":
    unittest.main()
