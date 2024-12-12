#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 17:08:18 2024

@author: sofi
"""
from calculate_arc_length import calculate_arc_length

def get_reference_path_end_idx(m,st_i,hpath_distance):
    s = 0
    end_i = st_i
    while(s<hpath_distance):
        A = m[0:2,end_i] 
        B = m[0:2,end_i+1]
        rc_AB = m[2,end_i] # rayon de courbure
        s+= calculate_arc_length(A,B,rc_AB)
        end_i+=1
    end_i -=1 
    # the index of the end of last path segment taken into our current processed big segment
    return end_i