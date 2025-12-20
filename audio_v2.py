import numpy as np
from scipy.io.wavfile import write
from scipy import signal
import subprocess
import matplotlib.pyplot as plt

SAMPLERATE = 44100

# Define the note class
class Note:
	def __init__(self, name:str, adsr:list = None, duration:float = 0.25, amplitude:int = 1, wave_type:str = 'sq', effects: list = None):
		self.name = name
		self.adsr = adsr
		self.duration = duration 		# duration in fraction of seconds
		self.amplitude = 1000*amplitude
		self.wave_type = wave_type
		self.effects = effects
		self.samplerate = 44100
		self.t = np.linspace(0., self.duration, self.samplerate) #time vector for note
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
	}

  # creates waveform of given wave type
	def wave(self):
		match self.wave_type:
			case 'saw':
				return signal.sawtooth(2*np.pi*self.frequencies[self.name]*self.t, width=1)
			case 'sq':
				return signal.square(2*np.pi*self.frequencies[self.name]*self.t)
			case 'tri':
					return signal.sawtooth(2*np.pi*self.frequencies[self.name]*self.t, width=0.5)
			case 'pulse':
				return signal.square(2*np.pi*self.frequencies[self.name]*self.t, duty=0.3)
			case 'sine':
				return np.sin(2*np.pi*self.frequencies[self.name]*self.t)
			case _:
				return ''
  # applies adsr sequence
	def apply_adsr(self):
		if self.adsr == None:
			self.waveform = self.waveform
		else:
			num_attack = int(self.adsr[0] * self.samplerate)
			num_decay = int(self.adsr[1] * self.samplerate)
			num_release = int(self.adsr[3] * self.samplerate)
			num_sustain = len(self.waveform) - (num_attack + num_decay + num_release)
			 	
		 	# attack 
			self.waveform[0:num_attack] *= np.linspace(0, 1, num_attack)

			# decay
			self.waveform[num_attack:num_decay + num_attack] *= np.linspace(1, self.adsr[2], num_decay)

			# sustain
			self.waveform[num_decay + num_attack:num_sustain  + num_decay + num_attack] *= self.adsr[2]

			# release
			self.waveform[num_sustain  + num_decay + num_attack:num_decay + num_attack + num_release + num_sustain] *= np.linspace(self.adsr[2], 0, num_release)

  # to be implemented
	def apply_effects(self):
		self.waveform = self.waveform

	def gen_waveform(self):
		self.waveform = np.array([])
		self.waveform = self.amplitude * self.wave()

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
# Sample definition of notes
notes = [Note(name='a4', duration=0.25, wave_type='saw'),
			Note(name='b4', adsr=[0.4, 0.2, 0.2, 0.2])]

output = gen_waveform(notes)
play(output)
