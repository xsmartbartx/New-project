from __future__ import annotations

from typing import List, Sequence

from ..config.settings import ROMAN_TO_DEGREE
from ..core.utils import clamp
from .scales import degree_to_midi


def chord_from_degree(scale_pc: Sequence[int], degree: int, quality: str, octave: int = 4) -> List[int]:
    root = degree_to_midi(scale_pc, degree, octave)
    third = degree_to_midi(scale_pc, ((degree + 1 - 1) % 7) + 1, octave + (1 if degree + 1 > 7 else 0))
    fifth = degree_to_midi(scale_pc, ((degree + 3 - 1) % 7) + 1, octave + (1 if degree + 3 > 7 else 0))
    chord = [root, third, fifth]

    if quality == "7th":
        seventh = degree_to_midi(scale_pc, ((degree + 5 - 1) % 7) + 1, octave + (1 if degree + 5 > 7 else 0))
        chord.append(seventh)
    elif quality == "sus2":
        second = degree_to_midi(scale_pc, ((degree) % 7) + 1, octave + (1 if degree > 7 else 0))
        chord = [root, second, fifth]
    elif quality == "sus4":
        fourth = degree_to_midi(scale_pc, ((degree + 2 - 1) % 7) + 1, octave + (1 if degree + 2 > 7 else 0))
        chord = [root, fourth, fifth]

    return [clamp(n, 36, 96) for n in chord]


def chord_tones_for_bar(progression: Sequence[str], bar: int, scale_pc: Sequence[int], chord_mode: str) -> List[int]:
    symbol = progression[bar % len(progression)]
    degree = ROMAN_TO_DEGREE[symbol]
    return chord_from_degree(scale_pc, degree, chord_mode, octave=5)

