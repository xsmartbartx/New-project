from __future__ import annotations

from typing import List

from ..config.settings import PROGRESSION_PRESETS


def choose_progression(genre: str, mood: str) -> List[str]:
    genre_map = PROGRESSION_PRESETS.get(genre, PROGRESSION_PRESETS["hip-hop"])
    return genre_map.get(mood, genre_map["chill"])

