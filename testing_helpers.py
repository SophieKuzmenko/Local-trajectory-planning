#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 17:44:45 2025

@author: sofi
"""
from numpy import sin,cos
import numpy as np
import matplotlib.pyplot as plt

def draw_car(fig, x,  color='b'):
    #Affiche un motif de voiture avec des roues
    #fig = handle de la figure
    #x = état (x, y, theta, v, delta)
    #color = permet de changer la couleur de la voiture
    #retourne les handles qui permettent d'effacer la voiture
    
    #Chassis en coordonnées homogènes dans le repère véhicule
    M=np.array([
        [-1,  0,  0,  0,  3,  3,  3,  4,  4.7,  5,   5,   4.7, 4, 3, 3, 3, 0, 0, 0, -1, -1],
        [-2, -2, -3, -2, -2, -3, -2, -2, -1.5, -0.5, 0.5, 1.5, 2, 2, 3, 2, 2, 3, 2,  2, -2],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
    
    #transformation homogène 2D pour transformer tous les points du chassis
    #dans le repère de travail
    T=np.array([
        [np.cos(x[2]), -np.sin(x[2]), x[0]],
        [np.sin(x[2]), np.cos(x[2]) , x[1]],
        [0             , 0              , 1]])
    #M=T.dot(M)
    M=T@M
    h1=fig.plot(M[0], M[1], color)
    
    #Motif d'une roue
    Roue=np.array([[-0.7, 0.7], [0, 0], [1, 1]])  
    #on oriente les roues de devant avec le même angle que la roue virtuelle 
    #i.e. on neglige la contrainte d'Ackermann
    
    Havd=np.array([
        [np.cos(x[4]),-np.sin(x[4]), 3], 
        [np.sin(x[4]), np.cos(x[4]),-3], 
        [0           , 0           , 1]])
    Ravd=T@Havd@Roue
    h2= fig.plot(Ravd[0,:],Ravd[1,:],color)#set(h2,'LineWidth',3);
    
    Havg=np.array([
        [np.cos(x[4]),-np.sin(x[4]), 3], #x[4] est l'angle au volant
        [np.sin(x[4]), np.cos(x[4]), 3], 
        [0           , 0           , 1]])
    Ravg=T@Havg@Roue
    h3= fig.plot(Ravg[0,:],Ravg[1,:],color)#set(h3,'LineWidth',3);
          
    #pour les roues arrières, c'est une simple translation
    Rard=T@np.array([[1, 0, 0], [0, 1, -3], [0, 0, 1]])@Roue
    h4= fig.plot(Rard[0,:],Rard[1,:],color)
    
    Rarg=T@np.array([[1, 0, 0], [0, 1,  3], [0, 0, 1]])@Roue
    h5= fig.plot(Rarg[0,:],Rarg[1,:],color)
    
    h=[h1, h2, h3, h4, h5]

    
    return h   
 
def ecart_pente_frenet(A,B,x):
    #Calcule :
    #   - e = ecart lateral signe
    #   - p = pente signee du segment [AB] (angle alpha)
    #En entree, on passe les deux points A et B et la position x de la
    #voiture
    #Le repere de Frenet a le point A pour origine et B definit l'axe x
    
    M = x[0:2]#position 
    xa=A[0]
    ya=A[1]
    xb=B[0]
    yb=B[1]
    alpha=np.arctan2((yb-ya),(xb-xa))
    #mat homogene
    O_T_A=np.array([
        [np.cos(alpha), -np.sin(alpha), xa],
        [np.sin(alpha),  np.cos(alpha), ya],
        [0            ,    0          ,  1]])
    #dans RA (repere de frenet)
    A_M = np.dot(np.linalg.inv(O_T_A), np.append(M, np.array([1])))
    axm=A_M[0]
    aym=A_M[1]
    
    A_B = np.dot(np.linalg.inv(O_T_A), np.append(B, np.array([1])))
    axb=A_B[0]
#    ayb=A_B[1]
    
    if (axm<0):
        e=np.sign(aym)*np.linalg.norm(A-M)
    elif (axm>axb):
        e=np.sign(aym)*np.linalg.norm(B-M)
    else:
        e=aym

    p=alpha
    
    return e,p

def sub_mod_pi2(x,y):
#pour 2 angles passes en parametre, calcule l'ecart e=x-y 
#retourne une valeur entre -pi et pi
#fct utile pour calculer des ecarts angulaires dans des commandes 
#car un ecart angulaire de commande doit rester petit

    if (x>=y):
        while np.abs(x-y)>np.pi:
            x=x-2*np.pi
    else:
        while np.abs(x-y)>np.pi:
            y=y-2*np.pi
    return x-y

def fxy(x, delta, v, L): # delta influences the steering direction, the radius of the turn
    x_dot = v*cos(delta)*cos(x[2])
    y_dot = v*cos(delta)*sin(x[2])
    theta_dot = v*sin(delta)/L
    return np.array([x_dot,y_dot,theta_dot])