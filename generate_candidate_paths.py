#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 13:59:03 2024

@author: sofi
"""
import numpy as np
from solve_q_polynomial import solve_q_polynomial

def generate_candidate_paths_curvilinear(s_f1, s_f2, s_f, s_prev,q_prev, q, theta_prev, theta_bf, curb_prev, curb_bf):
   hn_q = len(q)
   step = 0.01
   s_arr = np.arange(0,s_f + step, step)
   # matrix that stores in the rows values of the generated paths
   res = np.zeros((hn_q, len(s_arr)) ) 
   #res[0,] = s_arr
   for j in np.arange(0,hn_q):
        q_f = q[j]
        coeff =  solve_q_polynomial(s_prev,q_prev, s_f1, q_f, theta_prev, theta_bf, curb_prev, curb_bf[0])#[0], curb_prev, curb_bf[0])#
        poly1 = np.poly1d(coeff[::-1])
        ss_f1 = np.arange(0, s_f1,step )
        val_f1 = np.polyval(poly1,ss_f1)
        poly2 = np.poly1d(q_f)
        ss_final = np.arange(s_f1 , s_f+step, step )
        val_final = np.polyval(poly2,ss_final)
        #print(len(np.concat((val_f1,val_final))))
        res[j,] = np.concat((val_f1,val_final))
   return res