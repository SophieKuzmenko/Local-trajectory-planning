#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 14:58:37 2024

@author: sofi
"""
import numpy as np

def calculate_angle_of_the_path(A):
  """
  Function to calculate the angle between the tangent to a curve at a given point and the x-axis.
  Outputs the angle in radians
  """
  x = A[0]
  y = A[1]
  r = A[2]
  slope = 1 / r
  angle = np.arctan(slope)
  # Adjust the angle based on the quadrant to get the correct angle relative to the x-axis
  if x < 0 and y > 0:  # quadrant 2
    angle += np.pi
  elif x < 0 and y < 0:  # quadrant 3
    angle += np.pi
  elif x > 0 and y < 0:  # quadrant 4
    angle += 2 * np.pi

  return angle
