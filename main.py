from synth import *

## TEST
# define custom ADSR envelopes
adsr_flute = [6/14, 0, 8/14, 0] # use with square wave
adsr_violin = [10/37, 8/37, 10/37, 9/37] # use with square wave
adsr_cello = [0, 1, 0, 0] # use with square wave


a4 = Note('a4', adsr=[0.5, 0.2, 0.1, 0.1], effects=[('h', 4), ('v', 3, 'sine')])
a3 = Note('a3', adsr=[0.5, 0.2, 0.1, 0.1], effects=[('h', 4), ('v', 3, 'sine')])
c5 = Note('c5', adsr=[0.5, 0.2, 0.1, 0.1], effects=[('h', 4), ('v', 3, 'sine')])
e5 = Note('e5', adsr=[0.5, 0.2, 0.1, 0.1], effects=[('h', 4), ('v', 3, 'sine')])
e4 = Note('e4', adsr=[0.5, 0.2, 0.1, 0.1], effects=[('h', 4), ('v', 3, 'sine')])
g4 = Note('g4', adsr=[0.5, 0.2, 0.1, 0.1], effects=[('h', 4), ('v', 3, 'sine')])
b4 = Note('b4', adsr=[0.5, 0.2, 0.1, 0.1], effects=[('h', 4), ('v', 3, 'sine')])
d4 = Note('d4', adsr=[0.5, 0.2, 0.1, 0.1], effects=[('h', 4), ('v', 3, 'sine')])
f4 = Note('f4', adsr=[0.5, 0.2, 0.1, 0.1], effects=[('h', 4), ('v', 3, 'sine')])
f4s = Note('f4s', adsr=[0.5, 0.2, 0.1, 0.1],effects=[('h', 4), ('v', 3,'sine')])
g5 = Note('g5', adsr=[0.5, 0.2, 0.1, 0.1], effects=[('h', 4), ('v', 3, 'sine')])
c4 = Note('c4', adsr=[0.5, 0.2, 0.1, 0.1], effects=[('h', 4), ('v', 3, 'sine')])

a_minor_1 = Chord([a4, c5, e5])
a_minor_2 = Chord([a3, c4, e4])
e_minor = Chord([e4, g4, b4])
d_minor = Chord([d4, f4, a4])
am7 = Chord([a4, c5, e5, g5])

notes_1 = [a_minor_1,
		 a_minor_2,
		 e_minor,
		 d_minor,
		 am7,
		 am7,
		 a_minor_1,
		 d_minor
]
sector_1 = [f4s, f4s, g4, a4, a4, g4, f4s, e4 , d4 , d4 , e4 , f4s ,  f4s ,  e4 ,  e4]
apply_gnome_mode(sector_1) 
notes_2 = [*sector_1 , *sector_1]
output_1 = gen_waveform(notes_1)
output_1 = apply_filter(output_1, 'lowpass', [630], 2)
output_2 = gen_waveform(notes_2)
output_2 = apply_filter(output_2, 'lowpass', [630], 2)

play(output_2)
