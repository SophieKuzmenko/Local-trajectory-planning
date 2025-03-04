#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 16:36:56 2024

@author: sofi
"""


"""
Verifying that the safety circles defined for the vehicle and the obstacle won't intersect, e.g. there won't be a colission
"""
def obstacle_collision_check(cand, obstacles,R_v):
    for obstacle in obstacles:
        if (circle_collision(cand.cartesian, obstacle.c, R_v,obstacle.r)):
            return False
    return True
        
            
        
def circle_collision(c1_arr, c2, r1,r2):
    for c1 in c1_arr:
        val = (c1[0]-c2[0])**2 + (c1[1] - c2[1])**2
        if val <= r1+r2:
            return True
    return False