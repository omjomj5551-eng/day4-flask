import argparse
import json
import sys
import textwrap

import requests
from bs4 import BeautifulSoup

RSS_URL = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"
LIMIT = 10


def fetch_rss(url: str) -> str:
    response = requests.get(
        url,
        timeout=10,
        headers={"User-Agent": "Mozilla/5.0 (rss-crawler)"},
    )
    response.raise_for_status()
    return response.text


def parse_items(xml_text: str, limit: int = LIMIT) -> list[dict]:
    soup = BeautifulSoup(xml_text, "xml")
    items = []

    for item in soup.find_all("item", limit=limit):
        title = item.title.get_text(strip=True) if item.title else "(제목 없음)"
        raw_description = item.description.get_text(" ", strip=True) if item.description else ""
        summary = BeautifulSoup(raw_description, "html.parser").get_text(" ", strip=True)
        link = item.link.get_text(strip=True) if item.link else ""
        published_at = item.pubDate.get_text(strip=True) if item.pubDate else ""

        items.append(
            {
                "title": title,
                "summary": summary,
                "link": link,
                "published_at": published_at,
            }
        )

    return items


def print_items(items: list[dict]) -> None:
    print(f"총 {len(items)}건\n")
    for idx, item in enumerate(items, start=1):
        print(f"[{idx}] {item['title']}")
        print(f"발행시간: {item['published_at']}")
        print("요약:")
        print(textwrap.fill(item["summary"], width=88, subsequent_indent="  "))
        print(f"링크: {item['link']}")
        print("-" * 100)


def save_json(items: list[dict], output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="뉴스 RSS 크롤러")
    parser.add_argument(
        "--json",
        dest="json_path",
        help="결과를 JSON 파일로 저장할 경로 (예: news.json)",
    )
    return parser


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    args = build_parser().parse_args()

    xml_text = fetch_rss(RSS_URL)
    items = parse_items(xml_text, LIMIT)
    print_items(items)

    if args.json_path:
        save_json(items, args.json_path)
        print(f"JSON 저장 완료: {args.json_path}")


if __name__ == "__main__":
    main()
