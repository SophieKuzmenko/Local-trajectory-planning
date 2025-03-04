#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 16:28:00 2025

@author: sofi
"""
import numpy as np
import matplotlib.pyplot as plt
from testing_helpers import sub_mod_pi2

def discretize_path(ax, cand_opt, st_i, end_i):
    ind = st_i
    while ind <(end_i - 1):
        vect = cand_opt.cartesian[(ind+1),:] - cand_opt.cartesian[ind,:]
        ns = np.linspace(0,1,11)
        for s in ns:
            pos_v = cand_opt.cartesian[ind,:] + s*vect
            carh = ax.plot(pos_v[0], pos_v[1],"*k")
            plt.pause(0.03)
            c = carh.pop(0)
            c.remove()
            del c
        ind = ind + 1
        
def generate_obstacle(path_p):
    return np.array([path_p[0] + 1.2, path_p[1] - 1.2])  

"""

"""
# def get_q(p1, p2, p3):
#     dist = np.linalg.norm(p3 - p1)
#     alpha = get_segm_angle(p1, p3) - get_segm_angle(p1, p2)
#     return dist*np.sin(alpha)
def find_closest_segment_index(m, point):
  min_distance = float('inf')
  closest_segment_index = -1
  angle_tolerance = np.pi/2
  for i in range(m.shape[1]):
    # Calculate the distance from the point to the line segment
    angle_diff = sub_mod_pi2(point[2], get_segm_angle(m[0:2,i], m[0:2,(i+1)%m.shape[1]]))
   
    print([i,angle_diff])
    #angle_diff = np.degrees(angle_diff)
    if angle_diff <= angle_tolerance:
        distance = distance_point_to_line_segment(point, m[0:2,i], m[0:2,(i+1)%m.shape[1]])
        # e_angle = abs(point[2] - get_segm_angle(m[:,ind], m[:,(ind+1)%m.shape[1]]))
        # err = L1*distance + L2*e_angle
        # if (err < min_err):
        #print([i,distance, min_distance])
        #print([i,angle_diff,distance])
        if distance < min_distance:
            min_distance = distance
            closest_segment_index = i
  return closest_segment_index

def distance_point_to_line_segment(point, p1, p2):

  x0, y0,theta = point
  x1, y1 = p1
  x2, y2 = p2
  # Calculate the length of the line segment
  line_length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
  if line_length == 0.0:
    return np.sqrt((x0 - x1)**2 + (y0 - y1)**2)  # Point is the same as the line segment
  # Calculate parameters for the projection
  u = ((x0 - x1) * (x2 - x1) + (y0 - y1) * (y2 - y1)) / (line_length * line_length)
  # Clamp u to the range [0, 1] to ensure the projection is on the segment
  u = max(0, min(u, 1))
  # Calculate the projection point
  x = x1 + u * (x2 - x1)
  y = y1 + u * (y2 - y1)
  # Calculate the distance between the point and the projection point
  distance = np.sqrt((x0 - x) ** 2 + (y0 - y) ** 2)
  return distance

def get_projection_params(p1,p2,p3):
    dist = np.linalg.norm(p3-p1)
    alpha_bf = get_segm_angle(p1,p2)
    alpha = get_segm_angle(p1, p3) - alpha_bf
    lenp = np.cos(alpha)*dist# length of the projection vector
    q = dist*np.sin(alpha)
    x_p = p1[0] + np.cos(alpha_bf)*lenp
    y_p = p1[1] + np.sin(alpha_bf)*lenp
    proj = np.array([x_p,y_p])
    #print([q, np.linalg.norm(proj - p3)])
    return [proj, q]
def get_q(p1,p2,p3):
    dist = np.linalg.norm(p3-p1)
    alpha = get_segm_angle(p1, p3) - get_segm_angle(p1,p2)
    return abs(dist*np.sin(alpha))

def get_segm_angle(A,B):
    return np.arctan2((B[1] - A[1]),(B[0] - A[0]) ) 
   
