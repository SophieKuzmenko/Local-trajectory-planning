#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 18:07:47 2024

@author: sofi
"""
import numpy as np
import matplotlib.pyplot as plt
"""
Functions to retrieve the value of a complex polynomial q(s) of degree 4, that consists of two parts.

The eqation for the polynomial depends on the value of s
q(s) = q_1(s) if s is bigger than s_prev and lies on the outside of the interval (s_f1,s_f)
q(s) = q_2(s) if s lies in the interval (s_f1,s_f)
"""
def get_poly_curvilin_value(poly_curvilin, s, s_prev, s_f1,s_f):
    return np.polyval(poly_curvilin[0], s)*int((s <= s_f1)&(s>=s_prev)) + np.polyval(poly_curvilin[1],s)*int( (s>s_f1) & (s<=s_f))

# Vectorization, due to casting functions used could not be combined with the single value case
def get_poly_curvilin_value_arr(poly_curvilin, s, s_prev, s_f1, s_f):
    return np.polyval(poly_curvilin[0], s)*((s <= s_f1) &(s >= s_prev)).astype(int) + np.polyval(poly_curvilin[1],s)*((s>s_f1) &(s<=s_f)).astype(int)