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
	    # octave 3
	    'c3': 130.81,
	    'c3s': 138.59,
	    'd3': 146.83,
	    'd3s': 155.56,
	    'e3': 164.81,
	    'f3': 174.61,
	    'f3s': 185.00,
	    'g3': 196.00,
	    'g3s': 207.65,
	    'a3': 220.00,
	    'a3s': 233.08,
	    'b3': 246.94,

	    # octave 4
	    'c4': 261.63,
	    'c4s': 277.18,
	    'd4': 293.66,
	    'd4s': 311.13,
	    'e4': 329.63,
	    'f4': 349.23,
	    'f4s': 369.99,
	    'g4': 392.00,
	    'g4s': 415.30,
	    'a4': 440.00,
	    'a4s': 466.16,
	    'b4': 493.88,

	    # octave 5
	    'c5': 523.25,
	    'c5s': 554.37,
	    'd5': 587.33,
	    'd5s': 622.25,
	    'e5': 659.25,
	    'f5': 698.46,
	    'f5s': 739.99,
	    'g5': 783.99,
	    'g5s': 830.61,
	    'a5': 880.00,
	    'a5s': 932.33,
	    'b5': 987.77,

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
def play(output:np.array):
	write("output.wav", SAMPLERATE, output.astype(np.int16))
	subprocess.run("afplay output.wav", shell=True)

## TEST
a4 = Note('a4', adsr=[0.5, 0.2, 0.1, 0.1], effects=[('h', 4), ('v', 3, 'sine')])
a3 = Note('a3', adsr=[0.5, 0.2, 0.1, 0.1], effects=[('h', 4), ('v', 3, 'sine')])
c5 = Note('c5', adsr=[0.5, 0.2, 0.1, 0.1], effects=[('h', 4), ('v', 3, 'sine')])
e5 = Note('e5', adsr=[0.5, 0.2, 0.1, 0.1], effects=[('h', 4), ('v', 3, 'sine')])
e4 = Note('e4', adsr=[0.5, 0.2, 0.1, 0.1], effects=[('h', 4), ('v', 3, 'sine')])
g4 = Note('g4', adsr=[0.5, 0.2, 0.1, 0.1], effects=[('h', 4), ('v', 3, 'sine')])
b4 = Note('b4', adsr=[0.5, 0.2, 0.1, 0.1], effects=[('h', 4), ('v', 3, 'sine')])
d4 = Note('d4', adsr=[0.5, 0.2, 0.1, 0.1], effects=[('h', 4), ('v', 3, 'sine')])
f4 = Note('f4', adsr=[0.5, 0.2, 0.1, 0.1], effects=[('h', 4), ('v', 3, 'sine')])
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

output_1 = gen_waveform(notes_1)
output_1 = apply_filter(output_1, 'lowpass', [630], 2)
play(output_1)
