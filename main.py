import requests
from dotenv import load_dotenv
import os
import json
from send_email import send_email
from deep_translator import GoogleTranslator
import re
import html

_translation_cache = {}


def translate_to_english(text: str) -> str:
    try:
        return GoogleTranslator(source="auto", target="en").translate(text)
    except Exception:
        return text


def translate_to_english_cached(text: str) -> str:
    if text in _translation_cache:
        return _translation_cache[text]
    res = translate_to_english(text)
    _translation_cache[text] = res
    return res


def translate_to_ukrainian(text: str) -> str:
    if not needs_translation(text):
        return text
    try:
        return GoogleTranslator(source="auto", target="uk").translate(text)
    except Exception:
        return text


def needs_translation(text: str) -> bool:
    if re.search(r'[\u4e00-\u9fff]', text):
        return True
    if not re.search(r'[а-яіїєґ]', text.lower()):
        return True
    return False


def strip_html(text: str) -> str:
    text = html.unescape(text)
    text = re.sub(r'<[^>]+>', ' ', text)
    return text


def trim_incomplete_tail(text: str) -> str:
    if re.search(r'[A-Za-zА-Яа-яІіЇїЄєҐґ]{1,5}$', text):
        last_dot = text.rfind(".")
        if last_dot != -1:
            return text[:last_dot + 1]
    return text


def clean_snippet(text: str) -> str:
    text = strip_html(text)
    text = text.split("[+")[0]
    text = text.split("…")[0]
    text = re.sub(r'\b\d{1,2}/\d{1,2}\s+[A-Z][A-Za-z\s.&-]{2,40}', '', text)
    text = re.sub(r'\s*[•◦▪–\-]\s*', '. ', text)
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)
    text = trim_incomplete_tail(text)
    return text.strip()


def extract_snippets_limited(
        content: str,
        keywords: list[str],
        window: int = 120,
        max_snippets: int = 2
) -> list[str]:
    if not content:
        return []
    content_lower = content.lower()
    snippets = []
    used_ranges = []
    for kw in keywords:
        idx = content_lower.find(kw.lower())
        if idx == -1:
            continue
        start = max(0, idx - window)
        end = min(len(content), idx + len(kw) + window)
        if any(start <= r_end and end >= r_start for r_start, r_end in
               used_ranges):
            continue
        snippet = content[start:end].strip()
        snippet = snippet.split("[+")[0].strip()
        snippets.append(snippet)
        used_ranges.append((start, end))
        if len(snippets) >= max_snippets:
            break
    return snippets


def content_contains_keywords_any_lang(content: str,
                                       keywords: list[str]) -> bool:
    if not content:
        return False
    content_en = translate_to_english_cached(content).lower()
    return any(k.lower() in content_en for k in keywords)


KEYWORDS = ["dryer", "washer"]
SEARCH_STRING = "Whirlpool"

load_dotenv()
API_KEY = os.getenv("API_KEY")

URL = (
    f"https://newsapi.org/v2/everything"
    f"?q={SEARCH_STRING}&from=2025-11-29"
    f"&sortBy=publishedAt&apiKey={API_KEY}"
)

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(URL, headers=headers)
parsed_json = response.json()

email_body = "<h2>Important News</h2>"

for article in parsed_json.get("articles", []):
    content = article.get("content", "")
    if not content_contains_keywords_any_lang(content, KEYWORDS):
        continue

    content_for_snippets = content
    if not any(k.lower() in content.lower() for k in KEYWORDS):
        content_for_snippets = translate_to_english_cached(content)

    snippets = extract_snippets_limited(content_for_snippets, KEYWORDS)
    if not snippets:
        continue

    title_ua = translate_to_ukrainian(article["title"])
    print(title_ua)
    url = article["url"]

    email_body += f"""
    <div style="margin-bottom:18px;">
        <div>
            <a href="{url}" target="_blank"
               style="font-weight:bold; color:#1a73e8; text-decoration:none;">
               {title_ua}
            </a>
        </div>
    """

    for snip in snippets:
        snip_clean = clean_snippet(snip)
        snip_ua = translate_to_ukrainian(snip_clean)
        email_body += f"""
        <div style="margin-left:12px; margin-top:6px; color:#444;">
            {snip_ua}
        </div>
        """

    email_body += "</div>"

send_email(
    to="desaga@gmail.com",
    subject="Important news",
    body_html=email_body
)
