#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 22:51:48 2024

@author: sofi
"""
import numpy as np
import matplotlib.pyplot as plt
from generate_candidate_paths import generate_candidate_paths_curvilinear
from calculate_angle_of_the_path import calculate_angle_of_the_path
from convert_curvilin_to_cartesian import convert_curvilin_to_cartesian
from get_reference_path_end_idx import get_reference_path_end_idx

"""
 Loading the map
"""
m = np.loadtxt("SevilleCoubureSignee.csv", comments="#", delimiter=",", unpack=False)
m = m.T

"""
 Setting hyperparameters
"""
hpath_distance = 100
hn_q = 6
hK_v = 0.1
hl_max = 1.5*hpath_distance
hds_f1_min = 30# 5*car_l# min acceptable length for the transient phase
hds_f2_min = 30#3*car_l + 0.3# min acceptable length for the permanent phase
hd_ss = 0.5
# real-lie parameters
hroad_w = 4
hline_w = 1.5
hcar_w = 1.8
hcar_l = 4.1
hroad_margins = np.array([-2, 2]);
###############################
"""
 Setting parameters
"""
V_v = 20# not a hyperparameter, will updated with ROS2
# 
s = 0
st_i = 0
end_i = 0
#
q = np.linspace(hroad_margins[0] + hcar_w/2, hroad_margins[1] - hcar_w/2,hn_q)
#
# Merging together a curved path of length hpath_distance
"""
 Calculating the index for the reference path of length hpath_distance
"""
end_i = get_reference_path_end_idx(m,st_i,hpath_distance)
"""
 Generating candidate paths in curvilinear parameters
"""
s_prev = 0 # for the first segment processed
q_prev = 0 # for the first segment we stayed on the nominative path
theta_prev = 0
curb_prev = 0
curb_bf = 1/m[2,st_i:end_i]
#
s_f1 = hds_f1_min + hK_v*V_v# K_v - gain
s_f2 = max(hds_f2_min, 2*hd_ss  - s_f1)
s_f = min(hl_max, s_f1 + s_f2)
###############
# theta - array of the path angles 
###############
cand_curvilin = generate_candidate_paths_curvilinear(s_f1, s_f2, s_f, s_prev, q_prev, q, theta_prev, calculate_angle_of_the_path(m[:,st_i]), curb_prev, curb_bf)# theta_bf[0], curb_prev, curb_bf[0])
# Plotting in curvilinear
# for i in np.arange(1,cand_curvilin.shape[0]):
#    plt.plot(cand_curvilin[0,],cand_curvilin[i,],"b")
# plt.axhline(y=0,c="k",linestyle="--")
# Transforming into Cartesian coordinates
"""
 Transforming from cruvilinear into Cartesian coordinates
"""
cand_coord_Cartesian = []
for c in np.arange(0,hn_q):
    cand_coord_Cartesian.append(convert_curvilin_to_cartesian(m, st_i, end_i, s_f, cand_curvilin[c,:]))
"""
 Plotting in Cartesian coordinates
"""
plt.plot(m[0,st_i:end_i],m[1,st_i:end_i],"--k")
for c in np.arange(0,hn_q):
    plt.plot(cand_coord_Cartesian[c][0,:],cand_coord_Cartesian[c][1,:],"r")
