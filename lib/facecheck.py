"""FaceCheck.id API client."""
import os, time, requests
from typing import Optional

class FaceCheckClient:
    BASE = "https://facecheck.id"
    def __init__(self, api_token: Optional[str] = None):
        self.api_token = api_token or os.getenv("FACECHECK_API_TOKEN", "")
        self.available = bool(self.api_token)

    def search(self, image_bytes: bytes) -> dict:
        if not self.available:
            return {"error": "FACECHECK_API_TOKEN not set", "results": []}
        headers = {"accept": "application/json", "Authorization": self.api_token}
        try:
            r = requests.post(f"{self.BASE}/api/upload_pic", headers=headers, files={"images": ("query.jpg", image_bytes, "image/jpeg")}, timeout=30)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            return {"error": str(e), "results": []}
        if data.get("error"):
            return {"error": data["error"], "results": []}
        id_search = data.get("id_search")
        if not id_search:
            return {"error": "No id_search", "results": []}
        payload = {"id_search": id_search, "with_progress": True, "status_only": False}
        for _ in range(45):
            try:
                r = requests.post(f"{self.BASE}/api/search", headers=headers, json=payload, timeout=30)
                r.raise_for_status()
                data = r.json()
            except Exception as e:
                return {"error": str(e), "results": []}
            if data.get("output"):
                items = data["output"].get("items", [])
                results = [{"score": item.get("score", 0)/100.0, "url": item.get("url"), "source": "facecheck"} for item in items]
                return {"results": results, "id_search": id_search}
            time.sleep(1)
        return {"error": "Timeout", "results": []}

facecheck = FaceCheckClient()
