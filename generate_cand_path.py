#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 13:59:03 2024

@author: sofi
"""
import numpy as np
# from solve_q_polynomial import solve_q_polynomial

def generate_cand_path_curvilinear(cand, s_f1, s_f2, s_f, s_prev,q_prev, theta_prev, theta_bf, curb_prev, curb_bf):
   q_f = cand.q
   coeff =  solve_q_polynomial(s_prev,q_prev, s_f1, q_f, theta_prev, theta_bf, curb_prev, curb_bf[0])#[0], curb_prev, curb_bf[0])#
   poly1 = np.poly1d(coeff[::-1])
   poly2 = np.poly1d(q_f)
   return [poly1,poly2]

   
import sympy as sp
   #import matplotlib.pyplot as plt

def solve_q_polynomial(s_prev, q_prev, s_f1, q_f, theta_prev, theta_bf, curb_prev, curb_bf):
       a2,a3,a4= sp.symbols('a2 a3 a4')
       # a0 and a1 were derived basing off logic
       a0 = q_prev
       a1 = np.tan(theta_prev - theta_bf)
       # additional variables to simplify the constraints notation
       a = 1 - a0*curb_bf
       b = np.sqrt(float(a1**2 + a**2))
       ds_s = s_f1 - s_prev
       # the constraints
       Eq1 =  sp.Eq(a1 + 2*a2*ds_s + 3*a3*ds_s**2 + 4*a4*ds_s**3, 0)
       Eq2 =   sp.Eq(a0 + a1*ds_s + a2*ds_s**2 + a3*ds_s**3 + a4*ds_s**4, q_f)
       Eq3 =  sp.Eq(np.sign(a)*(curb_bf + (2*a2*a + curb_bf*(b**2 - a**2))/b**2)/b, curb_prev)
       # Solving the constraint equations
       res =  sp.solve((Eq1,Eq2, Eq3),(a2,a3,a4), dict=True)
       #
       a2 = res[0][a2]
       a3 = res[0][a3]
       a4 = res[0][a4]
       return np.array([a0,a1,a2,a3,a4])
       