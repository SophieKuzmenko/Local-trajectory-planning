#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 15:14:38 2024

@author: sofi
"""
import numpy as np
from curvilin import get_poly_curvilin_value_arr


def get_cand_i_curvatures(cand, ro_bf, ro_max, s_arr,s_prev, s_f1,s_f):
    poly_curvilin = cand.curvilin
    n_s = len(s_arr)
    qs = get_poly_curvilin_value_arr(poly_curvilin, s_arr, s_prev, s_f1, s_f)
    dpoly_curvilin = get_complex_poly_deriv(poly_curvilin, 1)
    ddpoly_curvilin = get_complex_poly_deriv(poly_curvilin,2)
    dqs = get_poly_curvilin_value_arr(dpoly_curvilin,s_arr, s_prev, s_f1, s_f)
    ddqs = get_poly_curvilin_value_arr(ddpoly_curvilin,s_arr, s_prev, s_f1, s_f)
    ro_cand = np.empty(n_s)
    a = 1 - qs*ro_bf # S = sign(a)
    b = (dqs**2 + a**2).astype(float) # Q^2
    ro_cand = a*(ro_bf + (a*ddqs + ro_bf*(dqs**2))/b)/np.sqrt(b)
    ro_cand = ro_cand.astype(float)
    return [all(abs(ro_cand) < ro_max), ro_cand]


def get_cand_i_speed(poly_curvilin, ro_bf, ro_cand, s_arr,s_prev, s_f1,s_f, V_Pbf_des, V_Pbf_lim,a_max):
     qs = get_poly_curvilin_value_arr(poly_curvilin,s_arr, s_prev,s_f1,s_f)
     dpoly_curvilin = get_complex_poly_deriv(poly_curvilin, 1)
     #ddpoly_curvilin = get_complex_poly_deriv(poly_curvilin,2)
     dqs = get_poly_curvilin_value_arr(dpoly_curvilin,s_arr, s_prev, s_f1, s_f)
     #ddqs = get_poly_curvilin_value_arr(ddpoly_curvilin,s_arr, s_f1, s_f)
     a = 1 - qs*ro_bf
     b = np.sqrt((dqs**2 + a**2).astype(float))
     V_des_init = np.sign(a)*b*V_Pbf_des
     V_limit = np.sign(a)*b*V_Pbf_lim
     V_ro = np.sqrt(a_max/ro_cand)
     return min(V_limit, V_ro, V_des_init)
 
    
def get_complex_poly_deriv(poly,m):
     res =[]
     for p in poly:
         res.append(np.polyder(p,m))
     return res
     
