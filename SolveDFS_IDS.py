# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 15:50:01 2023

@author: DELL
"""

from SokobanState import *

def dfs_search(initial_state, MAX_DEPTH = 1000):
    stack = [(initial_state)]  # Stack để lưu trữ các trạng thái cần xem xét

    visited = set()  # Lưu trữ các trạng thái đã xem
    
    while stack:
        current_state = stack.pop()  # Lấy trạng thái hiện tại từ stack

        if current_state.is_complete():
            return current_state  # Nếu đạt được trạng thái mục tiêu, trả về kết quả
        
        if current_state.depth >= MAX_DEPTH: #giúp không bị treo máy
            continue
    
        # Sinh các trạng thái kế tiếp và thêm vào stack
        for move in self.generate_moves(current_state):
            if tuple(map(tuple, move.puzzle)) not in visited:
                stack.append(move)
                visited.add(tuple(map(tuple, move.puzzle))) 
                move.path = current_state.path + [move.puzzle]
    return None