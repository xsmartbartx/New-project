from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Sequence

PatternType = Literal["drums", "bass", "chords", "melody", "combined"]
Mood = Literal["dark", "energetic", "chill", "aggressive"]


@dataclass(frozen=True)
class TimeSignature:
    numerator: int = 4
    denominator: int = 4


@dataclass(frozen=True)
class Note:
    midi_note: int
    velocity: int
    start_tick: int
    duration_ticks: int
    channel: int = 0


@dataclass(frozen=True)
class Preset:
    genre: str = "trap"
    scale: str = "minor"
    key: str = "A"
    bpm: int = 140
    bars: int = 8
    time_signature: TimeSignature = field(default_factory=TimeSignature)
    mood: Mood = "dark"
    chord_mode: str = "triad"
    complexity: float = 0.5
    swing: float = 0.0
    humanize_ms: float = 8.0
    humanize_velocity: int = 12
    seed: int = 7
    output_dir: Path = Path("output")
    combined: bool = False


@dataclass(frozen=True)
class Pattern:
    type: PatternType
    name: str
    bpm: int
    time_signature: TimeSignature
    ppq: int
    notes: Sequence[Note]

