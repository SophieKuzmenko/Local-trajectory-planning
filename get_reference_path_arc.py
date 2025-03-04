#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 17:08:18 2024

@author: sofi
"""
import numpy as np

def get_reference_path_arc_lengths(m,st_i,hpath_distance):
    s_arr  = []
    s = 0
    end_i = st_i
    mlen = m.shape[1] - 1
    while(s<hpath_distance):  
        s_arr.append(s)
        A = m[0:2,(end_i)%mlen]
        B = m[0:2,(end_i+1)%mlen]
        rc_AB = m[2,(end_i)%mlen] # rayon de courbure
        s+= calculate_arc_length(A,B,rc_AB)
        end_i = (end_i + 1)%mlen
    return [s_arr,end_i]


def calculate_arc_length(A,B,rc_AB):
    theta_c = 2*np.arcsin(np.linalg.norm(B-A)/(2*rc_AB)) 
    # theta_c -> AB arc anle in the circle of the radius rc
    s = rc_AB*theta_c # the arc length
    return s