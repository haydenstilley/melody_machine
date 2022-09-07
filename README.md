# melody_machine
An RNG-based system that, given a set of musical chords and a diatonic key, will produce "improvised" melodies that harmonize with the piece.

The necessary arguments for the main() function are 1) [key], and 2) [sequence], further defined below.
  1)  [key] is an array created by the function melody.key(). The first entry in the array is itself a seven-item array denoting the pitches in a one-octave diatonic scale. The second entry in the array is another array denoting each chord in a chord progression as a three-item array, with each entry being a value in Hz corresponding to a pitch within the chord.
  2)  [sequence] is an array listing the musical piece's [meter], number of [bars], [chord progression], and [tempo], in that order. The first entry, [meter], is an integer denoting the number of beats in one measure. [bars] is an integer denoting the number of loops through the chord progression the musical piece lasts before it ends. [chord progression] is the same array as the second item in [key].
