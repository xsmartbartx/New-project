from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo

from ..config.settings import PPQ
from ..core.types import Note, TimeSignature


def _event_stream(note_events: Iterable[Note]) -> List[Tuple[int, bool, Note]]:
    stream: List[Tuple[int, bool, Note]] = []
    for e in note_events:
        start = max(0, e.start_tick)
        end = max(start + 1, e.start_tick + e.duration_ticks)
        stream.append((start, True, e))
        stream.append((end, False, e))
    stream.sort(key=lambda x: (x[0], not x[1]))
    return stream


def write_midi(path: Path, note_events: Sequence[Note], bpm: int, time_signature: TimeSignature, track_name: str) -> None:
    midi = MidiFile(ticks_per_beat=PPQ)
    track = MidiTrack()
    midi.tracks.append(track)
    track.append(MetaMessage("set_tempo", tempo=bpm2tempo(bpm), time=0))
    track.append(
        MetaMessage(
            "time_signature",
            numerator=time_signature.numerator,
            denominator=time_signature.denominator,
            clocks_per_click=24,
            notated_32nd_notes_per_beat=8,
            time=0,
        )
    )
    track.append(MetaMessage("track_name", name=track_name, time=0))

    last_time = 0
    for abs_time, is_on, e in _event_stream(note_events):
        delta = abs_time - last_time
        last_time = abs_time
        if is_on:
            track.append(Message("note_on", note=e.midi_note, velocity=e.velocity, time=delta, channel=e.channel))
        else:
            track.append(Message("note_off", note=e.midi_note, velocity=0, time=delta, channel=e.channel))

    track.append(MetaMessage("end_of_track", time=0))
    midi.save(path)


def write_combined(
    path: Path,
    parts: Dict[str, Sequence[Note]],
    bpm: int,
    time_signature: TimeSignature,
) -> None:
    midi = MidiFile(ticks_per_beat=PPQ)
    tempo_track = MidiTrack()
    midi.tracks.append(tempo_track)
    tempo_track.append(MetaMessage("set_tempo", tempo=bpm2tempo(bpm), time=0))
    tempo_track.append(
        MetaMessage(
            "time_signature",
            numerator=time_signature.numerator,
            denominator=time_signature.denominator,
            clocks_per_click=24,
            notated_32nd_notes_per_beat=8,
            time=0,
        )
    )
    tempo_track.append(MetaMessage("track_name", name="tempo", time=0))
    tempo_track.append(MetaMessage("end_of_track", time=0))

    for name, events in parts.items():
        track = MidiTrack()
        midi.tracks.append(track)
        track.append(MetaMessage("track_name", name=name, time=0))

        last_time = 0
        for abs_time, is_on, e in _event_stream(events):
            delta = abs_time - last_time
            last_time = abs_time
            if is_on:
                track.append(Message("note_on", note=e.midi_note, velocity=e.velocity, time=delta, channel=e.channel))
            else:
                track.append(Message("note_off", note=e.midi_note, velocity=0, time=delta, channel=e.channel))

        track.append(MetaMessage("end_of_track", time=0))

    midi.save(path)

