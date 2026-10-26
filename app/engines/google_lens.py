"""Google Lens reverse image search via Playwright."""
from .base import Engine, Candidate, SearchContext

class GoogleLensEngine(Engine):
    key = "google_lens"
    name = "Google Lens"
    async def search(self, ctx: SearchContext) -> list:
        return []
