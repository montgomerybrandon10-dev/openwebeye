"""PimEyes client (best-effort)."""
import os

class PimEyesClient:
    def __init__(self):
        self.available = bool(os.getenv("SCRAPINGBEE_API_KEY"))

    def search(self, image_bytes: bytes) -> dict:
        if not self.available:
            return {"error": "No ScrapingBee key", "results": [], "note": "PimEyes has no public API"}
        return {"results": [], "note": "PimEyes scraping limited"}

pimeyes = PimEyesClient()
