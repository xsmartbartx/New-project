# MIDI & Drum Pattern Generator

DAW-independent MIDI generator that creates editable patterns for:
- `chords.mid`
- `melody.mid`
- `bass.mid`
- `drums.mid`
- optional `combined.mid` (multitrack)

Outputs are standard MIDI files and import directly into FL Studio, Ableton, Logic, and other DAWs.

## Features

- Genre + mood-aware chord progression templates
- Scale-constrained melody with chord-tone weighting on strong beats
- Bassline generation with syncopation and octave variation
- GM drum mapping (kick/snare/clap/hats/toms)
- Humanization:
  - timing jitter (`--humanize-ms`)
  - velocity variance (`--humanize-velocity`)
  - swing (`--swing`)
- Seed-based reproducibility (`--seed`)

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python generator.py \
  --genre trap \
  --scale minor \
  --key A \
  --bpm 145 \
  --bars 8 \
  --mood dark \
  --complexity 0.7 \
  --swing 18 \
  --humanize-ms 10 \
  --humanize-velocity 14 \
  --seed 42 \
  --combined \
  --output-dir output
```

## Key Arguments

- `--genre`: `hip-hop`, `trap`, `edm`, `house`, `techno`, `pop`, `rock`, `jazz`
- `--scale`: `major`, `minor`, `harmonic_minor`, `dorian`, `mixolydian`
- `--key`: note name like `C`, `C#`, `Db`, `A`, `Bb`
- `--time-signature`: default `4/4`
- `--chord-mode`: `triad`, `7th`, `sus2`, `sus4`
- `--complexity`: `0.0` to `1.0`
- `--swing`: `0` to `100`
- `--humanize-ms`: recommended `5` to `15`
- `--humanize-velocity`: recommended `8` to `20`

## MIDI Drum Notes (GM)

- Kick: `36` (`C1`)
- Snare: `38` (`D1`)
- Clap: `39` (`D#1`)
- Closed Hat: `42` (`F#1`)
- Open Hat: `46` (`A#1`)

## DAW Workflow

1. Run generator.
2. Drag `drums.mid`, `bass.mid`, `chords.mid`, `melody.mid` into DAW tracks.
3. Route each track to your preferred instruments/samplers.

## Notes

- This is an MVP focused on deterministic, editable MIDI output.
- Future extensions: mutation controls, groove extraction, ML probability models, VST plugin port.
