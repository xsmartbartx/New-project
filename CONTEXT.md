## MIDI & Drum Pattern Generator (DAW-Independent)

Automatically generate musical, editable MIDI patterns (melody, chords, bass) and drum grooves with realistic, dDrum-style humanization. All output is DAW-agnostic and ready to use in any modern workflow.

---

### Goals

- **Automatic generation**: Melody, chords, bass, and drum patterns.
- **DAW independence**: Works with any DAW that supports `.mid` files.
- **Realistic groove**: Timing and velocity humanization inspired by dDrum.
- **Musical controls**: Users think in musical terms (genre, mood, key), not low-level parameters.

---

## Output

- **MIDI files**
  - `drums.mid`
  - `bass.mid`
  - `chords.mid`
  - `melody.mid`
- **Combined multitrack MIDI** (optional)
- **DAW compatibility**
  - Fully compatible with:
    - FL Studio (Piano Roll, Channel Rack)
    - Ableton Live (Drum Rack, MIDI tracks)
    - Logic Pro
    - Any other DAW that supports `.mid`

---

## Core Architecture

### 1. Input Parameters (User Control Layer)

High-level, musical parameters that define intent.

#### Musical Parameters

- **Genre**: Hip-Hop, Trap, EDM, House, Techno, Pop, Rock, Jazz
- **Scale**: Major, Natural Minor, Harmonic Minor, Dorian, etc.
- **Key**: C–B
- **Tempo**: BPM (user-defined)
- **Time Signature**: Default 4/4 (extensible)
- **Mood**: Dark, Energetic, Chill, Aggressive

#### Drum Parameters

- **Groove complexity**: Simple → Polyrhythmic
- **Swing**: Percentage-based (MPC-style feel)
- **Humanization**:
  - Timing variance
  - Velocity variance
- **Drum kit type**:
  - Acoustic
  - dDrum / Hybrid
  - 808 / 909
  - Experimental

---

### 2. Generation Engine (Logic Layer)

#### A. MIDI Music Generator

##### 1) Chord Generator

- **Scale-aware chord construction**
- Supports:
  - Triads
  - 7th chords
  - Suspended chords
  - Passing chords and substitutions
- **Example**  
  - Key: A Minor  
  - Progression: i – VI – III – VII  
  - Output: Am → F → C → G

##### 2) Melody Generator

- Notes constrained to the selected scale.
- **Weighted randomness**:
  - Strong beats → chord tones
  - Weak beats → passing/neighbor tones
- **Phrase structure**:
  - Supports 4, 8, and 16-bar phrases.
  - Can generate call-and-response patterns and motifs.

##### 3) Bass Generator

- Root-following as the base behavior.
- Variants:
  - Octave jumps
  - Approach notes
  - Syncopated figures
- **Rhythm design**:
  - Genre-aware patterns
  - Sidechain-friendly rhythms for EDM/Trap styles.

---

#### B. Drum Generator (dDrum-Style)

##### MIDI Mapping (GM-Compatible)

- **Kick**: C1 (36)  
- **Snare**: D1 (38)  
- **Clap**: D#1  
- **Hi-Hat Closed**: F#1  
- **Hi-Hat Open**: A#1  
- **Toms**: Vary by kit

Tested for compatibility with:

- FL Studio
- Ableton Live
- Logic Pro
- Any GM-style drum mapping

##### Groove Logic

- **Kick**
  - Downbeats emphasized
  - Genre-dependent syncopation rules
- **Snare**
  - Backbeat on 2 and 4
  - Optional ghost notes with reduced velocity
- **Hi-Hats**
  - Rhythmic resolution from 1/8 to 1/32
  - Velocity shaping for natural dynamics
  - Optional rolls, stutters, and triplets (important for Trap and modern Hip-Hop)
- **Additional percussion** (optional)
  - Shakers, rims, tom fills, and FX layers

---

### 3. Humanization Engine

Critical for achieving a dDrum-like, non-mechanical feel.

- **Timing offset**
  - Randomized within a musical range, e.g. ±5–15 ms
  - Weighted by beat strength (strong beats stay tighter)
- **Velocity variance**
  - ±8–20 around the base velocity
  - Genre- and instrument-aware (e.g., hats vary more than kicks)
- **Accent probability**
  - Higher on strong beats or key syncopation points
  - Tunable per genre and groove complexity
- **Result**
  - Avoids "grid-perfect" or "Excel spreadsheet" grooves.
  - Produces a natural, human-like feel out of the box.

---

## Output System

### MIDI Export

- **Per-part files**:
  - `drums.mid`
  - `bass.mid`
  - `chords.mid`
  - `melody.mid`
- **Combined multitrack**:
  - Single `.mid` file containing multiple channels for easy DAW import.

### DAW Integration Examples

- **FL Studio**
  - Drag `drums.mid` to Channel Rack or Piano Roll.
  - Assign drum generator output to FPC or any dDrum-style kit.
  - Drag `bass.mid`, `chords.mid`, and `melody.mid` to instrument channels (e.g., 3xOsc, Harmor, Serum).
- **Ableton Live**
  - Drop `drums.mid` on a MIDI track with Drum Rack.
  - Drop `bass.mid`, `chords.mid`, and `melody.mid` on instrument tracks.
- **Logic Pro**
  - Import MIDI regions directly into the Arrange view and assign software instruments.

---

## Tech Stack Options

### Option A: Desktop App (Recommended)

- **Language**: Python
- **Core libraries**:
  - `music21` – music theory, scales, chord building, analysis
  - `mido` or `pretty_midi` – MIDI creation and export
- **UI frameworks**:
  - PySide / PyQt for native desktop UI  
  - Electron bridge (if a web-like UI is preferred)

### Option B: VST / Plugin (Advanced)

- **Framework**: JUCE (C++)
- **Features**:
  - Real-time MIDI generation
  - Runs as a plugin inside the DAW
  - Live parameter automation (genre, mood, complexity, etc.)

### Option C: Web Generator (MVP-Friendly)

- **Technology**:
  - Web MIDI API (where supported)
  - Client-side MIDI file export
- **Use case**:
  - Quick idea generation
  - Browser-based preview
  - MIDI download and manual import into any DAW

---

## Advanced / Future Features

- **Pattern mutation**:
  - “Mutate” button to generate variations while preserving core groove or harmony.
- **Groove learning**:
  - Extract timing and velocity profiles from reference MIDI.
  - Apply learned groove to newly generated patterns.
- **Genre-trained probability models**:
  - Statistical or ML models trained on genre-specific MIDI datasets.
- **Preset packs**:
  - FL Studio and other-DAW-specific presets for immediate plug-and-play.
- **Seed-based reproducibility**:
  - Random seed parameter for repeatable pattern generation.
- **AI extension**:
  - Integration with transformer-based MIDI models for advanced, style-aware generation.

---

## Example FL Studio Workflow

1. Generate a MIDI pack from the app using your chosen genre, key, and mood.
2. Drag `drums.mid` into the Channel Rack or a Piano Roll.
3. Load an FPC or dDrum-style kit on that channel.
4. Drag `bass.mid` onto an instrument (e.g., 3xOsc or a bass VST).
5. Drag `chords.mid` and `melody.mid` onto synth or piano instruments.
6. Tweak groove parameters (swing, humanization, complexity) and regenerate as needed.

---

## Implementation Roadmap (Step-by-Step)

High-level sequence for building the app, focusing on one task at a time.

1. **Refactor into a package skeleton**
   - Create `midi_generator/` package with `core`, `theory`, `instruments`, `humanization`, `midi`, `db`, and `cli` submodules.
   - Move minimal orchestration logic from `generator.py` into `midi_generator/cli/main.py`, keeping `generator.py` as a thin entrypoint.

2. **Define shared types and configuration**
   - Add `midi_generator/core/types.py` with dataclasses for `Note`, `Pattern`, `Preset`, and `GenerationRequest`.
   - Add `midi_generator/config/settings.py` for constants (PPQ, default BPM, supported genres/scales/moods, GM mappings).

3. **Implement theory layer**
   - Implement `scales.py`, `chords.py`, and `progressions.py` to encapsulate all scale and chord logic, plus genre/mood-based progression templates.

4. **Implement instrument generators**
   - Implement `chords.py`, `melody.py`, `bass.py`, and `drums.py` in `midi_generator/instruments/` using the theory layer and types.
   - Ensure each instrument generator consumes a `Preset` + RNG seed and emits `Pattern` objects.

5. **Implement humanization and groove layer**
   - Implement `timing.py`, `velocity.py`, and `groove_templates.py` in `midi_generator/humanization/`.
   - Apply timing jitter, velocity variance, swing, and optional groove templates to `Pattern` objects.

6. **Implement MIDI mapping and writer**
   - Implement `midi_generator/midi/mapping.py` for GM mappings and drum note constants.
   - Implement `midi_generator/midi/writer.py` using `mido` or `pretty_midi` to export individual and combined `.mid` files from `Pattern` objects.

7. **Add persistence layer**
   - Implement `midi_generator/db/schema.sql` from the database schema above.
   - Implement `midi_generator/db/models.py` for basic CRUD on presets, generations, patterns, notes, and grooves.

8. **Wire everything in the core generator**
   - Implement `midi_generator/core/generator.py` to coordinate: parse preset → generate patterns → humanize → write MIDI → persist metadata.
   - Update `cli/main.py` to translate CLI args into a `Preset` and call the core generator.

9. **Testing and validation**
   - Add unit tests in `tests/` for theory, instruments, humanization, and MIDI export.
   - Add an end-to-end test that runs the CLI and asserts that valid `.mid` files are created.

10. **Optional UI / advanced features**
    - Add desktop or web UI on top of the CLI.
    - Implement groove extraction from reference MIDI and pattern mutation controls.

---

## Database Schema

Relational schema designed for PostgreSQL (or SQLite for local use). Focus is on reproducible generations, presets, and detailed note-level storage.

### Entities

- **users** (optional for local, required for multi-user setups)
  - `id` (PK, UUID)
  - `email` (unique, nullable for offline use)
  - `display_name`
  - `created_at`
  - `updated_at`

- **presets**
  - `id` (PK, UUID)
  - `user_id` (FK → users.id, nullable)
  - `name`
  - `description`
  - `genre` (enum: hip_hop, trap, edm, house, techno, pop, rock, jazz, other)
  - `scale` (enum or text: major, minor, harmonic_minor, dorian, etc.)
  - `key` (text: C, C#, Db, A, Bb, etc.)
  - `bpm` (integer)
  - `time_signature_numerator` (integer, default 4)
  - `time_signature_denominator` (integer, default 4)
  - `mood` (enum: dark, energetic, chill, aggressive, neutral)
  - `bars` (integer)
  - `complexity` (float 0.0–1.0)
  - `swing` (float 0–100)
  - `humanize_ms` (integer)
  - `humanize_velocity` (integer)
  - `drum_kit_type` (enum: acoustic, ddrum_hybrid, _808, _909, experimental)
  - `chord_mode` (enum: triad, seventh, sus2, sus4, extended)
  - `seed` (bigint, nullable; when set, generation is reproducible)
  - `created_at`
  - `updated_at`

- **generations**
  - `id` (PK, UUID)
  - `user_id` (FK → users.id, nullable)
  - `preset_id` (FK → presets.id)
  - `status` (enum: success, failed, partial)
  - `engine_version` (text; identifies generator algorithm version)
  - `requested_at`
  - `completed_at`
  - `error_message` (nullable)
  - `output_dir` (filesystem path or URI to exported .mid files)

- **patterns**
  - `id` (PK, UUID)
  - `generation_id` (FK → generations.id)
  - `type` (enum: drums, bass, chords, melody, combined)
  - `name` (e.g., "drums_01", "chords_alt")
  - `bpm` (integer)
  - `time_signature_numerator` (integer)
  - `time_signature_denominator` (integer)
  - `bars` (integer)
  - `midi_channel` (integer, nullable for drums where channel is implicit)
  - `is_active` (boolean, default true)
  - `created_at`
  - `updated_at`

- **notes**
  - `id` (PK, UUID)
  - `pattern_id` (FK → patterns.id)
  - `track_index` (integer, for multi-track combined patterns; 0 for single-track)
  - `bar` (integer, 1-based)
  - `beat` (float; or store `tick` as integer instead of bar/beat)
  - `tick` (integer, relative to pattern start, in PPQ units)
  - `duration_ticks` (integer)
  - `midi_note` (integer 0–127)
  - `velocity` (integer 1–127)
  - `channel` (integer 0–15)
  - `humanize_offset_ms` (integer, positive/negative)
  - `is_accent` (boolean)
  - `is_ghost` (boolean)

- **grooves**
  - `id` (PK, UUID)
  - `user_id` (FK → users.id, nullable)
  - `name`
  - `source_type` (enum: built_in, extracted)
  - `source_midi_path` (nullable; path/URI of reference MIDI if extracted)
  - `ppq` (integer; pulses per quarter note used in template)
  - `instrument_scope` (enum: drums, hats_only, full_mix)
  - `created_at`
  - `updated_at`

- **groove_steps**
  - `id` (PK, UUID)
  - `groove_id` (FK → grooves.id)
  - `step_index` (integer; index in a single-bar template grid)
  - `expected_tick` (integer; perfect grid position)
  - `offset_ticks` (integer; deviation from grid)
  - `velocity_scale` (float; multiplier applied to base velocity)
  - `accent_weight` (float; probability/weight for accent at this step)

### Notes on Storage Strategy

- For local-only CLI use, serialize presets as JSON and use SQLite with the above tables.
- For a future desktop or web app, move to PostgreSQL and keep the same schema.
- Generations can be fully reconstructed from `presets` + `seed` + `engine_version`, but storing `notes` makes debugging and groove-learning much easier.

---

## Application Folder Structure

Target structure for evolving the current single-file `generator.py` into a maintainable Python package.

```text
.
├── generator.py          # Thin CLI entrypoint (backwards compatible)
├── requirements.txt
├── README.md
├── CONTEXT.md
├── midi_generator/       # Main application package
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py        # Defaults, paths, DB config, constants
│   ├── core/
│   │   ├── __init__.py
│   │   ├── types.py           # Dataclasses / typed models for notes, patterns, presets
│   │   ├── generator.py       # High-level orchestration of full pattern generation
│   │   └── random_utils.py    # Seed handling, RNG helpers
│   ├── theory/
│   │   ├── __init__.py
│   │   ├── scales.py          # Scale definitions and helpers
│   │   ├── chords.py          # Chord building, voicing
│   │   └── progressions.py    # Progression templates per genre/mood
│   ├── instruments/
│   │   ├── __init__.py
│   │   ├── chords.py          # Chord track generation
│   │   ├── melody.py          # Melody generation logic
│   │   ├── bass.py            # Bassline generation logic
│   │   └── drums.py           # Kick/snare/hat/polyrhythm generation
│   ├── humanization/
│   │   ├── __init__.py
│   │   ├── timing.py          # Timing jitter and swing application
│   │   ├── velocity.py        # Velocity variance and accents
│   │   └── groove_templates.py# Groove extraction and template application
│   ├── midi/
│   │   ├── __init__.py
│   │   ├── mapping.py         # GM drum mapping and note constants
│   │   └── writer.py          # mido/pretty_midi wrappers for writing .mid
│   ├── db/
│   │   ├── __init__.py
│   │   ├── schema.sql         # SQL for creating the tables above
│   │   ├── models.py          # Thin ORM/DAO layer for presets, generations, notes
│   │   └── migrations/        # Future DB migrations
│   └── cli/
│       ├── __init__.py
│       └── main.py            # Argument parsing and CLI command wiring
└── tests/
    ├── __init__.py
    ├── test_theory.py
    ├── test_instruments.py
    ├── test_humanization.py
    ├── test_midi_writer.py
    └── test_end_to_end.py     # Ensures CLI call produces valid .mid files
```

Design notes:

- `generator.py` at the project root remains as the entrypoint used in the README, importing `midi_generator.cli.main`.
- `midi_generator/core` coordinates calls to the theory, instruments, humanization, and MIDI layers.
- `midi_generator/db` encapsulates all persistence concerns so that the CLI and generators remain database-agnostic.
- `tests/` mirrors the package structure to keep unit and integration tests organized.
