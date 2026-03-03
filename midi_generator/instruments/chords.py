from __future__ import annotations

from typing import List, Sequence

from ..config.settings import PPQ, ROMAN_TO_DEGREE
from ..core.types import Note, Preset, TimeSignature
from ..theory.chords import chord_from_degree


def build_chords(
    progression: Sequence[str],
    bars: int,
    time_signature: TimeSignature,
    scale_pc: Sequence[int],
    chord_mode: str,
) -> List[Note]:
    events: List[Note] = []
    ticks_bar = time_signature.numerator * PPQ
    for bar in range(bars):
        symbol = progression[bar % len(progression)]
        degree = ROMAN_TO_DEGREE[symbol]
        quality = chord_mode
        if symbol in ("V", "VII") and chord_mode == "triad":
            quality = "7th"
        chord_notes = chord_from_degree(scale_pc, degree, quality, octave=4)
        start = bar * ticks_bar
        duration = ticks_bar
        for midi_note in chord_notes:
            events.append(Note(midi_note=midi_note, velocity=70, start_tick=start, duration_ticks=duration, channel=0))
    return events


def generate(preset: Preset, progression: Sequence[str], scale_pc: Sequence[int]) -> List[Note]:
    return build_chords(
        progression=progression,
        bars=preset.bars,
        time_signature=preset.time_signature,
        scale_pc=scale_pc,
        chord_mode=preset.chord_mode,
    )

