import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "openwebeye.db"
FAISS_INDEX_PATH = DATA_DIR / "faces.index"
UPLOAD_DIR = DATA_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
THUMB_DIR = DATA_DIR / "thumbs"
THUMB_DIR.mkdir(exist_ok=True)

INSIGHTFACE_MODEL = os.getenv("INSIGHTFACE_MODEL", "buffalo_l")
DET_SIZE = (640, 640)
DET_THRESH = float(os.getenv("DET_THRESH", "0.75"))

SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.55"))
TOP_K = int(os.getenv("TOP_K", "50"))

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
SITE_URL = os.getenv("SITE_URL", "https://openwebeye.com")
ADMIN_KEY = os.getenv("ADMIN_KEY", "changeme-admin-key")

MAX_UPLOAD_MB = 10
