import numpy as np
from scipy.io.wavfile import write
from scipy import signal
import subprocess
import math

SAMPLERATE = 44100

# Define the note class
class Note:
	def __init__(self, name:str=None, adsr:list = None, duration:float = 0.25, amplitude:int = 1, wave_type:str = 'sq', effects: list=None):
		self.name = name
		self.adsr = adsr
		self.duration = duration 		# duration in fraction of seconds
		self.amplitude = 1000*amplitude
		self.wave_type = wave_type
		self.effects = effects
		self.samplerate = 44100
		self.freq = self.frequencies[self.name]
		self.t = np.linspace(0., self.duration, int(self.duration * self.samplerate))
		self.gen_waveform()
		self.apply_adsr()
		self.apply_effects()
	

	frequencies = {
	   	# octave 0
		'c0': 16.35,
	    'c0s': 17.32,
		'd0f': 17.32,
	    'd0': 18.35,
	    'd0s': 19.45,
		'e0f': 19.45,
	    'e0': 20.60,
	    'f0': 21.83,
	    'f0s': 23.12,
		'g0f': 23.12,
	    'g0': 24.50,
	    'g0s': 25.96,
		'a0f': 29.14,
	    'a0': 27.50, # lowest piano note
	    'a0s': 29.14,
		'b0f': 29.14,
	    'b0': 30.87,  # 5 string bass's lowest note

	   	# octave 1
		'c1': 32.70,
	    'c1s': 34.65,
		'd1f': 34.65,
	    'd1': 36.71,
	    'd1s': 38.89,
		'e1f': 38.89,
	    'e1': 41.20, # lowest note on a bass 
	    'f1': 43.65,
	    'f1s': 46.25,
		'g1f': 46.25,
	    'g1': 49.00,
	    'g1s': 51.91,
		'a1f': 51.91,
	    'a1': 55.00,
	    'a1s': 58.27,
		'b1f': 58.27,
	    'b1': 61.74,
		
		# octave 2
		'c2': 65.41,
	    'c2s': 69.30,
		'd2f': 69.30,
	    'd2': 73.42,
	    'd2s': 77.78,
		'e2f': 77.78,
	    'e2': 82.41,
	    'f2': 87.31,
	    'f2s': 92.50,
		'g2f': 92.50,
	    'g2': 98.00,
	    'g2s': 103.83,
		'a2f': 103.83,
	    'a2': 110.00,
	    'a2s': 116.54,
		'b2f': 116.54,
	    'b2': 123.47,


	    # octave 3
	    'c3': 130.81,
	    'c3s': 138.59,
	    'd3': 146.83,
	    'd3s': 155.56,
		'e3f': 155.56,
	    'e3': 164.81,
	    'f3': 174.61,
	    'f3s': 185.00,
		'g3f': 185.00,
	    'g3': 196.00, # lowest note on a violin
	    'g3s': 207.65,
		'a3f': 207.65,
	    'a3': 220.00,
	    'a3s': 233.08,
		'b3f': 233.08,
	    'b3': 246.94,

	    # octave 4
	    'c4': 261.63, # middle C note on a piano
	    'c4s': 277.18,
		'd4f': 277.18,
	    'd4': 293.66,
	    'd4s': 311.13,
		'e4f': 311.13,
	    'e4': 329.63,
	    'f4': 349.23,
	    'f4s': 369.99,
		'g4f': 369.99,
	    'g4': 392.00,
	    'g4s': 415.30,
		'a4f': 415.30,
	    'a4': 440.00,
	    'a4s': 466.16,
		'b4f': 466.16,
	    'b4': 493.88,

	    # octave 5
	    'c5': 523.25,
	    'c5s': 554.37,
		'd5f': 554.37,
	    'd5': 587.33,
	    'd5s': 622.25,
		'e5f': 622.25,
	    'e5': 659.25,
	    'f5': 698.46,
	    'f5s': 739.99,
		'g5f': 739.99,
	    'g5': 783.99,
	    'g5s': 830.61,
		'a5f': 830.61,
	    'a5': 880.00,
	    'a5s': 932.33,
		'b5f': 932.33,
	    'b5': 987.77,
		
		# octave 6
		'c6': 1046.50,
	    'c6s': 1108.73,
		'd6f': 1108.73,
	    'd6': 1174.66,
	    'd6s': 1244.51,
		'e6f': 1244.51,
	    'e6': 1318.51,
	    'f6': 1396.91,
	    'f6s': 1479.98,
		'g6f': 1479.98,
	    'g6': 1567.98,
	    'g6s': 1661.22,
		'a6f': 1661.22,
	    'a6': 1760.00,
	    'a6s': 1864.66,
		'b6f': 1864.66,
	    'b6': 1975.53,

		# octave 7
		'c7': 2093.00,
	    'c7s': 2217.46,
		'd7f': 2217.46,
	    'd7': 2349.32,
	    'd7s': 2489.02,
		'e7f': 2489.02,
	    'e7': 2637.02,
	    'f7': 2793.83,
	    'f7s': 2959.96,
		'g7f': 2959.96,
	    'g7': 3135.96,
	    'g7s': 3322.44,
		'a7f': 3322.44,
	    'a7': 3520.00, # highest playable note on a violin
	    'a7s': 3729.31,
		'b7f': 3729.31,
	    'b7': 3951.07,


		# octave 8
		'c8': 4186.01, # highest note on a piano
	    'c8s': 4434.92,
		'd8f': 4434.92,
	    'd8': 4698.63,
	    'd8s': 4978.03,
		'e8f': 4978.03,
	    'e8': 5274.04,
	    'f8': 5587.65,
	    'f8s': 5919.91,
		'g8f': 5919.91,
	    'g8': 6271.93,
	    'g8s': 6644.88,
		'a8f': 6644.88,
	    'a8': 7040.00, 
	    'a8s': 7458.62,
		'b8f': 7458.62,
	    'b8': 7902.13,
	
	    # rest
	    'r': 0
	}

	def vibrato(self, v_freq:float, type:str):
		self.waveform *= self.wave(v_freq, type)

	def harmonics(self, order:int):
		h_amplitude = np.linspace(order, 1, order) * (1/math.factorial(order)) # decrease amplitude of harmonic n as n->order
		for i in range(0, order):
			self.waveform += h_amplitude[i] * self.wave(self.freq * (i+1))

    # creates waveform of given wave type
	def wave(self, freq:float=None, type:str=None):
		if freq == None:
			freq = self.freq
		if type==None:
			type = self.wave_type
		match type:
			case 'saw':
				return signal.sawtooth(2*np.pi*freq*self.t, width=1)
			case 'sq':
				return signal.square(2*np.pi*freq*self.t)
			case 'tri':
					return signal.sawtooth(2*np.pi*freq*self.t, width=0.5)
			case 'pulse':
				return signal.square(2*np.pi*freq*self.t, duty=0.3)
			case 'sine':
				return np.sin(2*np.pi*freq*self.t)
			case 'rest':
				return np.zeros(len(self.t))
			case _:
				return ''
                
    # applies adsr sequence
    # ADSR - "attack", "decay", "sustain", "release"
	def apply_adsr(self):
		if self.adsr == None:
			self.waveform = self.waveform
		else:
			len_waveform = int(self.duration * self.samplerate)
			num_attack = int(self.adsr[0] * len_waveform)
			num_decay = int(self.adsr[1] * len_waveform)
			num_release = int(self.adsr[3] * len_waveform)
			num_sustain = len_waveform - (num_attack + num_decay + num_release)
			
		 	# attack 
			self.waveform[0:num_attack] *= np.linspace(0, 1, num_attack)

			# decay
			self.waveform[num_attack:num_decay + num_attack] *= np.linspace(1, self.adsr[2], num_decay)

			# sustain
			self.waveform[num_decay + num_attack:num_sustain  + num_decay + num_attack] *= self.adsr[2]

			# release
			self.waveform[num_sustain  + num_decay + num_attack:num_decay + num_attack + num_release + num_sustain] *= np.linspace(self.adsr[2], 0, num_release)

	"""
	Effects:
	1. vibrato: ('v', v_freq, type)
		Vibrato effect is created by modulating (i.e. multiplying) the note's waveform with a wave of frequency v_freq.
		type specifies the wave type (i.e. 'sq', 'sine', 'saw', 'pulse').
	2. harmonics: ('h', order)
		nth harmonic is given as n*fundamental_frequency. Harmonics are added to the note's waveform.
	"""
	def apply_effects(self):
		if self.effects != None:
			for e in self.effects:
				match e[0]:
					case 'v':
						self.vibrato(e[1], e[2])
					case 'h':
						self.harmonics(e[1])
					case _:
						pass

	def gen_waveform(self):
		self.waveform = np.array([])
		self.waveform = self.amplitude * self.wave()
  
class Chord:
    def __init__(self, notes:list, effects:list=None):
        self.notes = notes
        self.gen_waveform()

    def gen_waveform(self):
        self.waveform = np.zeros(len(self.notes[0].waveform))
        for n in self.notes:
            self.waveform += n.waveform

# Applies a digital filter to the output waveform. Filter options:
# 'bandpass': cutoff_freq = [f_low, f_high]
# 'bandstop': cutoff_freq = [f_low, f_high]
# 'highpass': cutoff_freq = [fc]
# 'lowpass': cutoff_freq = [fc]
def apply_filter(waveform:np.array, type:str, cutoff_freq:list, order:int):
    if (type == 'low') or (type == 'high'):
        b, a = signal.butter(order, cutoff_freq[0], btype=type, fs=SAMPLERATE, analog=False)
        output = signal.filtfilt(b, a, waveform)
    else:
        b, a = signal.butter(order, cutoff_freq, btype=type, fs=SAMPLERATE, analog=False)
        output = signal.filtfilt(b, a, waveform)
    return output
        
# generates the output waveform given a list of Notes
def gen_waveform(notes:list):
	output = np.array([])
	for n in notes:
		output = np.append(output, n.waveform)
	return output

# plays output waveform's sound
# can only feed array of notes processed as a waveform, not an array of raw notes
def play(output:np.array):
	#folder = "python-audio"
	filename = "output_v2.wav"
	#fullpath = f'{folder}/{filename}'
	write("output.wav", SAMPLERATE, output.astype(np.int16))
	#subprocess.run("afplay output.wav", shell=True)

## TEST
# define custom ADSR envelopes
adsr_flute = [6/14 0 8/14 0] # use with square wave
adsr_violin = [10/37 8/37 10/37 9/37] # use with square wave
adsr_cello = [0 1 0 0] # use with square wave


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
notes_2 = [*sector_1 , *sector_1]
output_1 = gen_waveform(notes_1)
output_1 = apply_filter(output_1, 'lowpass', [630], 2)
output_2 = gen_waveform(notes_2)
output_2 = apply_filter(output_2, 'lowpass', [630], 2)

play(output_2)
