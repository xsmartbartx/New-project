from __future__ import annotations

import random
from typing import List, Sequence

from ..config.settings import PPQ, ROMAN_TO_DEGREE
from ..core.types import Note, Preset
from ..core.utils import clamp
from ..theory.scales import degree_to_midi


def build_bass(
    progression: Sequence[str],
    bars: int,
    beats_per_bar: int,
    scale_pc: Sequence[int],
    rng: random.Random,
    genre: str,
) -> List[Note]:
    events: List[Note] = []
    step_ticks = PPQ // 2  # 8th-note grid
    steps_per_bar = beats_per_bar * 2

    for bar in range(bars):
        symbol = progression[bar % len(progression)]
        degree = ROMAN_TO_DEGREE[symbol]
        root = degree_to_midi(scale_pc, degree, 2)
        for step in range(steps_per_bar):
            beat_pos = step / 2.0
            strong = step % 2 == 0
            should_play = strong or rng.random() < (0.35 if genre in ("edm", "house", "techno") else 0.5)
            if not should_play:
                continue
            midi_note = root
            if rng.random() < 0.18:
                midi_note += 12
            if rng.random() < 0.14:
                midi_note -= 5
            midi_note = clamp(midi_note, 28, 60)
            vel = 92 if beat_pos in (0.0, 2.0) else rng.randint(68, 88)
            duration = step_ticks if genre not in ("house", "techno") else int(step_ticks * 0.9)
            start = bar * beats_per_bar * PPQ + step * step_ticks
            events.append(Note(midi_note=midi_note, velocity=vel, start_tick=start, duration_ticks=duration, channel=0))
    return events


def generate(preset: Preset, progression: Sequence[str], scale_pc: Sequence[int], rng: random.Random) -> List[Note]:
    return build_bass(
        progression=progression,
        bars=preset.bars,
        beats_per_bar=preset.time_signature.numerator,
        scale_pc=scale_pc,
        rng=rng,
        genre=preset.genre,
    )

