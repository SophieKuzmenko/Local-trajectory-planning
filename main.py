#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 22:51:48 2024

@author: sofi
"""
import numpy as np

from generate_cand_path import generate_cand_path_curvilinear
from calculate_angle_of_the_path import calculate_angle_of_the_path
from space_transformations import convert_curvilin_to_cartesian
from get_reference_path_arc import get_reference_path_arc_lengths
from process_cand_curv_speed import get_cand_i_curvatures
from obstacle_collision_check import obstacle_collision_check
"""
 Loading the map
"""
def main(s_prev,q_prev, theta_prev, curb_prev,st_i, obstacles,R_ob, R_v, pos, ax1, ax2): 
    m = np.loadtxt("SevilleCoubureSignee.csv", comments="#", delimiter=",", unpack=False)
    m = m.T
    m = m[:,:-1]
    
    """
     Setting hyperparameters
    """
    hpath_distance = 100
    hn_q = 7
    hK_v = 0.5
    hl_max = 1.5*hpath_distance
    hds_f1_min = 10# 5*car_l# min acceptable length for the transient phase
    hds_f2_min = 30#3*car_l + 0.3# min acceptable length for the permanent phase
    hd_ss = 0.5
    # real-lie parameters
   # hroad_w = 4
    #hline_w = 1.5
    hcar_w = 1.8
    #hcar_l = 4.1
    hroad_margins = np.array([-2, 2]);
    hro_max = 0.2# 07#0.1 # https://www.cds.caltech.edu/~murray/books/AM08/pdf/fbs-steering_17Jul19.pdf
    # hV_Pbf_des = 25 # TODO: integrate with ROSS, to ask for desired velocity via ROSS
    # hV_Pbf_lim = 50 # TODO: also research more velocity limits for our frame
    # hacc_max = 2.5 # TODO: tune later #maximum acceptable lateral acceleration,
    ###############################
 
    """
     Setting parameters
    """
    V_v = 20# not a hyperparameter, will updated with ROS2
    
    q = np.linspace(hroad_margins[0] + hcar_w/2, hroad_margins[1] - hcar_w/2,hn_q)
    
    # Merging together a curved path of length hpath_distance
    """
     Calculating the index for the reference path of length hpath_distance
    """
    params = get_reference_path_arc_lengths(m, st_i, hpath_distance)
    s =params[0] 
    end_i = params[1]

    # Considering the case where the points taken continously are from two parts of the path array, e.g. end and beginning
    if (end_i < st_i):
        curb_bf = 1/m[2,st_i:-1]
        curb_bf =np.concatenate((curb_bf,1/m[2,0:end_i]))
    else:
        curb_bf = 1/m[2,st_i:end_i]
    
    #
    s_f1 = hds_f1_min + hK_v*V_v# K_v - gain 
    s_f2 = max(hds_f2_min, 2*hd_ss  - s_f1)
    
    s_f = min(hl_max, s_f1 + s_f2)

    ###############
    # theta - array of the path angles 
    ###############
    class Candidate:
        def __init__(self,q, valid=True):
            self.curvilin = []
            self.cartesian = []
            self.q = q
            self.ro = []
            self.valid = valid
    class Obstacle:
         def __init__(self, c, r):
             self.c = c
             self.r = r
    ###################
    
    candidates = []
    for dq in q:
        candidates.append(Candidate(dq))
    
    theta_bf = calculate_angle_of_the_path(m[:,st_i])#, m[:,(st_i+1)%m.shape[1]])

    for cand in candidates:
         cand.curvilin = generate_cand_path_curvilinear(cand, s_f1, s_f2, s_f, s_prev, q_prev, theta_prev, theta_bf, curb_prev, curb_bf)
         [cand.valid, cand.ro] = get_cand_i_curvatures(cand, curb_bf, hro_max, np.array(s), s_prev ,s_f1, s_f)
         cand.cartesian = convert_curvilin_to_cartesian(cand, m, st_i,np.array(s), s_prev, s_f1, s_f)
         cand.valid = cand.valid & obstacle_collision_check(cand, obstacles, R_v)   
    #
    cand_opt = Candidate(q[-1],False)
    for cand in candidates:
        if (cand.valid) & (abs(cand.q) <= abs(cand_opt.q)):
            cand_opt = cand
    if (not cand_opt.valid):
        cand_opt = candidates[0]     
        print(cand_opt.valid)
    
    return [candidates, cand_opt, np.array(s),  s_f1, s_f]