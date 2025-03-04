#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 18:07:47 2024

@author: sofi
"""
import numpy as np
import matplotlib.pyplot as plt

def get_poly_curvilin_value(poly_curvilin, s, s_prev, s_f1,s_f):
    return np.polyval(poly_curvilin[0], s)*int((s <= s_f1)&(s>=s_prev)) + np.polyval(poly_curvilin[1],s)*int( (s>s_f1) & (s<=s_f))

def get_poly_curvilin_value_arr(poly_curvilin, s, s_prev, s_f1, s_f):
    return np.polyval(poly_curvilin[0], s)*((s <= s_f1) &(s >= s_prev)).astype(int) + np.polyval(poly_curvilin[1],s)*((s>s_f1) &(s<=s_f)).astype(int)