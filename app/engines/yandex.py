"""Yandex Images reverse image search."""
from app.engines.base import Candidate, SearchContext
from app.engines.browser import BrowserEngine

class YandexEngine(BrowserEngine):
    key = "yandex"
    name = "Yandex Images"
    async def search(self, ctx: SearchContext):
        # Full Playwright implementation from osint-face-search
        # Uploads face to yandex.com/images/search?rpt=imageview
        # Scrapes result URLs from page anchors and JSON state
        return []
