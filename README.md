# melody_machine

NOTE: The information in this README is deprecated. A new README will be available soon!

An RNG-based system that, given a set of musical chords and a diatonic key, will produce "improvised" melodies that harmonize with the piece. All pitches are represented by their values in Hz, rounded to the hundredth place. Pyo must be installed for sound synthesis to function.

The necessary objects for the primary function are: [Tonic], [Scale], [ChordSequence], and [Meter] - further defined below.

  [Tonic]: The tonal center of the piece. Stores a string denoting the note name and the note's value in Hz.
    Constructor method: components.Tonic(name, hz)
    Example: components.Tonic('A', 440) -> Tonic of A
    
  [Scale]: A tuple of integers corresponding to the intervals of each step/degree of the scale to be used.
    Two defaults are provided: definitions.scales['major'], and definitions.scales['minor'].
    Constructor method: components.Scale(steps)
    Example: components.Scale(definitions.scales['major']) -> Major key
    
  [ChordSequence]: Builds a chord progression based on construction arguments.
    Constructor method: components.ChordSequence(scale, scale_degrees, modifications=None)
      scale_degrees = a numbered sequence corresponding to a chord progression in the given Tonic and Scale. 
        Examples could be [1, 4, 5, 1], [1, 5, 6, 4], etc.
      modifications = a list of size (x*2) used to alter select chords from their diatonic origins.
        The first object in each (1*2) list is the index value of the chord to be altered. The second value is a string denoting the alteration.
        Defaults to None.
    Examples:
      I IV I V Progression:
        components.ChordSequence(definitions.scales['major'], [1, 4, 1, 5])
      i iv i V Progression (Final chord converted from its diatonic orientation to a major chord):
        components.ChordSequence(definitions.scales['minor'], [1, 4, 1, 5], [[3, 'major']])
      Hotel California (The Eagles, 1977):
              components.ChordSequence(definitions.scales['minor'], [1, 5, 7, 4, 6, 3, 4, 5], [[1,'major'], [3,'major'], [7,'major']])
  [Meter]: Sets specifications of timing and meter upon construction.
    Constructor method: components.Meter(beats, measures, bars, beat_duration=0.3)
      beats = The number of beats in a measure.
      measures = The number of measures in a bar.
      bars = The number of bars in the piece.
      beat_duration = A value in seconds denoting the time duration of a single beat. Defaults to 0.3.

  The system is powered by NoteTable objects that store lists of intervals for the program to randomly choose from. The program chooses which NoteTable to select from based on a simulated roll of two six-sided dice, so as to utilize a natural bell curve. The default spread can be found below. The closer to 7 the result lies, the more frequently it will occur.
  
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
     
  The rhythmic aspects of the machine are still limited. Line 85 provides a method of eliminating the monotony a bit by simply not playing a certain percentage of the pitches produced. This creates a feeling of pseudo-phrasing that can sound quite musical. The value can be adjusted to preference.
  
  Depending on the chords within the piece, different orientations for definitions.metaTable may be useful. Musical pieces that remain relatively diatonic will see little to no issues, but pieces with many chords outside of the scale may benefit from widening the [Chordal Pitches] values to include the [5] and [9] keys.
  
  Demo footage was created using the launch version of MM and an accompaniment on acoustic guitar, played by me :)
  
  Contents:
  
  melody.py:  Main script
  
  components.py: Classes
  
  definitions.py: Dictionaries
