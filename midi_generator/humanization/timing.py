from __future__ import annotations

import random
from typing import Iterable, List

from ..core.types import Note


def ms_to_ticks(ms: float, bpm: int, ppq: int) -> int:
    ticks_per_second = (ppq * bpm) / 60.0
    return int(round((ms / 1000.0) * ticks_per_second))


def swing_offset_ticks(step_index: int, step_ticks: int, swing_percent: float) -> int:
    if swing_percent <= 0:
        return 0
    if step_index % 2 == 0:
        return 0
    swing_amount = (swing_percent / 100.0) * 0.5
    return int(step_ticks * swing_amount)


def apply_timing_jitter(notes: Iterable[Note], jitter_ticks: int, rng: random.Random) -> List[Note]:
    if jitter_ticks <= 0:
        return list(notes)
    out: List[Note] = []
    for n in notes:
        delta = rng.randint(-jitter_ticks, jitter_ticks)
        start = max(0, n.start_tick + delta)
        out.append(
            Note(
                midi_note=n.midi_note,
                velocity=n.velocity,
                start_tick=start,
                duration_ticks=n.duration_ticks,
                channel=n.channel,
            )
        )
    return out

