"""OSINT reverse image search links."""
import base64
from urllib.parse import quote

class OSINTClient:
    def search(self, image_bytes: bytes) -> dict:
        b64 = base64.b64encode(image_bytes).decode()
        # Generate search URLs for major engines
        results = [
            {"source": "google", "url": f"https://lens.google.com/uploadbyurl?url=data:image/jpeg;base64,{quote(b64[:100])}", "note": "Google Lens"},
            {"source": "yandex", "url": "https://yandex.com/images/search", "note": "Yandex Images"},
            {"source": "bing", "url": "https://www.bing.com/visualsearch", "note": "Bing Visual"},
            {"source": "tineye", "url": "https://tineye.com/", "note": "TinEye"},
        ]
        return {"results": results, "note": "Open these links to search manually"}

osint = OSINTClient()
