from __future__ import annotations

PPQ: int = 480

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

SUPPORTED_GENRES = ["hip-hop", "trap", "edm", "house", "techno", "pop", "rock", "jazz"]
SUPPORTED_MOODS = ["dark", "energetic", "chill", "aggressive"]
SUPPORTED_CHORD_MODES = ["triad", "7th", "sus2", "sus4"]

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

