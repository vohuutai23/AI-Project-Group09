# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 17:18:34 2023

@author: DELL
"""

class Sokoban:
    def __init__(self, sokoban, depth=0, path = [], cost = 0):
        self.state = sokoban  
        self.depth = depth 
        self.path = path
        self.cost = cost