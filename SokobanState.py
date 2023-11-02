# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 17:18:34 2023

@author: DELL
"""

class Sokoban:
    def __init__(self, sokoban, depth=0, path = [], cost = 0, heuristic = 0):
        self.state = sokoban  
        self.depth = depth 
        self.path = path
        self.cost = cost
        self.heuristic = heuristic
        
    def is_complete(self):
        for row in self.state:
            if 'b' in row:
                return False
        return True