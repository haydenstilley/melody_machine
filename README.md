# melody_machine
An RNG-based system that, given a set of musical chords and a diatonic key, will produce "improvised" melodies that harmonize with the piece. All pitches are represented by their values in Hz, rounded to the hundredth place. Pyo must be installed for sound synthesis to function.

The necessary arguments for the main() function are 1) [key], and 2) [sequence], further defined below.
  1)  [key] is an array created by the function melody.key(). The first entry in the array is itself a seven-item array denoting the pitches in a one-octave diatonic scale. The second entry in the array is another array denoting each chord in a chord progression as a three-item array, with each entry being a value in Hz corresponding to a pitch within the chord.
    * A couple defaults are included in the script, namely melody.keyC and melody.keyCminor.
  2)  [sequence] is an array listing the musical piece's [meter], number of [bars], [chord progression], and [tempo], in that order. The first entry, [meter], is an integer denoting the number of beats in one measure. [bars] is an integer denoting the number of loops through the chord progression the musical piece lasts before it ends. [chord progression] is the same array as the second item in [key]. [tempo] is a value in seconds corresponding to the length of each beat.
    * A couple defaults are included in the script, namely melody.seqC and melody.seqCminor.

  The system is powered by an array of pitch tables and a larger disambiguating dictionary. Values are chosen for the dictionary randomly using melody.rand2d6(), an emulation of a roll of two six-sided dice, so as to create a bell curve distribution. Once a value is chosen from the dictionary, that value is used to access the corresponding index value of the pitch table array. Once a pitch table is selected, a pitch is randomly selected from that table to be played next. 
  More tables can be added, but currently the three pitch tables contain the pitches for 1) the current chord, 2) the scale pitches adjacent to the current pitch, and 3) the entire scale. Roll weight is meant to decrease with each subsequent entry.

Contents:
  melody.py:  Main script
  
  a440.py:    Array of chromatic pitches in Hz, tuned to A=440.

