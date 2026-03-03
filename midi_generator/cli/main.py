from __future__ import annotations

import argparse
from pathlib import Path

from ..config.settings import (
    PROGRESSION_PRESETS,
    SCALES,
    SUPPORTED_CHORD_MODES,
    SUPPORTED_MOODS,
)
from ..core.generator import run
from ..core.types import Preset, TimeSignature


def _parse_time_signature(ts: str) -> TimeSignature:
    try:
        num_str, den_str = ts.split("/")
        num = int(num_str)
        den = int(den_str)
        if num <= 0 or den not in (2, 4, 8, 16):
            raise ValueError
        return TimeSignature(numerator=num, denominator=den)
    except Exception as exc:
        raise ValueError(f"Invalid time signature: {ts}") from exc


def main() -> None:
    parser = argparse.ArgumentParser(description="DAW-independent MIDI and drum pattern generator")
    parser.add_argument("--genre", default="trap", choices=sorted(PROGRESSION_PRESETS.keys()))
    parser.add_argument("--scale", default="minor", choices=sorted(SCALES.keys()))
    parser.add_argument("--key", default="A")
    parser.add_argument("--bpm", type=int, default=140)
    parser.add_argument("--bars", type=int, default=8)
    parser.add_argument("--time-signature", default="4/4")
    parser.add_argument("--mood", default="dark", choices=SUPPORTED_MOODS)
    parser.add_argument("--chord-mode", default="triad", choices=SUPPORTED_CHORD_MODES)
    parser.add_argument("--complexity", type=float, default=0.5, help="0.0-1.0")
    parser.add_argument("--swing", type=float, default=0.0, help="0-100")
    parser.add_argument("--humanize-ms", type=float, default=8.0)
    parser.add_argument("--humanize-velocity", type=int, default=12)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--output-dir", default="output")
    parser.add_argument("--combined", action="store_true", help="also write combined multitrack MIDI")

    args = parser.parse_args()
    if args.bars <= 0:
        raise ValueError("--bars must be > 0")
    if args.bpm < 40 or args.bpm > 240:
        raise ValueError("--bpm must be between 40 and 240")

    preset = Preset(
        genre=args.genre,
        scale=args.scale,
        key=args.key,
        bpm=args.bpm,
        bars=args.bars,
        time_signature=_parse_time_signature(args.time_signature),
        mood=args.mood,
        chord_mode=args.chord_mode,
        complexity=float(args.complexity),
        swing=float(args.swing),
        humanize_ms=float(args.humanize_ms),
        humanize_velocity=int(args.humanize_velocity),
        seed=int(args.seed),
        output_dir=Path(args.output_dir),
        combined=bool(args.combined),
    )

    out_dir = run(preset)

    print(f"Generated MIDI files in: {out_dir.resolve()}")
    print("Files: chords.mid, melody.mid, bass.mid, drums.mid" + (", combined.mid" if preset.combined else ""))


__all__ = ["main"]

