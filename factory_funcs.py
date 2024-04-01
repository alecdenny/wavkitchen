#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 11:06:31 2024

@author: alecdenny
"""




def clamp (n, low, high):
    if (n > high):
        return high
    if (n < low):
        return low
    return n




def midi_to_freq(note_midi: int, fs: float):
    #convert 0-127 midi note to frequency
    
    pass

def freq_to_midi(freq_hz: float, fs: float):
    #convert frequency to 0-127 midi note
    pass

def mod_to_freq(value: float, fs: float):
    #convert 0 to 1 modulation value to frequency
    pass

def freq_to_samps(value):
    pass

def samps_to_freq(value):
    pass
