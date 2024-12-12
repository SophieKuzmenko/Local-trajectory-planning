#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 16:52:48 2024

@author: sofi
"""
import numpy as np

def get_normal_vector(p1,p2):
    p0 = p2 - p1
    p0[0] = -p0[0]
    return p0/np.linalg.norm(p0)
    
    
def get_segment_length(p1,p2):
    return np.linalg.norm(p2 - p1)

