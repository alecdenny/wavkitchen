#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 09:39:15 2023

@author: alecdenny
"""

from frag_shader import *
from vertex_shader import *
import factory_funcs as ff

"""
init with 2 objects:
    - fragment shader initialized with its constituent functions
    - vertex shader initialized with its constituent functions
    
contains functions:
    - render
        input: control data
        return: synthesized output
        
        +   fill in control data data (call vertex shader to interpolate)
        +   call frag shader per vertex from filled data, append each window with time stamp to a list
        +   overlay all windows
        +   normalize output
        +   return audio as numpy array
    

"""

class WavKitchen():

    def __init__(self, frag: FragShader, vert : VertexShader):
        self.frag_shader = frag
        self.vertex_shader = vert
        
    
    def render(self, control_data, num_harms):
        
        self.frag_shader.num_harms = num_harms
        interp_data = np.asarray(self.vertex_shader.fill_vertices(control_data))
        dur = int(np.max(interp_data[:,Parameters.TIME]) + np.max(interp_data[:,Parameters.PERIOD]))
        
        plt.plot(interp_data[:,Parameters.TIME],interp_data[:,Parameters.PERIOD])
        plt.show()
        
        plt.plot(interp_data[:,Parameters.TIME],interp_data[:,Parameters.MOD])
        plt.show()
        
        plt.plot(interp_data[:,Parameters.TIME])
        plt.show()
        

        
        audio = np.zeros(dur, dtype=np.float32)
        for i in range(0, len(interp_data)):
            start = int(interp_data[i,Parameters.TIME])
            w = self.frag_shader.get_wave(interp_data[i])
            end = len(w) + start
            audio[start:end] += w
            
        return audio
    
        
        
        
    
        