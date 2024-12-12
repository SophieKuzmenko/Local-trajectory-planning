#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 15:51:23 2024

@author: sofi
"""
import numpy as np
def calculate_arc_length(A,B,rc_AB):
    theta_c = 2*np.arcsin(np.linalg.norm(B-A)/(2*rc_AB)) 
    # theta_c -> AB arc anle in the circle of the radius rc
    s = rc_AB*theta_c # the arc length
    return s