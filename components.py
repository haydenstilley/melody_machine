import definitions

class Tonic(object):
    def __init__(self, name, hz):
        self.name = name
        self.hz = hz
        self.interval = 0

class Chord(object):
    def __init__(self, root_interval, intervals, scale):
        self.root_interval = root_interval
        self.root_note = scale[(self.root_interval)]
        self.intervals = intervals
        self.diatonic = True
        self.notes = []
        for i in intervals:
            self.notes.append(scale[i])

    def octave_adjust(self):
        for i in range(len(self.notes)):
            if self.notes[i] > 11:
                self.notes[i] -= 12

    def make_major(self):
        self.notes = [self.root_note, self.root_note + 4, self.root_note + 7]
        self.diatonic = False
        self.octave_adjust()

    def make_minor(self):
        self.notes = [self.root_note, self.root_note + 3, self.root_note + 7]
        self.diatonic = False
        self.octave_adjust()

    def make_diminished(self):
        self.notes = [self.root_note, self.root_note + 3, self.root_note + 6]
        self.diatonic = False
        self.octave_adjust()

    def make_augmented(self):
        self.notes = [self.root_note, self.root_note + 4, self.root_note + 8]
        self.octave_adjust()

    chord_mod = {
        'major' : make_major,
        'minor' : make_minor,
        'diminished' : make_diminished,
        'augmented' : make_augmented
    }

class ChordSequence(object):
    def __init__(self, scale, scale_degrees, modifications=None):
        self.scale = scale
        self.scale_degrees = scale_degrees
        self.chords = []
        for i in scale_degrees:
            self.chords.append(Chord(
                (i-1),
                definitions.diatonic_chords[i],
                scale))
        if modifications != None:
            for i in modifications:
                self.chords[i[0]].chord_mod[i[1]](self.chords[i[0]])

class Meter(object):
    def __init__(self, beats, measures, bars, beat_duration=0.3):
        self.beats = beats
        self.measures = measures
        self.bars = bars
        self.beat_duration = beat_duration

class Scale(object):
    def __init__(self, steps):
        self.steps = steps

class NoteTable(object):
    def __init__(self, notes, label):
        self.notes = notes
        self.label = label
        self.is_active = True

class AdjacentTable(NoteTable):
    def __init__(self, notes, current_note = 1):
        super().__init__(notes, label = 'adjacent')
        self.is_active = False
        for i in range(len(notes)):
            if notes[i] == current_note:
                self.note_array = []
                if current_note != 0:
                    self.note_array.append(notes[i - 1])
                if current_note < len(notes):
                    self.note_array.append(notes[i + 1])
                self.notes = self.note_array
                self.is_active = True