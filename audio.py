import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
from scipy import signal
import subprocess


samplerate = 44100
t = np.linspace(0., 1., samplerate)
t = t[0:int(samplerate/2)]
amp = 1000 


def add_harmonics(note, order):
	fundamental_freq = frequencies[note]
	wav_int = waveforms[note]

	for i in range(1, order + 1):
		n_harmonic = signal.sawtooth(fundamental_freq + (100*i) * 2 * np.pi * t)
		wav_int += n_harmonic

	return wav_int


def create_waveform(notes):
	waveform = np.array([])
	rests = {'r1', 'r2', 'r3', 'r4', 'r5', 'ri'}

	for n in notes:

		if n in rests:
			waveform = np.append(waveform, waveforms[n])
		else:
			waveform = np.append(waveform, waveforms['ri'])
			note_h = add_harmonics(n, 4)
			waveform = np.append(waveform, note_h)

	return waveform


frequencies = {
	# frequencies for notes in 3rd octave
	'a3': 220.00,
	'b3': 246.94,
	'c3': 130.81,
	'd3': 146.83,
	'e3': 164.81,
	'f3': 174.61,
	'g3': 196.00,

	# frequencies for notes in 4th octave
	'a4': 440.00,
	'b4': 493.88,
	'c4': 261.63,
	'd4': 293.66,
	'e4': 329.63,
	'f4': 349.23,
	'g4': 392.00,

	# frequencies for notes in 5th octave
	'a5': 987.77,
	'b5': 880.00,
	'c5': 523.25,
	'd5': 587.33,
	'e5': 659.25,
	'f5': 698.46,
	'g5': 783.99
}


waveforms = {
	# 3rd octave
    'a3': amp * signal.sawtooth(2 * np.pi * frequencies['a3'] * t),
    'b3': amp * signal.sawtooth(2 * np.pi * frequencies['b3'] * t),
    'c3': amp * signal.sawtooth(2 * np.pi * frequencies['c3'] * t),
    'd3': amp * signal.sawtooth(2 * np.pi * frequencies['d3'] * t),
    'e3': amp * signal.sawtooth(2 * np.pi * frequencies['e3'] * t),
    'f3': amp * signal.sawtooth(2 * np.pi * frequencies['f3'] * t),
    'g3': amp * signal.sawtooth(2 * np.pi * frequencies['g3'] * t),

	# 4th octave
    'a4': amp * signal.sawtooth(2 * np.pi * frequencies['a4'] * t),
    'b4': amp * signal.sawtooth(2 * np.pi * frequencies['b4'] * t),
    'c4': amp * signal.sawtooth(2 * np.pi * frequencies['c4'] * t),
    'd4': amp * signal.sawtooth(2 * np.pi * frequencies['d4'] * t),
    'e4': amp * signal.sawtooth(2 * np.pi * frequencies['e4'] * t),
    'f4': amp * signal.sawtooth(2 * np.pi * frequencies['f4'] * t),
    'g4': amp * signal.sawtooth(2 * np.pi * frequencies['g4'] * t),

	# 5th octave
    'a5': amp * signal.sawtooth(2 * np.pi * frequencies['a5'] * t),
    'b5': amp * signal.sawtooth(2 * np.pi * frequencies['b5'] * t),
    'c5': amp * signal.sawtooth(2 * np.pi * frequencies['c5'] * t),
    'd5': amp * signal.sawtooth(2 * np.pi * frequencies['d5'] * t),
    'e5': amp * signal.sawtooth(2 * np.pi * frequencies['e5'] * t),
    'f5': amp * signal.sawtooth(2 * np.pi * frequencies['f5'] * t),
    'g5': amp * signal.sawtooth(2 * np.pi * frequencies['g5'] * t),

    # rests
    'r1': np.zeros(int(samplerate / 4)),
    'r2': np.zeros(int(samplerate / 8)),
    'r3': np.zeros(int(samplerate / 16)),
    'r4': np.zeros(int(samplerate / 32)),
    'r5': np.zeros(int(samplerate / 64)),
    'ri': np.zeros(int(samplerate / 256))
}

# notes to be played
notes = ['g3', 'a3', 'c4', 'a3', 'e4', 'e4', 'd4', 'r4', 'g3', 'a3', 'c4', 'a3', 'd4', 'd4', 'c4', 
		 'b3', 'a3', 'r4', 'g3', 'a3', 'c4', 'a3', 'c4', 'd4', 'b3', 'a3', 'g3', 'ri', 'g3', 'd4', 'c4']

data_out = create_waveform(notes)
write("output.wav", samplerate, data_out.astype(np.int16))
subprocess.run("afplay output.wav", shell=True)

