# python-synth
A python-based synthesizer that generates audio waveforms given a sequence of notes and/or chords. Effects and filters can be added to the waveforms for added sound design freedom.

## Defining Notes
### Syntax:
```
Note(name:str, adsr:list, duration:float, amplitude:int, wave_type:str, effects:list)
```
* name: note name
* adsr: adsr envelope. stands for "attack", "decay", "sustain", "release". A four-element list in which the sum of elements is equal to one. 
* duration: length of time that note is played for in fraction of a second  (default is 0.25s)
* amplitude: loudness of the note, defined as an integer > 0 (default is 1)  
* wave_type: waveform type  (default is 'sq')  
          - square -> 'sq'  
          - sine -> 'sine'  
          - sawtooth -> 'saw'  
          - pulse -> 'pulse'  
          - triangle -> 'tri'  
          - rest -> 'r'  
* effects: list of effects to be applied (defined in next section, default=None)
### Example
```
a4 = Note('a4', adsr=[0.4, 0.3, 0.2, 0.1])
```
## Defining Chords
```
Chord(notes:list, effects:list)
```
Given a list of notes, a chord waveform is generated
### Example
```
am7 = Chord(['a3', 'c4', 'e4', 'g4'])
```
## Effects
Effects are defined in the note and chord class as lists of tuples.
### Note Effects
#### Vibrato
The vibrato effect is created by multiplying a note's waveform with a lower frequency waveform.
```
('v', v_freq, type)
```
##### Use
* v_freq: frequency of waveform to be multiplied with note waveform
* type: waveform type, same wave types as given in the note definition (i.e. 'sq', 'sine, etc.)

#### Harmonics
```
('h', order)
```
Harmonics are waveforms added to the note waveform in which their frequencies are multiples of the fundamental frequency. The order specifies how many harmonics are added. The amplitude of the harmonics decreases toward the nth harmonic. 

