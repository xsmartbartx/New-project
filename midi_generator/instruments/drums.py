from __future__ import annotations

import random
from typing import List

from ..config.settings import GM_DRUM_NOTES, PPQ
from ..core.types import Note, Preset
from ..core.utils import clamp
from ..humanization.timing import ms_to_ticks, swing_offset_ticks


def drum_velocity(base: int, variance: int, accent: bool, rng: random.Random) -> int:
    bump = 10 if accent else 0
    return clamp(base + bump + rng.randint(-variance, variance), 1, 127)


def build_drums(
    preset: Preset,
    rng: random.Random,
) -> List[Note]:
    """
    Drum generator closely matching the original `generator.py` behavior:
    - 16th grid core
    - genre-dependent kick patterns
    - backbeat snare with optional ghost notes
    - hats with optional trap rolls
    - swing + timing jitter + velocity variance applied inside this builder
    """

    bars = preset.bars
    beats_per_bar = preset.time_signature.numerator
    genre = preset.genre
    complexity = min(max(preset.complexity, 0.0), 1.0)
    swing = preset.swing
    humanize_ms = preset.humanize_ms
    humanize_vel = preset.humanize_velocity

    events: List[Note] = []
    step_ticks = PPQ // 4  # 16th notes
    steps_per_bar = beats_per_bar * 4
    total_steps = bars * steps_per_bar

    # Keep legacy behavior: convert ms jitter using bpm=120 baseline.
    jitter_ticks = ms_to_ticks(humanize_ms, bpm=120, ppq=PPQ)

    for idx in range(total_steps):
        bar = idx // steps_per_bar
        step_in_bar = idx % steps_per_bar
        base_start = bar * beats_per_bar * PPQ + step_in_bar * step_ticks
        start = base_start + swing_offset_ticks(step_in_bar, step_ticks, swing)
        start += rng.randint(-jitter_ticks, jitter_ticks)
        start = max(0, start)

        on_beat = step_in_bar % 4 == 0

        kick_prob = 0.1
        if step_in_bar in (0, 8):
            kick_prob = 0.9
        elif step_in_bar in (4, 12):
            kick_prob = 0.45
        if genre in ("house", "techno"):
            kick_prob = 0.95 if on_beat else 0.08
        if rng.random() < kick_prob + (complexity * 0.1):
            events.append(
                Note(
                    midi_note=GM_DRUM_NOTES["kick"],
                    velocity=drum_velocity(95, humanize_vel, accent=on_beat, rng=rng),
                    start_tick=start,
                    duration_ticks=int(step_ticks * 0.35),
                    channel=9,
                )
            )

        if step_in_bar in (4, 12):
            events.append(
                Note(
                    midi_note=GM_DRUM_NOTES["snare"],
                    velocity=drum_velocity(100, humanize_vel, accent=True, rng=rng),
                    start_tick=start,
                    duration_ticks=int(step_ticks * 0.35),
                    channel=9,
                )
            )
            if rng.random() < (0.25 + complexity * 0.3):
                ghost_start = max(0, start - int(step_ticks * 0.5))
                events.append(
                    Note(
                        midi_note=GM_DRUM_NOTES["snare"],
                        velocity=drum_velocity(45, humanize_vel, accent=False, rng=rng),
                        start_tick=ghost_start,
                        duration_ticks=int(step_ticks * 0.25),
                        channel=9,
                    )
                )

        hat_resolution = 2 if genre in ("house", "techno", "edm") else 1
        if step_in_bar % hat_resolution == 0:
            hat_note = GM_DRUM_NOTES["hat_closed"]
            if genre == "trap" and rng.random() < 0.18:
                hat_note = GM_DRUM_NOTES["hat_open"]
            events.append(
                Note(
                    midi_note=hat_note,
                    velocity=drum_velocity(70, humanize_vel, accent=on_beat, rng=rng),
                    start_tick=start,
                    duration_ticks=int(step_ticks * 0.2),
                    channel=9,
                )
            )

        if genre == "trap" and rng.random() < (0.05 + complexity * 0.15):
            roll_start = start
            roll_sub = step_ticks // 4
            for r in range(3):
                events.append(
                    Note(
                        midi_note=GM_DRUM_NOTES["hat_closed"],
                        velocity=drum_velocity(58 + r * 4, humanize_vel, accent=False, rng=rng),
                        start_tick=roll_start + r * roll_sub,
                        duration_ticks=int(roll_sub * 0.8),
                        channel=9,
                    )
                )

    return events


def generate(preset: Preset, rng: random.Random) -> List[Note]:
    return build_drums(preset=preset, rng=rng)

