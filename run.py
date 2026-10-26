"""OpenWebEye entry point."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

def main():
    import uvicorn
    from app.config import config
    print(f"OpenWebEye running on http://0.0.0.0:{config.PORT}")
    uvicorn.run("app.main:app", host="0.0.0.0", port=config.PORT)

if __name__ == "__main__":
    main()
