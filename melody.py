import random
from time import sleep
import a440
from pyo import *
import components
import definitions

#  --- MELODY MACHINE, v 0.1.1  ---
# Written by Hayden Stilley, December 2022
# (requires an install of pyo, a software synthesizer for Python.)
# SUMMARY: This is an engine that, given a sequence of chords and a
# key, pseudo-randomly produces pitch values (in Hz) that, when strung
# together, act as a melody over the chord progression. There are
# limitations currently - see below.
#
# LIMITATION: There is virtually no rhythm functionality as of yet.
# To compensate, only 60% of the notes generated are actually heard.
#
# LIMITATION: The engine has little capability to create musical
# phrases, as it does not reference previously played pitches while
# picking a new pitch, and has no system for remembering motifs.
# A Markov-based generation system may be helpful.
#
# LIMITATION: Only works within one octave.
#
# LIMITATION: Chords are confined to 3 notes, for now.
#
# TODO: components.ChordSequence() constructor method for roman numerals

def rand2d6():
    """ Randomizer emulating a roll of two six-sided dice """
    return (random.randint(1, 6) + random.randint(1, 6))

def get_hz(rootNote, interval):
    """ Calculates Hz value of note for synthesizer """
    return round(rootNote * (2 ** (interval / 12)), 2)

def play_note(note):
    """ Sound source """
    return Sine(freq=note).out()

def set_tables(Chord, current_note, scale_steps):
    """ Establishes three tables of notes to choose from """
    if Chord.diatonic == False:
        return [components.NoteTable(Chord.notes, 'chord')]
    else:
        return [
            components.NoteTable(Chord.notes, 'chord'),
            components.AdjacentTable(scale_steps, current_note),
            components.NoteTable(scale_steps, 'scale')
        ]

def table_select(tables):
    """
    Chooses which table to choose from, based on a simulated 2d6
    dice roll interpreted by definitions.metatable
    """
    for i in tables:
        if i.is_active == False:
            tables.remove(i)
    if len(tables) == 3:
        out = tables[definitions.metaTable[rand2d6()]]
        return out
    else:
        out = random.choice(tables)
        return out

def pitch_select(Table):
    """ Chooses pitch from table """
    return random.choice(Table.notes)

def play(meter, tonic, key, chord_progression, starting_note):
    """ Perform entire music loop """
    current_note = starting_note
    for bar in range(meter.bars):
        for measure in range(1, (meter.measures+1)):
            for beat in range(meter.beats):
                note_tables = set_tables(
                    chord_progression.chords[measure-1],
                    current_note,
                    key.steps
                )
                current_note = pitch_select(table_select(note_tables))

                if (random.randint(1, 100) < 60):
                    player = play_note(get_hz(tonic.hz, current_note))

                sleep(meter.beat_duration)

if __name__ == "__main__":
    """ Set up music environment """
    tonic = components.Tonic('A', 440.00)
    key = components.Scale(definitions.scales['minor'])
    chord_progression = components.ChordSequence(key.steps, [1, 4, 1, 5], [[3,'major']])
    meter = components.Meter(8, 4, 4)

    """ Set up music player """
    synth = Server().boot().start()

    """ Starts the music """
    play(meter, tonic, key, chord_progression, 0)

    """ Closes synthesizer server """
    synth.stop()