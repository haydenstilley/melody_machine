from time import sleep
import random
from pyo import *
import a440

##  --- MELODY MACHINE  ---
## Written by Hayden Stilley, September 2022
## (requires an install of pyo, a software synthesizer for Python.)
## SUMMARY: This is an engine that, given a sequence of chords and a key, pseudo-randomly produces pitch values (in Hz) that, when strung together, act as a melody over the chord progression. There are limitations currently - see below.
## LIMITATION 1: There is virtually no rhythm functionality as of yet. In musical terms, this means the melody is only capable of playing quarter/eighth notes.
## LIMITATION 2: The engine has little capability to create musical phrases, as it scantly references previously played pitches while picking a new pitch, and has no system for remembering motifs. A Markov-based generation system may be helpful, but would need several layers of complexity to be effective.
## LIMITATION 3: As the engine essentially keeps no track of previously played pitches, the scope of the melody is locked to a 1-octave range to keep it from meandering too far from home.

## Establishes melodic framework. 'root' is a numerical value corresponding with an index value in [stage]. There are still limitations.
## LIMITATION 1: Only one octave range
## LIMITATION 2: No ability to change key (though this is more intrinsic to the code and requires a little rewrite).
def key(stage, root, scale, sequence):
    pitch = stage[root]
    key1 = [pitch]
    for interval in scale:
        root += interval
        pitch = stage[root]
        key1.append(pitch)
    chords = sequence[2]
    keyOut = [key1,chords]
    return keyOut

## Establishes sequence of musical piece. Tempo is a numerical value in seconds.
def sequence(meter,bars,chords,tempo):
    seqOut = [meter,bars,chords,tempo]
    return seqOut

## Sets initial pitch tables.
def setTables(key,position=2):
    t1 = key[1][0] ## current chord
    if (position==0):
        t2 = [key[0][position+1]]
    elif (position==(len(key[0])-1)):
        t2 = [key[0][position-1]]
    else:
        t2 = [key[0][position-1],key[0][position+1]] ## adjacent pitches
    t3 = key[0] ## full scale
    tables = [t1,t2,t3]
    return tables

## Randomizer emulating a roll of two six-sided dice
def rand2d6():
    x = (random.randint(1,6) + random.randint(1,6))
    return x

## Percentage randomizer. Outputs a decimal from 0.01 - 1.0
def rand100():
    x = (random.randint(1,100) / 100)
    return x

## Outputs an index number corresponding to the newly picked pitch table.
def pickTable(_metaTable):
    meta = rand2d6()
    tIndex = _metaTable[str(meta)]
    return tIndex
    
## Takes the index value from pickTable() and randomly picks a pitch from the corresponding sublist.
def pickPitch(_tables, _tIndex):
    subTable = _tables[_tIndex]
    pitch = random.randint(0,(len(subTable)-1))
    return _tables[_tIndex][pitch]

class Parameters:
    ## Default scale orientations. First is C Major - Ionian, second is C Minor - Aeolian.
    scale = [2,2,1,2,2,2]
    minorScale = [2,1,2,2,1,2]
    ## Primary array of available pitches. Contains a chromatic scale from C4 to B6.
    stage = [a440.C4,
        a440.C_SHARP4,
        a440.D4,
        a440.D_SHARP4,
        a440.E4,
        a440.F4,
        a440.F_SHARP4,
        a440.G4,
        a440.G_SHARP4,
        a440.A4,
        a440.A_SHARP4,
        a440.B4,
        a440.C5,
        a440.C_SHARP5,
        a440.D5,
        a440.D_SHARP5,
        a440.E5,
        a440.F5,
        a440.F_SHARP5,
        a440.G5,
        a440.G_SHARP5,
        a440.A5,
        a440.A_SHARP5,
        a440.B5,
        a440.C6,
        a440.C_SHARP6,
        a440.D6,
        a440.D_SHARP6,
        a440.E6,
        a440.F6,
        a440.F_SHARP6,
        a440.G6,
        a440.G_SHARP6,
        a440.A6,
        a440.A_SHARP6,
        a440.B6]
        
    ## Default sequences and keys. 
    
    ## C Major (Ionian). Key is listed after default progressions in that key.
    ## I V vi IV
    seqC = sequence(8,4,[a440.CMAJOR,a440.GMAJOR,a440.AMINOR,a440.FMAJOR],0.2)
    ## IV V iii vi (Koakuma)
    seqCk = sequence(8,4,[a440.FMAJOR,a440.GMAJOR,a440.EMINOR,a440.AMINOR],0.2)
    ## ii V I (Turnaround)
    seqCt = sequence(8,4,[a440.DMINOR,a440.GMAJOR,a440.CMAJOR,a440.CMAJOR],0.2)
    ## I iv IV V (50's)
    seqCf = sequence(8,4,[a440.CMAJOR,a440.AMINOR,a440.FMAJOR,a440.GMAJOR],0.2)
    ## The Killing Moon (Echo and The Bunnymen)
    seqCecho = sequence(8,4,[a440.CMAJOR,a440.FMINOR,a440.CMAJOR,a440.FMINOR],0.3)
    keyCmajor = key(stage,0,scale,seqC)
    
    ## C Minor (Aeolian)
    ## i iv i V (Minor Blues / Django Chords)
    seqCminor = sequence(8,4,[a440.CMINOR,a440.FMINOR,a440.CMINOR,a440.GMAJOR],0.2)
    
    keyCminor = key(stage,0,minorScale,seqCminor)
    
    ## Dictionary to facilitate randomly picking a pitch table produced by setTables().
    metaTable = {
        "2": 2,
        "3": 2,
        "4": 1,
        "5": 1,
        "6": 0,
        "7": 0,
        "8": 0,
        "9": 1,
        "10": 1,
        "11": 2,
        "12": 2
    }
    ## Defaults
    dMeter = seqCminor[1]
    dChords = seqCminor[2]
    dLoops = 4
    dMeasures = seqCminor[0]
    dTempo = [3]

## Main function. Default chord progression is i-iv-i-V in C Minor.
def main(sequence=Parameters.seqCminor, key=Parameters.keyCminor):
    defaults = Parameters()
    s = Server().boot()
    s.start()
    run1 = True
    ## parameters for needle are: beat [0], measure [1], current loop [2], and chord [3].
    needle = [1,1,1,sequence[2][0]]
    tables = setTables(key)
    while (run1 == True):
        for measure1 in range(sequence[1]):
            for beat1 in range(sequence[0]):
                needle[0] = (beat1+1)
                if needle[0] > sequence[0]:
                    needle[0] = 0
                print(needle[0])
                pitch = (pickPitch(tables,pickTable(defaults.metaTable)))
                if (rand100()>.4): ## Makes it so that 60% of the beats will have a new pitch, and the remaining 40% will hold the pitch of the previous beat. Adjustable to preference.
                    _sine = Sine(freq=pitch).out() ## _sine is the object that produces sound.
                print(pitch)
                tick = 0 ## this is so ugly. we should change it to an enumerate() function when we feel the urge.
                for i in key[0]:
                    if (i==pitch):
                        setTables(key,tick)
                    tick += 1
                sleep(sequence[3])
            needle[1] = (measure1+1)
            needle[3] = sequence[2][measure1]
            print(needle[3])
        needle[2] += 1
        if needle[2] > 4: ## song length arbitrarily set to 4 loops.
            run1 = False
            break
    s.stop()
    return
