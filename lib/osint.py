"""OSINT reverse image search — generates working search links."""
import base64
from urllib.parse import quote

class OSINTClient:
    def search(self, image_bytes: bytes) -> dict:
        # Encode a small preview for data URLs where useful
        b64 = base64.b64encode(image_bytes).decode()
        data_url = f"data:image/jpeg;base64,{b64}"
        
        results = [
            {
                "source": "Google Lens",
                "url": "https://lens.google.com/",
                "note": "Upload the image at Google Lens for best free results",
                "type": "manual",
            },
            {
                "source": "Yandex Images",
                "url": "https://yandex.com/images/",
                "note": "Strong for faces — upload the image",
                "type": "manual",
            },
            {
                "source": "Bing Visual Search",
                "url": "https://www.bing.com/visualsearch",
                "note": "Upload for visual matches",
                "type": "manual",
            },
            {
                "source": "TinEye",
                "url": "https://tineye.com/",
                "note": "Finds exact and modified copies",
                "type": "manual",
            },
            {
                "source": "FaceCheck.id",
                "url": "https://facecheck.id/",
                "note": "Face-specific search (free tier available)",
                "type": "manual",
            },
            {
                "source": "PimEyes",
                "url": "https://pimeyes.com/en",
                "note": "Paid face search",
                "type": "manual",
            },
        ]
        return {
            "results": results,
            "note": "Click a link and upload your image for full results. Automated face APIs require a paid key.",
        }

osint = OSINTClient()
