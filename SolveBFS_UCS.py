# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 17:03:52 2023

@author: HOME
"""
import heapq
from SokobanState import *

def bfs_search(initial_state):
    queue = [initial_state]  
    visited = set()  
    
    while queue:
        current_state = queue.pop(0)  

        if current_state.is_complete():
            
            return current_state  
    
        # Sinh các trạng thái kế tiếp và thêm vào hàng đợi
        for move in current_state.generate_moves():
            if tuple(map(tuple, move.state)) not in visited:
                queue.append(move)
                visited.add(tuple(map(tuple, move.state))) 
                move.path = current_state.path + [move]
    return None

def ucs_search(initial_state):
    queue = [(0, initial_state)]  

    visited = set()  
    
    while queue:
        queue = sorted(queue, key=lambda x: x[0])  
        
        cost, current_state = queue.pop(0)  
        
        if current_state.is_complete():
            return current_state  
    
       
        for move in current_state.generate_moves():
            if tuple(map(tuple, move.state)) not in visited:
                new_cost = cost + 1  # Tính toán chi phí mới cho trạng thái kế tiếp
                queue.append((new_cost, move))
                visited.add(tuple(map(tuple, move.state))) 
                move.path = current_state.path + [move]
        print(cost)
    return None
