# melody_machine
An RNG-based system that, given a set of musical chords and a diatonic key, will produce "improvised" melodies that harmonize with the piece. All pitches are represented by their values in Hz, rounded to the hundredth place. Pyo must be installed for sound synthesis to function.

The necessary arguments for the main() function are 1) [key], and 2) [sequence], further defined below.
  1)  [key] is an array created by the function melody.key(). The first entry in the array is itself a seven-item array denoting the pitches in a one-octave diatonic scale. The second entry in the array is another array denoting each chord in a chord progression as a three-item array, with each entry being a value in Hz corresponding to a pitch within the chord.
    * A couple defaults are included in the script, namely melody.keyC and melody.keyCminor.
  2)  [sequence] is an array listing the musical piece's [meter], number of [bars], [chord progression], and [tempo], in that order. The first entry, [meter], is an integer denoting the number of beats in one measure. [bars] is an integer denoting the number of loops through the chord progression the musical piece lasts before it ends. [chord progression] is the same array as the second item in [key]. [tempo] is a value in seconds corresponding to the length of each beat.
    * A couple defaults are included in the script, namely melody.seqC and melody.seqCminor.

  The system is powered by an array of pitch tables and a larger disambiguating dictionary. Values are chosen for the dictionary randomly using melody.rand2d6(). Once a value is chosen from the dictionary, that value is used to access the corresponding index value of the pitch table array. Once a pitch table is selected, a pitch is randomly selected from that table to be played next. 
  
  More tables can be added, but currently the three pitch tables contain the pitches for 0) the current chord, 1) the scale pitches adjacent to the current pitch, and 2) the entire scale. The disambiguating dictionary is accessed after a simulation of the rolling of two dice, each with six sides (hereafter denoted as "2d6"). This creates a natural bell-curve with the most-frequent result of 7. The closer to 7 the result lies, the more frequently it occurs. The most improbable results are 2 and 12. Here is the default spread:
  
    [2d6]   [Next Table]
    
     2        Full Scale
     
     3        Full Scale
     
     4        Adjacent Pitches
     
     5        Adjacent Pitches
     
     6        Chordal Pitches
     
     7        Chordal Pitches
     
     8        Chordal Pitches
     
     9        Adjacent Pitches
     
     10       Adjacent Pitches
     
     11       Full Scale
     
     12       Full Scale
     
  The rhythmic aspects of the machine are still limited. Line 164 provides a method of eliminating the monotony a bit by simply not playing a certain percentage of the pitches produced. This creates a feeling of pseudo-phrasing that can sound quite musical. The value can be adjusted to preference.
  
  Depending on the chords within the piece, different orientations for [metatable] may be useful. Musical pieces that remain relatively diatonic will see little to no issues, but pieces with many chords outside of the scale will benefit from widening the [Chordal Pitches] category to include the [5] and [9] keys.
  
  Demo footage was created using the current version of MM and an accompaniment on acoustic guitar, played by me :)
  
  Contents:
  
  melody.py:  Main script
  
  a440.py:    Array of chromatic pitches in Hz, tuned to A=440.

