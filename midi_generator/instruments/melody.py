from __future__ import annotations

import random
from typing import List, Sequence

from ..config.settings import PPQ
from ..core.types import Note, Preset
from ..core.utils import clamp
from ..theory.chords import chord_tones_for_bar


def build_melody(
    progression: Sequence[str],
    bars: int,
    beats_per_bar: int,
    scale_pc: Sequence[int],
    rng: random.Random,
    genre: str,
) -> List[Note]:
    events: List[Note] = []
    step_division = 8 if genre in ("jazz", "hip-hop", "trap") else 4
    step_ticks = PPQ // (step_division // 2)
    steps_per_bar = beats_per_bar * (step_division // 2)

    scale_pitch_pool: List[int] = []
    for octave in (4, 5, 6):
        scale_pitch_pool.extend([(pc + (octave + 1) * 12) for pc in scale_pc])

    for bar in range(bars):
        chord_tones = chord_tones_for_bar(progression, bar, scale_pc, "triad")
        for step in range(steps_per_bar):
            strong = step % (step_division // 2) == 0
            play_prob = 0.55 if strong else 0.35
            if rng.random() > play_prob:
                continue
            if strong or rng.random() < 0.7:
                midi_note = rng.choice(chord_tones + [n + 12 for n in chord_tones])
            else:
                midi_note = rng.choice(scale_pitch_pool)
            duration_steps = 1 if rng.random() < 0.8 else 2
            duration = step_ticks * duration_steps
            start = bar * beats_per_bar * PPQ + step * step_ticks
            velocity = rng.randint(62, 102 if strong else 88)
            events.append(
                Note(
                    midi_note=clamp(midi_note, 60, 92),
                    velocity=velocity,
                    start_tick=start,
                    duration_ticks=duration,
                    channel=0,
                )
            )
    return events


def generate(preset: Preset, progression: Sequence[str], scale_pc: Sequence[int], rng: random.Random) -> List[Note]:
    return build_melody(
        progression=progression,
        bars=preset.bars,
        beats_per_bar=preset.time_signature.numerator,
        scale_pc=scale_pc,
        rng=rng,
        genre=preset.genre,
    )

