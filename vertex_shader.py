#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 09:37:26 2023

@author: alecdenny
"""
from resources import *
"""
init with 2 functions:
    - get_vert:
        input: most recent vertex, next vertex, percentage, range
        return: vertex to be appended
        
        +   this function is for interpolating between an input set of vertices to
            the shader in time / parameter space
    
    - get_delta
        input: most recently generated vertex during interpolation
        return: nr of samples to move forward in time to place the next window
        
        ex: if get delta is always 2, the windows will always overlap by two samples
        ex: if get delta returns the period of the current vertex, we will have
            something akin to wavetable synthesis, where each wave window is placed
            after the preceding one
            
contains functions:
    - interp
        input: start vertex, end vertex, offset
        return: list of vertices that interpolate between start and end vertex,
                  offset
                  
        +   Interpolate between two vertices in input data. when the previous
            returned data overshoots the time stamp of the end vertex, an offset 
            value is returned such that the time offset returned by get_delta remains
            accurate
            
            v1----------------v2--* <- end of previous fill
            v2--*-------------v3
                ^
                L start of next fill
           
            
         +   create an empty new vertex to pad / trim output of get_vert such that 
             appended vertices are always of the correct dimension 
             
         +   can not append a number of vertices greater than the number of samples
             between v1 and v2 to avoid infinite, or terribly long loops
             
         +   if time is somehow negative, it will be set to 0
         
         +   you can still do crazy suboptimal stuff in get_delta and get_vertex
             but hopefully, infinite render times, and other bugs are for the most part
             mitigated
             
    - fill_vertices
        input: control data
        return: interpolated data
        
        +   Fill gaps between all vertices in control data to place individual wave windows in time
        
        +   Time values less than zero will be replaced with zero currently
        
        +   Interpolation between points can't change directions in time currently
        

"""

    
class VertexShader():
    
    def __init__(self, get_vert, get_delta):
        self.get_vertex = get_vert
        self.get_delta = get_delta
        
    def interp(self, v1, v2, offset):
        n = len(v1)
        p = offset
        
        r = v2[Parameters.TIME] - v1[Parameters.TIME]
        direction = abs(r) / r
        r = abs(r)

        data = []
        
        #interp loop: move playhead position (relative to v1) until it exceeds range between v1 and v2
        while (p < r):
            
            #to protect against infinite loops, break if the number of vertices 
            #produced is greater than the number of samples between v1 and v2
            if(len(data) > r):
                offset = 0
                return data, offset
            
            #create empty vertex of correct length
            #call get_vertex, pad & trim output to length of input vertices
            new_vertex = np.zeros(n)
            interp_vertex = self.get_vertex(v1, v2, p, r)
            l = min(n,len(interp_vertex))
            new_vertex[:l] = interp_vertex[:l]
            
            #set time to current playhead position
            #if time is less than zero, set it to zero
            #make sure period is positive and >= 1
            new_vertex[Parameters.TIME] = max((p * direction) + v1[Parameters.TIME], 0)
            new_vertex[Parameters.PERIOD] = max(abs(new_vertex[Parameters.PERIOD]), 1.0)
            data.append(new_vertex)
            
            #advance playhead by delta
            delta = self.get_delta(new_vertex)
            p += abs(delta)
        
        #calculate overshoot 
        offset = (p - r) * direction

        return data, offset
        
    def fill_vertices (self, control_data):
        new_data = []
        offset = 0
        for v in range(0, len(control_data[0]) - 1):
            new_vs, offset = self.interp(control_data[:,v], control_data[:,v+1], offset)
            new_data += new_vs

        return new_data
    
    