#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 16:51:54 2025

@author: sofi
"""


import matplotlib.pyplot as plt
import numpy as np
import random
import time

from main import main
# from get_closest_index import get_closest_index
from get_reference_path_arc import get_reference_path_arc_lengths
from testing_helpers import fxy, sub_mod_pi2, ecart_pente_frenet, draw_car
from calculate_angle_of_the_path import calculate_angle_of_the_path
from curvilin import get_poly_curvilin_value_arr
from map_matching_funcs import discretize_path, generate_obstacle, find_closest_segment_index, distance_point_to_line_segment, get_projection_params, get_q, get_segm_angle 

def init_plots_curvilin(ax, candidates, s_prev, s_f1, s_f):
    sspace = np.linspace(0,s_f)
    ax.axhline( y = 0, color='k', linestyle='--') 
    ax.axvline(x=s_f1, color='k', linestyle=':')
    ax.axvline(x=s_prev, color='k', linestyle=':')
    ax.set_xlabel("s")
    ax.set_ylabel("q")
    ax.set_title("Candidate paths in curvilinear space (s,q)")
    lines = []
    for cand in candidates:
        line, =  ax.plot(sspace, get_poly_curvilin_value_arr(cand.curvilin,sspace,s_prev,s_f1,s_f), c= get_color(cand, cand_opt))    
        lines.append(line)
    return lines

def init_plots_cart(ax, candidates,cand_opt, obstacles, m, st_i, pos):
    ax.plot(m[0,:],m[1,:],"--k")
    #ax.plot(pos[0],pos[1],"-o",markersize=4, markeredgecolor="k")
    #ax.plot(m[0,st_i],m[1,st_i],"*k")
    ax.set_title("Candidate paths in Cartesian space, (x,y)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    lines = []
    for obstacle in obstacles:
        obstacle_plt = plt.Circle(obstacle.c, obstacle.r)  
        ax.add_patch(obstacle_plt)
    for cand in candidates:
        colstyle = get_color(cand,cand_opt)
        line, = ax.plot(cand.cartesian[:,0], cand.cartesian[:,1], c=colstyle)
        lines.append(line)
    return lines

def get_color(cand,cand_opt):
    colstyle = "orangered"
    if (cand.valid):
        colstyle = "powderblue"
    if ((cand.q == cand_opt.q) & cand_opt.valid):
        colstyle = "green"
    return colstyle
      
class Obstacle:
     def __init__(self, c, r):
         self.c = c
         self.r = r

s1 = -2
s2 = -2
L1 = - s1*s2
L2 = -s1 -s2


v = 10
ed = 0
L = 2

m = np.loadtxt("SevilleCoubureSignee.csv", comments="#", delimiter=",", unpack=False)
m = m.T
m = m[:,:-1]
mlen = m.shape[1]

### PARAMETERS PASSED BY ROSS ############
   # obstacle = np.array([0,0])
R_ob = 0.6 # 1.2 meter diameter for the pedestrian
R_v = 2.1 # 4.2 d car circle
##########################################

obstacle  =Obstacle(np.array([-90.48042692, 130.32694196]),R_ob)# Obstacle(np.array([-140.102, 106.544]),R_ob)
obstacles = []
obstacles.append(obstacle)
obstacles.append(Obstacle(np.array([-140.102, 106.544]),R_ob))
obstacles.append(Obstacle(np.array([-126.9, 127.2]), R_ob))
st_i = 10# 56#20 - quite a deviation -> q is too big for the path:/
s_prev = 0#16
q_prev = 0#0.2
theta_prev = calculate_angle_of_the_path(m[:,st_i])
curb_prev =  0#1/m[2,3]

pos_v = m[0:2,st_i]
plt.ion()
figure, (ax1,ax2) =  plt.subplots(nrows=1,ncols=2,figsize=(12,5))
params = main(s_prev,q_prev, theta_prev, curb_prev,st_i, obstacles, R_ob, R_v, pos_v,ax1,ax2)
## ax1.clear()
candidates = params[0]
cand_opt = params[1]
s = params[2]
s_f1 = params[3]
s_f = params[4]
cand_opt_q = get_poly_curvilin_value_arr(cand_opt.curvilin, s, s_prev, s_f1, s_f)
"""
Map matching
"""
# ind = random.randint(0, cand_opt.cartesian.shape[0] - 2)
# pos_v = cand_opt.cartesian[ind,:]
# pos_v = pos_v + 0.35*(cand_opt.cartesian[(ind+1),:] - cand_opt.cartesian[ind,:])
# theta = get_segm_angle(pos_v, cand_opt.cartesian[(ind+1),:])
# p = np.array([pos_v[0], pos_v[1], theta])
# ind_m_closest = find_closest_segment_index(m, p)
# _,q_prev = get_projection_params(m[0:2, ind_m_closest], m[0:2,(ind_m_closest+1)], pos_v)
# curb_prev = cand_opt.ro[ind_m_closest - st_i]
# #st_i = ind_m_closest
# theta_prev = calculate_angle_of_the_path(np.array([pos_v[0],pos_v[1],curb_prev]))
# ax2.plot(pos_v[0], pos_v[1],"*m")
# ax2.plot(m[0,ind_m_closest:(ind_m_closest+1)], m[1,ind_m_closest:(ind_m_closest+1)],ls = "--", c="yellow")
# print([m[0,ind_m_closest:(ind_m_closest +2)], m[1,ind_m_closest:(ind_m_closest +2)]])
# ax2.plot(m[0,ind_m_closest:(ind_m_closest +2)], m[1,ind_m_closest:(ind_m_closest +2)], c="gold", linewidth="5" )
"""
"""
# for cand in candidates:
#     #print(cand.cartesian)
#     lines.append(plot_curvilin(ax1, cand.curvilin, s_prev, s_f1, s_f))
lines_cart = init_plots_cart(ax2, candidates, cand_opt, obstacles, m, st_i, pos_v)
lines_curvilin = init_plots_curvilin(ax1, candidates, s_prev, s_f1, s_f)
plt.show()


"""
Map matching addition
"""
# params = main(s_prev,q_prev, theta_prev, curb_prev, st_i, obstacles, R_ob, R_v,pos_v, ax1, ax2)
# candidates = params[0]
# cand_opt = params[1]
# s = params[2]
# s_f1 = params[3]
# s_f = params[4]
# cand_opt_q = get_poly_curvilin_value_arr(cand_opt.curvilin, s, s_prev, s_f1, s_f)
# #
# sspace = np.linspace(0,s_f)
# for l in range(len(lines_curvilin)):
#     col = get_color(candidates[l],cand_opt)
#     new_qspace = get_poly_curvilin_value_arr((candidates[l]).curvilin,sspace,s_prev,s_f1,s_f)
#     (lines_curvilin[l]).set_xdata(sspace)
#     (lines_curvilin[l]).set_ydata(new_qspace)
#     (lines_curvilin[l]).set_color(col)
#         #
#     (lines_cart[l]).set_color(col)
#     (lines_cart[l]).set_xdata((candidates[l]).cartesian[:,0])
#     (lines_cart[l]).set_ydata((candidates[l]).cartesian[:,1])
#     figure.canvas.draw()
#     figure.canvas.flush_events()
# ax2.plot(m[0,ind_m_closest+1], m[1,ind_m_closest+1],"*k")
# plt.show()
"""
"""
for j in range(50):
    ind = 3#random.randint(0, cand_opt.cartesian.shape[0] - 1)
    s_prev = 0
    curb_prev = cand_opt.ro[ind]
    q_prev = cand_opt_q[ind]
    P = np.array([cand_opt.cartesian[ind,0],cand_opt.cartesian[ind,1], 1/cand_opt.ro[ind]])
    theta_prev = calculate_angle_of_the_path(P)
    st_i = (st_i + ind)%mlen
    pos_v = cand_opt.cartesian[ind,0:2]
    params = main(s_prev,q_prev, theta_prev, curb_prev, st_i, obstacles, R_ob, R_v,pos_v, ax1, ax2)
    candidates = params[0]
    cand_opt = params[1]
    s = params[2]
    s_f1 = params[3]
    s_f = params[4]
    cand_opt_q = get_poly_curvilin_value_arr(cand_opt.curvilin, s, s_prev, s_f1, s_f)
    sspace = np.linspace(0,s_f)
    for l in range(len(lines_curvilin)):
        col = get_color(candidates[l],cand_opt)
        new_qspace = get_poly_curvilin_value_arr((candidates[l]).curvilin,sspace,s_prev,s_f1,s_f)
        (lines_curvilin[l]).set_xdata(sspace)
        (lines_curvilin[l]).set_ydata(new_qspace)
        (lines_curvilin[l]).set_color(col)
        #
        (lines_cart[l]).set_color(col)
        (lines_cart[l]).set_xdata((candidates[l]).cartesian[:,0])
        (lines_cart[l]).set_ydata((candidates[l]).cartesian[:,1])    
    figure.canvas.draw()
    figure.canvas.flush_events()
    # time.sleep(0.2)
        


