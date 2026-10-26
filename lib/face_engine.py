"""
Face detection and embedding engine using InsightFace.
Loads lazily so the site can start without the heavy dependency.
"""
import numpy as np
from loguru import logger

from .config import INSIGHTFACE_MODEL, DET_SIZE, DET_THRESH


class FaceEngine:
    def __init__(self):
        self.app = None
        self._initialized = False
        self._available = None

    def is_available(self) -> bool:
        if self._available is not None:
            return self._available
        try:
            import insightface  # noqa
            self._available = True
        except ImportError:
            self._available = False
        return self._available

    def initialize(self):
        if self._initialized:
            return True
        if not self.is_available():
            logger.warning("InsightFace not installed — face features disabled")
            return False
        try:
            from insightface.app import FaceAnalysis
            logger.info(f"Loading InsightFace model: {INSIGHTFACE_MODEL}")
            self.app = FaceAnalysis(
                name=INSIGHTFACE_MODEL,
                providers=["CPUExecutionProvider"]
            )
            self.app.prepare(ctx_id=0, det_size=DET_SIZE, det_thresh=DET_THRESH)
            self._initialized = True
            logger.info("Face engine ready")
            return True
        except Exception as e:
            logger.error(f"Failed to init InsightFace: {e}")
            self._available = False
            return False

    def extract_faces(self, image: np.ndarray) -> list:
        if not self.initialize():
            return []
        faces = self.app.get(image)
        results = []
        for face in faces:
            if face.det_score < DET_THRESH:
                continue
            results.append({
                "embedding": face.normed_embedding.astype(np.float32),
                "bbox": face.bbox.tolist(),
                "score": float(face.det_score),
                "age": int(face.age) if hasattr(face, "age") else None,
                "gender": "male" if getattr(face, "gender", None) == 1 else "female" if getattr(face, "gender", None) == 0 else None,
            })
        return results

    def compare(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        return float(np.dot(emb1, emb2))


face_engine = FaceEngine()
