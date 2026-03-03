from __future__ import annotations

from typing import List, Sequence

from ..config.settings import NOTE_NAME_TO_SEMITONE, SCALES


def parse_key(key: str) -> int:
    if key not in NOTE_NAME_TO_SEMITONE:
        raise ValueError(f"Unsupported key: {key}")
    return NOTE_NAME_TO_SEMITONE[key]


def scale_pitch_classes(key_root: int, scale_name: str) -> List[int]:
    if scale_name not in SCALES:
        raise ValueError(f"Unsupported scale: {scale_name}")
    return [(key_root + interval) % 12 for interval in SCALES[scale_name]]


def degree_to_midi(scale_pc: Sequence[int], degree: int, octave: int) -> int:
    idx = (degree - 1) % 7
    return scale_pc[idx] + (octave + 1) * 12

