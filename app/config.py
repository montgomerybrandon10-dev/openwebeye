"""Minimal config for OpenWebEye."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    BASE_DIR = BASE_DIR
    PORT = int(os.getenv("PORT", "8000"))
    HOST = os.getenv("HOST", "0.0.0.0")
    UPLOAD_DIR = BASE_DIR / "uploads"
    DATA_DIR = BASE_DIR / "data"
    STATIC_DIR = BASE_DIR / "static"
    MAX_UPLOAD_MB = 10
    ENGINE_TIMEOUT_S = 60
    MAX_RESULTS_PER_ENGINE = 20

config = Config()
