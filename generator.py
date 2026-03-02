#!/usr/bin/env python3
import argparse
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo


PPQ = 480

NOTE_NAME_TO_SEMITONE = {
    "C": 0,
    "C#": 1,
    "Db": 1,
    "D": 2,
    "D#": 3,
    "Eb": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "Gb": 6,
    "G": 7,
    "G#": 8,
    "Ab": 8,
    "A": 9,
    "A#": 10,
    "Bb": 10,
    "B": 11,
}

SCALES = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
}

ROMAN_TO_DEGREE = {
    "i": 1,
    "ii": 2,
    "iii": 3,
    "iv": 4,
    "v": 5,
    "vi": 6,
    "vii": 7,
    "I": 1,
    "II": 2,
    "III": 3,
    "IV": 4,
    "V": 5,
    "VI": 6,
    "VII": 7,
}

PROGRESSION_PRESETS = {
    "trap": {
        "dark": ["i", "VI", "III", "VII"],
        "energetic": ["i", "iv", "VI", "VII"],
        "chill": ["i", "v", "VI", "iv"],
        "aggressive": ["i", "VII", "VI", "VII"],
    },
    "hip-hop": {
        "dark": ["i", "VI", "III", "VII"],
        "energetic": ["i", "iv", "v", "i"],
        "chill": ["i", "iv", "VII", "III"],
        "aggressive": ["i", "ii", "VII", "VI"],
    },
    "edm": {
        "dark": ["i", "VI", "III", "VII"],
        "energetic": ["I", "V", "vi", "IV"],
        "chill": ["I", "vi", "IV", "V"],
        "aggressive": ["i", "VII", "VI", "VII"],
    },
    "house": {
        "dark": ["i", "VII", "VI", "VII"],
        "energetic": ["I", "V", "vi", "IV"],
        "chill": ["I", "iii", "vi", "IV"],
        "aggressive": ["i", "VI", "VII", "i"],
    },
    "techno": {
        "dark": ["i", "VII", "VI", "VII"],
        "energetic": ["i", "iv", "VII", "VI"],
        "chill": ["i", "VI", "iv", "VII"],
        "aggressive": ["i", "VII", "i", "VII"],
    },
    "pop": {
        "dark": ["vi", "IV", "I", "V"],
        "energetic": ["I", "V", "vi", "IV"],
        "chill": ["I", "vi", "IV", "V"],
        "aggressive": ["vi", "IV", "I", "V"],
    },
    "rock": {
        "dark": ["i", "VI", "VII", "i"],
        "energetic": ["I", "V", "vi", "IV"],
        "chill": ["I", "IV", "vi", "V"],
        "aggressive": ["i", "VII", "VI", "V"],
    },
    "jazz": {
        "dark": ["ii", "V", "i", "vi"],
        "energetic": ["ii", "V", "I", "VI"],
        "chill": ["I", "vi", "ii", "V"],
        "aggressive": ["ii", "V", "i", "V"],
    },
}

GM_DRUM_NOTES = {
    "kick": 36,
    "snare": 38,
    "clap": 39,
    "hat_closed": 42,
    "hat_open": 46,
    "tom_low": 45,
    "tom_mid": 47,
    "tom_high": 50,
}


@dataclass
class NoteEvent:
    note: int
    velocity: int
    start: int
    duration: int
    channel: int = 0


def clamp(n: int, low: int, high: int) -> int:
    return max(low, min(high, n))


def ms_to_ticks(ms: float, bpm: int) -> int:
    ticks_per_second = (PPQ * bpm) / 60.0
    return int(round((ms / 1000.0) * ticks_per_second))


def swing_offset_ticks(step_index: int, step_ticks: int, swing_percent: float) -> int:
    if swing_percent <= 0:
        return 0
    if step_index % 2 == 0:
        return 0
    swing_amount = (swing_percent / 100.0) * 0.5
    return int(step_ticks * swing_amount)


def parse_key(key: str) -> int:
    if key not in NOTE_NAME_TO_SEMITONE:
        raise ValueError(f"Unsupported key: {key}")
    return NOTE_NAME_TO_SEMITONE[key]


def scale_notes(key_root: int, scale_name: str) -> List[int]:
    if scale_name not in SCALES:
        raise ValueError(f"Unsupported scale: {scale_name}")
    return [(key_root + interval) % 12 for interval in SCALES[scale_name]]


def degree_to_midi(scale_pc: Sequence[int], degree: int, octave: int) -> int:
    idx = (degree - 1) % 7
    return scale_pc[idx] + (octave + 1) * 12


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


def choose_progression(genre: str, mood: str) -> List[str]:
    genre_map = PROGRESSION_PRESETS.get(genre, PROGRESSION_PRESETS["hip-hop"])
    return genre_map.get(mood, genre_map["chill"])


def build_chords(
    progression: Sequence[str],
    bars: int,
    beats_per_bar: int,
    scale_pc: Sequence[int],
    chord_mode: str,
) -> List[NoteEvent]:
    events: List[NoteEvent] = []
    ticks_bar = beats_per_bar * PPQ
    for bar in range(bars):
        symbol = progression[bar % len(progression)]
        degree = ROMAN_TO_DEGREE[symbol]
        quality = chord_mode
        if symbol in ("V", "VII") and chord_mode == "triad":
            quality = "7th"
        chord_notes = chord_from_degree(scale_pc, degree, quality, octave=4)
        start = bar * ticks_bar
        duration = ticks_bar
        for note in chord_notes:
            events.append(NoteEvent(note=note, velocity=70, start=start, duration=duration))
    return events


def chord_tones_for_bar(
    progression: Sequence[str],
    bar: int,
    scale_pc: Sequence[int],
    chord_mode: str,
) -> List[int]:
    symbol = progression[bar % len(progression)]
    degree = ROMAN_TO_DEGREE[symbol]
    return chord_from_degree(scale_pc, degree, chord_mode, octave=5)


def build_melody(
    progression: Sequence[str],
    bars: int,
    beats_per_bar: int,
    scale_pc: Sequence[int],
    rng: random.Random,
    genre: str,
) -> List[NoteEvent]:
    events: List[NoteEvent] = []
    step_division = 8 if genre in ("jazz", "hip-hop", "trap") else 4
    step_ticks = PPQ // (step_division // 2)
    steps_per_bar = beats_per_bar * (step_division // 2)

    scale_pitch_pool = []
    for octave in (4, 5, 6):
        scale_pitch_pool.extend([(pc + (octave + 1) * 12) for pc in scale_pc])

    for bar in range(bars):
        chord_tones = chord_tones_for_bar(progression, bar, scale_pc, "triad")
        for step in range(steps_per_bar):
            strong = (step % (step_division // 2) == 0)
            play_prob = 0.55 if strong else 0.35
            if rng.random() > play_prob:
                continue
            if strong or rng.random() < 0.7:
                note = rng.choice(chord_tones + [n + 12 for n in chord_tones])
            else:
                note = rng.choice(scale_pitch_pool)
            duration_steps = 1 if rng.random() < 0.8 else 2
            duration = step_ticks * duration_steps
            start = bar * beats_per_bar * PPQ + step * step_ticks
            velocity = rng.randint(62, 102 if strong else 88)
            events.append(NoteEvent(note=clamp(note, 60, 92), velocity=velocity, start=start, duration=duration))
    return events


def build_bass(
    progression: Sequence[str],
    bars: int,
    beats_per_bar: int,
    scale_pc: Sequence[int],
    rng: random.Random,
    genre: str,
) -> List[NoteEvent]:
    events: List[NoteEvent] = []
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
            note = root
            if rng.random() < 0.18:
                note += 12
            if rng.random() < 0.14:
                note -= 5
            note = clamp(note, 28, 60)
            vel = 92 if beat_pos in (0.0, 2.0) else rng.randint(68, 88)
            duration = step_ticks if genre not in ("house", "techno") else int(step_ticks * 0.9)
            start = bar * beats_per_bar * PPQ + step * step_ticks
            events.append(NoteEvent(note=note, velocity=vel, start=start, duration=duration))
    return events


def drum_velocity(base: int, variance: int, accent: bool, rng: random.Random) -> int:
    bump = 10 if accent else 0
    return clamp(base + bump + rng.randint(-variance, variance), 1, 127)


def build_drums(
    bars: int,
    beats_per_bar: int,
    genre: str,
    complexity: float,
    swing: float,
    humanize_ms: float,
    humanize_vel: int,
    rng: random.Random,
) -> List[NoteEvent]:
    events: List[NoteEvent] = []
    step_ticks = PPQ // 4  # 16th notes
    steps_per_bar = beats_per_bar * 4
    total_steps = bars * steps_per_bar

    for idx in range(total_steps):
        bar = idx // steps_per_bar
        step_in_bar = idx % steps_per_bar
        base_start = bar * beats_per_bar * PPQ + step_in_bar * step_ticks
        start = base_start + swing_offset_ticks(step_in_bar, step_ticks, swing)
        start += rng.randint(-ms_to_ticks(humanize_ms, 120), ms_to_ticks(humanize_ms, 120))
        start = max(0, start)

        beat = step_in_bar / 4.0
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
                NoteEvent(
                    note=GM_DRUM_NOTES["kick"],
                    velocity=drum_velocity(95, humanize_vel, accent=on_beat, rng=rng),
                    start=start,
                    duration=int(step_ticks * 0.35),
                    channel=9,
                )
            )

        snare_steps = (4, 12)
        if step_in_bar in snare_steps:
            events.append(
                NoteEvent(
                    note=GM_DRUM_NOTES["snare"],
                    velocity=drum_velocity(100, humanize_vel, accent=True, rng=rng),
                    start=start,
                    duration=int(step_ticks * 0.35),
                    channel=9,
                )
            )
            if rng.random() < (0.25 + complexity * 0.3):
                ghost_start = max(0, start - int(step_ticks * 0.5))
                events.append(
                    NoteEvent(
                        note=GM_DRUM_NOTES["snare"],
                        velocity=drum_velocity(45, humanize_vel, accent=False, rng=rng),
                        start=ghost_start,
                        duration=int(step_ticks * 0.25),
                        channel=9,
                    )
                )

        hat_resolution = 2 if genre in ("house", "techno", "edm") else 1
        if step_in_bar % hat_resolution == 0:
            hat_note = GM_DRUM_NOTES["hat_closed"]
            if genre == "trap" and rng.random() < 0.18:
                hat_note = GM_DRUM_NOTES["hat_open"]
            events.append(
                NoteEvent(
                    note=hat_note,
                    velocity=drum_velocity(70, humanize_vel, accent=on_beat, rng=rng),
                    start=start,
                    duration=int(step_ticks * 0.2),
                    channel=9,
                )
            )

        if genre == "trap" and rng.random() < (0.05 + complexity * 0.15):
            roll_start = start
            roll_sub = step_ticks // 4
            for r in range(3):
                events.append(
                    NoteEvent(
                        note=GM_DRUM_NOTES["hat_closed"],
                        velocity=drum_velocity(58 + r * 4, humanize_vel, accent=False, rng=rng),
                        start=roll_start + r * roll_sub,
                        duration=int(roll_sub * 0.8),
                        channel=9,
                    )
                )
    return events


def write_midi(path: Path, note_events: Sequence[NoteEvent], bpm: int, time_signature: Tuple[int, int], track_name: str) -> None:
    midi = MidiFile(ticks_per_beat=PPQ)
    track = MidiTrack()
    midi.tracks.append(track)
    track.append(MetaMessage("set_tempo", tempo=bpm2tempo(bpm), time=0))
    track.append(MetaMessage("time_signature", numerator=time_signature[0], denominator=time_signature[1], clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
    track.append(MetaMessage("track_name", name=track_name, time=0))

    event_stream = []
    for e in note_events:
        start = max(0, e.start)
        end = max(start + 1, e.start + e.duration)
        event_stream.append((start, True, e))
        event_stream.append((end, False, e))
    event_stream.sort(key=lambda x: (x[0], not x[1]))

    last_time = 0
    for abs_time, is_on, e in event_stream:
        delta = abs_time - last_time
        last_time = abs_time
        if is_on:
            track.append(Message("note_on", note=e.note, velocity=e.velocity, time=delta, channel=e.channel))
        else:
            track.append(Message("note_off", note=e.note, velocity=0, time=delta, channel=e.channel))
    track.append(MetaMessage("end_of_track", time=0))
    midi.save(path)


def write_combined(
    path: Path,
    parts: Dict[str, Sequence[NoteEvent]],
    bpm: int,
    time_signature: Tuple[int, int],
) -> None:
    midi = MidiFile(ticks_per_beat=PPQ)
    tempo_track = MidiTrack()
    midi.tracks.append(tempo_track)
    tempo_track.append(MetaMessage("set_tempo", tempo=bpm2tempo(bpm), time=0))
    tempo_track.append(MetaMessage("time_signature", numerator=time_signature[0], denominator=time_signature[1], clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
    tempo_track.append(MetaMessage("track_name", name="tempo", time=0))
    tempo_track.append(MetaMessage("end_of_track", time=0))

    for name, events in parts.items():
        track = MidiTrack()
        midi.tracks.append(track)
        track.append(MetaMessage("track_name", name=name, time=0))
        event_stream = []
        for e in events:
            start = max(0, e.start)
            end = max(start + 1, e.start + e.duration)
            event_stream.append((start, True, e))
            event_stream.append((end, False, e))
        event_stream.sort(key=lambda x: (x[0], not x[1]))
        last_time = 0
        for abs_time, is_on, e in event_stream:
            delta = abs_time - last_time
            last_time = abs_time
            if is_on:
                track.append(Message("note_on", note=e.note, velocity=e.velocity, time=delta, channel=e.channel))
            else:
                track.append(Message("note_off", note=e.note, velocity=0, time=delta, channel=e.channel))
        track.append(MetaMessage("end_of_track", time=0))
    midi.save(path)


def parse_time_signature(ts: str) -> Tuple[int, int]:
    try:
        num_str, den_str = ts.split("/")
        num = int(num_str)
        den = int(den_str)
        if num <= 0 or den not in (2, 4, 8, 16):
            raise ValueError
        return (num, den)
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
    parser.add_argument("--mood", default="dark", choices=["dark", "energetic", "chill", "aggressive"])
    parser.add_argument("--chord-mode", default="triad", choices=["triad", "7th", "sus2", "sus4"])
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

    rng = random.Random(args.seed)
    ts = parse_time_signature(args.time_signature)
    key_root = parse_key(args.key)
    scale_pc = scale_notes(key_root, args.scale)
    progression = choose_progression(args.genre, args.mood)
    complexity = min(max(args.complexity, 0.0), 1.0)

    chords = build_chords(progression, args.bars, ts[0], scale_pc, args.chord_mode)
    melody = build_melody(progression, args.bars, ts[0], scale_pc, rng, args.genre)
    bass = build_bass(progression, args.bars, ts[0], scale_pc, rng, args.genre)
    drums = build_drums(
        args.bars,
        ts[0],
        args.genre,
        complexity=complexity,
        swing=args.swing,
        humanize_ms=args.humanize_ms,
        humanize_vel=args.humanize_velocity,
        rng=rng,
    )

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_midi(out_dir / "chords.mid", chords, args.bpm, ts, "chords")
    write_midi(out_dir / "melody.mid", melody, args.bpm, ts, "melody")
    write_midi(out_dir / "bass.mid", bass, args.bpm, ts, "bass")
    write_midi(out_dir / "drums.mid", drums, args.bpm, ts, "drums")

    if args.combined:
        write_combined(
            out_dir / "combined.mid",
            {"chords": chords, "melody": melody, "bass": bass, "drums": drums},
            args.bpm,
            ts,
        )

    print(f"Generated MIDI files in: {out_dir.resolve()}")
    print("Files: chords.mid, melody.mid, bass.mid, drums.mid" + (", combined.mid" if args.combined else ""))


if __name__ == "__main__":
    main()
