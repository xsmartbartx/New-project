from __future__ import annotations

import random
from typing import Iterable, List

from ..core.types import Note
from ..core.utils import clamp


def apply_velocity_variance(notes: Iterable[Note], variance: int, rng: random.Random) -> List[Note]:
    if variance <= 0:
        return list(notes)
    out: List[Note] = []
    for n in notes:
        vel = clamp(n.velocity + rng.randint(-variance, variance), 1, 127)
        out.append(
            Note(
                midi_note=n.midi_note,
                velocity=vel,
                start_tick=n.start_tick,
                duration_ticks=n.duration_ticks,
                channel=n.channel,
            )
        )
    return out

