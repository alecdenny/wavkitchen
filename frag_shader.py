#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 13:05:16 2023

@author: alecdenny

"""
from resources import *
"""
init with 2 functions:
    - get_harmonic:
        input: harmonic nr, vertex info
        return: amp, phase for given harmonic
        
    - process_window:
        input: synthesized window, vertex info
        return: synthesized window with time domain processing
        
init with 1 variable (num_harms):

    - how many harmonics amplitude and phase will be specified (maximum)
        
contains functions:
    - get_spectrum:
        input: vertex info,
        return: list of amps, phases for this vertex
        
        +   get spectrum by calling get_harmonic for each harmonic
        
        +   don't fill in amplitudes for harmonics over nyquist (period < 2 samples)
        
        +   pad spectrum with zeros if num_harms < period
        

        
    - synthesize:
        input: spectrum (amp, phase), period
        return: ifft synthesized wavelet (?) with given period, spectral info
        
        +   convert polar coordinates (amplitudes and phases) to rectangular coordinates for idft synthesis
        
        +   synthesize and return single wave window
        
    - get_wave:
        input: vertex_info
        return: ifft synthesized wavelet processed by process_window
        
        +   convert each vertex to a spectrum of a single wave window by calling get_spectrum. Synthesize using irfft
        
        +   apply time domain processing (process_window)
        

"""


class FragShader():
    
    def __init__(self, get_harmonic, process_window):
        self.get_harmonic = get_harmonic
        self.process_window = process_window
        
        self.num_harms = 512
        
    def get_spectrum(self, v):
        spectrum = []
        for harmonic in range(0, self.num_harms):
            if (harmonic / v[Parameters.PERIOD] > 2):
                break
            
            spectrum.append(self.get_harmonic(harmonic, v))
            
        fft_length = int(v[Parameters.PERIOD] // 2) + 1
        dim = min(self.num_harms, fft_length)
        padded_spectrum = np.zeros((fft_length, 2))
        padded_spectrum[:dim] = spectrum[:dim]   
        return padded_spectrum
    
    #convert polar (magnitude, phase per frequency) to rectangular(real, imaginary component amplitudes)
    def p_to_r(self, mag, phase):
        reX = mag * np.cos(phase)
        imX = mag * np.sin(phase)
        
        return reX, imX
    
    #convert from real valued magnitude and phase spectrum to complex coordinates
    def m_p_conversion (self, spectrum):
        reX, imX = self.p_to_r(spectrum[:,0], spectrum[:,1])
        return reX + (1j * imX)


    def synthesize(self, spec, p):
        if(p < 1.0):
            return np.zeros(1)
        
        complex_spec = self.m_p_conversion(spec)
        wave = np.fft.irfft(a=complex_spec, n=int(p), norm='forward')
        
        return wave
   
    def get_wave(self, v):
        spec = self.get_spectrum(v)
        w = self.synthesize(spec, v[Parameters.PERIOD])        
        w = self.process_window(w, v)

        return w
    

    
    
            


    