#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 10:14:09 2024

@author: alecdenny
"""

from wav_kitchen import *
from scipy.io.wavfile import write
from scipy.interpolate import CubicSpline

num_harms = 512
fs = 44100
rand_table = np.random.rand(num_harms, 32)
duration = 100000



def clamp (n, low, high):
    if (n > high):
        return high
    if (n < low):
        return low
    return n
    

def get_vert(v1, v2, p, r):
    
    #linear interpolation
    new_v = np.zeros(len(v1))
    pcent = abs(float(p / r))
    
    #interpolate values except time
    for l in range(1, len(new_v)):
        new_v[l] = v1[l] * (1.0 - pcent) + v2[l] * pcent

    new_v[Parameters.PERIOD] = int(new_v[Parameters.PERIOD])
    
    
    return new_v

def get_delta(v):
    x = int(math.floor(v[Parameters.MOD] * rand_table.shape[0]) - 1)
    y = int(math.floor(v[Parameters.TIME] / duration * rand_table.shape[1]))
    jitter = rand_table[x,y] 
    jitter *= (v[Parameters.MOD])
    return clamp(1000 * jitter,16, 1000)
    return v[Parameters.PERIOD] * (1.0-jitter)
    
    
def get_harmonic(nr, v):
    mag = 0.0
    phase = 0.0
    
    if nr == 0:
        return [mag, phase]

    
    x = int(math.floor(v[Parameters.MOD] * rand_table.shape[1]) - 1)
    x = clamp (x, 0, rand_table.shape[1] - 1)
    
    y = int(math.floor(v[Parameters.TIME] / duration * rand_table.shape[1]))
    mag = rand_table[nr,x] * float(rand_table[num_harms - nr, 32 - x - 1] > v[Parameters.MOD])
    phase = rand_table[nr,y] * 3.14
    return [mag, phase]
    
    

def process_window(w, v):
    window = np.hanning(len(w))
    return w * window * v[Parameters.AMP]
    return w
    
v = VertexShader(get_vert, get_delta)
f = FragShader(get_harmonic, process_window)
wk = WavKitchen(f, v)


window_len = 1024

data = np.array([[0,    duration],
                 [1000,2000],
                 [1.0,  0.0],
                 [1.0, 0.0]
        ])



audio = wk.render(data, num_harms)

#convert to 16bit int + normalize    
audio = audio * (2 ** 15 - 1) / np.max(np.abs(audio))
audio = audio.astype(np.int16) 
plt.plot(audio)
plt.show()
w_obj = sa.WaveObject(audio, 1, 2, fs)

def p(m):
    n = 0
    while(n < m):
        play_obj = w_obj.play()
        play_obj.wait_done()
        n += 1
        
p(1)

def w(name):
    
    write(name+'.wav', 44100, audio.astype(np.int16))