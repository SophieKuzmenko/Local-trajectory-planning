#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 16:25:48 2024

@author: sofi
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
#from get_normal_vector import get_normal_vector, get_segment_length
from curvilin import get_poly_curvilin_value_arr

def convert_curvilin_to_cartesian(cand, m, st_i,s_arr,s_prev, s_f1, s_f): 
    mlen = m.shape[1]
    poly_curvilin = cand.curvilin
    cand_coord_Cartesian = np.empty((len(s_arr),2))
    # processing the candidate path
    q_s = get_poly_curvilin_value_arr(poly_curvilin,s_arr,s_prev, s_f1,s_f)
    for ind in range(0,len(s_arr)):
        s_arc_len = s_arr[ind]

        if (s_arc_len > s_f):
            return cand_coord_Cartesian[0:ind,:]
        # calculating the normal vector
        
        N_Pbf = get_normal_vector(m[0:2,(st_i+ind)%mlen], m[0:2,(st_i + ind+1)%mlen])
        cand_coord_Cartesian[ind,:] = (m[0:2,(st_i + ind)%mlen]  + q_s[ind]*N_Pbf)
    return cand_coord_Cartesian

def get_normal_vector(p1,p2):
    p0 = p2 - p1
    p0 = np.array([-p0[1], p0[0]])
    
    return p0/np.linalg.norm(p0)

