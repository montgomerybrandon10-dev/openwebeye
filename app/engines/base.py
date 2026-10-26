"""Base engine types."""
from dataclasses import dataclass, field
from typing import Any, List, Optional

@dataclass
class Candidate:
    image_url: str = ""
    source_url: str = ""
    title: str = ""
    thumb_url: str = ""
    engine: str = ""
    engine_score: float = 0.0

@dataclass
class SearchContext:
    query_path: str
    face_path: str
    face_bbox: Optional[list] = None
    session: Any = None
    browser: Any = None
    emit: Any = None
    max_results: int = 20

class Engine:
    key = ""
    name = ""
    async def probe(self):
        class R: available = True; reason = ""
        return R()
    async def search(self, ctx: SearchContext) -> List[Candidate]:
        return []
