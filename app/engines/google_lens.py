"""Google Lens reverse image search."""
from app.engines.base import Candidate, SearchContext
from app.engines.browser import BrowserEngine

class GoogleLensEngine(BrowserEngine):
    key = "google_lens"
    name = "Google Lens"
    async def search(self, ctx: SearchContext):
        return []
