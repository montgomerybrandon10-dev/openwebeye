"""Engine registry."""
from .base import Engine, Candidate, SearchContext
from .yandex import YandexEngine
from .google_lens import GoogleLensEngine
from .bing import BingEngine
from .tineye import TinEyeEngine

_ENGINES = {
    "yandex": YandexEngine(),
    "google_lens": GoogleLensEngine(),
    "bing": BingEngine(),
    "tineye": TinEyeEngine(),
}

def get_engine(key):
    return _ENGINES.get(key)

def registry_info():
    return [{"key": k, "name": e.name} for k, e in _ENGINES.items()]
