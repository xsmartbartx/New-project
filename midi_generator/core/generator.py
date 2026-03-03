from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Dict, List

from ..config.settings import PPQ
from ..core.random_utils import make_rng
from ..core.types import Note, Preset
from ..midi.writer import write_combined, write_midi
from ..theory.progressions import choose_progression
from ..theory.scales import parse_key, scale_pitch_classes
from ..instruments import bass as bass_gen
from ..instruments import chords as chords_gen
from ..instruments import drums as drums_gen
from ..instruments import melody as melody_gen

ENGINE_VERSION = "core-v1"


def generate_patterns(preset: Preset) -> Dict[str, List[Note]]:
    rng = make_rng(preset.seed)

    ts = preset.time_signature
    key_root = parse_key(preset.key)
    scale_pc = scale_pitch_classes(key_root, preset.scale)
    progression = choose_progression(preset.genre, preset.mood)

    chords = chords_gen.generate(preset, progression, scale_pc)
    melody = melody_gen.generate(preset, progression, scale_pc, rng)
    bass = bass_gen.generate(preset, progression, scale_pc, rng)
    drums = drums_gen.generate(preset, rng)

    return {"chords": chords, "melody": melody, "bass": bass, "drums": drums}


def write_outputs(preset: Preset, parts: Dict[str, List[Note]]) -> Path:
    out_dir = Path(preset.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    write_midi(out_dir / "chords.mid", parts["chords"], preset.bpm, preset.time_signature, "chords")
    write_midi(out_dir / "melody.mid", parts["melody"], preset.bpm, preset.time_signature, "melody")
    write_midi(out_dir / "bass.mid", parts["bass"], preset.bpm, preset.time_signature, "bass")
    write_midi(out_dir / "drums.mid", parts["drums"], preset.bpm, preset.time_signature, "drums")

    if preset.combined:
        write_combined(out_dir / "combined.mid", parts, preset.bpm, preset.time_signature)

    return out_dir


def run(preset: Preset) -> Path:
    parts = generate_patterns(preset)
    return write_outputs(preset, parts)

