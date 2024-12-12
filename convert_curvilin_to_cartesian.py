#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 16:25:48 2024

@author: sofi
"""
import numpy as np
#import matplotlib as plt
from get_normal_vector import get_normal_vector, get_segment_length
# s_curvilin - corresponds to discretized vector of the curvilinear space - NOT NEEDED  APPARENTLY
# q_curvilin - corresponding q values 
def convert_curvilin_to_cartesian(m, st_i, end_i, s_f, q_curvilin): # ,s_curvilin
    cand_coord_Cartesian = np.empty((2,end_i-st_i+1))

    # processing the candidate path #c
    for ind in np.arange(st_i, end_i+1):
        #ind = st_i
        print(np.array(["ind",ind]))
        s_arc_len = 0
        s_i = st_i
        # calculating the length of the path from the beginning of the currently processed segment to the point m[0:2,ind]
        while(s_i<ind + 1):
            # TODO: Atttention : the path segments are considered linear for simplification
           # s_arc_len += calculate_arc_length(m[0:2,s_i],m[0:2,s_i+1],m[2,s_i]) 
            s_arc_len += get_segment_length(m[0:2,s_i],m[0:2,s_i+1])
            s_i += 1
        print(s_arc_len)
        s_len_ind_curvilin = int(100*round(s_arc_len,2))
        if (s_arc_len > s_f):
            return cand_coord_Cartesian[:,0:ind]
            # plt.plot(cand_coord_Cartesian[0,:],cand_coord_Cartesian[1,:],"r")
            # plt.plot(m[0,st_i:ind],m[1,st_i:ind],"k")
        N_Pbf = get_normal_vector(m[0:2,ind],m[0:2,ind+1])
        #print([m[0:2,ind],m[0:2,ind+1],N_Pbf])
        cand_coord_Cartesian[:,ind] = m[0:2,ind]  + q_curvilin[s_len_ind_curvilin]*N_Pbf
    return cand_coord_Cartesian    