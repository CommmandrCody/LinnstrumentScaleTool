"""
Scale definitions for Linnstrument Scale Tool
Defines common musical scales and modes with their interval patterns
"""

# Scale intervals are defined in semitones from the root note
SCALES = {
    # Major scales and modes
    'major': [0, 2, 4, 5, 7, 9, 11],
    'ionian': [0, 2, 4, 5, 7, 9, 11],  # Same as major
    'dorian': [0, 2, 3, 5, 7, 9, 10],
    'phrygian': [0, 1, 3, 5, 7, 8, 10],
    'lydian': [0, 2, 4, 6, 7, 9, 11],
    'mixolydian': [0, 2, 4, 5, 7, 9, 10],
    'aeolian': [0, 2, 3, 5, 7, 8, 10],  # Natural minor
    'locrian': [0, 1, 3, 5, 6, 8, 10],

    # Minor scales
    'minor': [0, 2, 3, 5, 7, 8, 10],  # Natural minor
    'harmonic_minor': [0, 2, 3, 5, 7, 8, 11],
    'melodic_minor': [0, 2, 3, 5, 7, 9, 11],

    # Pentatonic scales
    'major_pentatonic': [0, 2, 4, 7, 9],
    'minor_pentatonic': [0, 3, 5, 7, 10],

    # Blues
    'blues': [0, 3, 5, 6, 7, 10],

    # Other common scales
    'whole_tone': [0, 2, 4, 6, 8, 10],
    'chromatic': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'diminished': [0, 2, 3, 5, 6, 8, 9, 11],  # Half-whole
    'augmented': [0, 3, 4, 7, 8, 11],

    # Jazz/Advanced
    'bebop_major': [0, 2, 4, 5, 7, 8, 9, 11],
    'bebop_minor': [0, 2, 3, 5, 7, 8, 9, 10],
    'altered': [0, 1, 3, 4, 6, 8, 10],  # Super Locrian

    # Exotic scales
    'harmonic_major': [0, 2, 4, 5, 7, 8, 11],
    'double_harmonic': [0, 1, 4, 5, 7, 8, 11],  # Byzantine
    'hungarian_minor': [0, 2, 3, 6, 7, 8, 11],
    'japanese': [0, 1, 5, 7, 8],
    'spanish': [0, 1, 4, 5, 7, 8, 10],  # Phrygian dominant
}

# Note names
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTE_NAMES_FLAT = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

def get_scale_notes(root_note, scale_name):
    """
    Get all notes in a scale across all octaves (0-127 MIDI note range)

    Args:
        root_note: MIDI note number (0-11) or note name ('C', 'D', etc.)
        scale_name: Name of the scale from SCALES dict

    Returns:
        List of MIDI note numbers that are in the scale
    """
    if isinstance(root_note, str):
        root_note = note_name_to_number(root_note)

    if scale_name not in SCALES:
        raise ValueError(f"Unknown scale: {scale_name}. Available scales: {list(SCALES.keys())}")

    intervals = SCALES[scale_name]
    scale_notes = []

    # Generate notes across all octaves
    for octave in range(-1, 11):  # MIDI notes 0-127
        for interval in intervals:
            note = root_note + (octave * 12) + interval
            if 0 <= note <= 127:
                scale_notes.append(note)

    return sorted(scale_notes)

def note_name_to_number(note_name):
    """
    Convert note name to MIDI note number (within one octave, 0-11)

    Args:
        note_name: Note name like 'C', 'C#', 'Db', etc.

    Returns:
        MIDI note number 0-11
    """
    note_name = note_name.upper()

    if note_name in NOTE_NAMES:
        return NOTE_NAMES.index(note_name)
    elif note_name in NOTE_NAMES_FLAT:
        return NOTE_NAMES_FLAT.index(note_name)
    else:
        raise ValueError(f"Unknown note name: {note_name}")

def note_number_to_name(note_number, use_flats=False):
    """
    Convert MIDI note number to note name

    Args:
        note_number: MIDI note number
        use_flats: Use flat notation instead of sharps

    Returns:
        Note name with octave (e.g., 'C4', 'F#3')
    """
    octave = (note_number // 12) - 1
    note = note_number % 12

    names = NOTE_NAMES_FLAT if use_flats else NOTE_NAMES
    return f"{names[note]}{octave}"

def get_available_scales():
    """Return list of all available scale names"""
    return sorted(SCALES.keys())
