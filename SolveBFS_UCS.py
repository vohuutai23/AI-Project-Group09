# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 17:03:52 2023

@author: HOME
"""
import heapq
from SokobanState import *

def bfs_search(initial_state):
    queue = [initial_state]  # Hàng đợi để lưu trữ các trạng thái cần xem xét

    visited = set()  # Lưu trữ các trạng thái đã xem
    
    while queue:
        current_state = queue.pop(0)  # Lấy trạng thái hiện tại từ hàng đợi

        if current_state.is_complete():
            
            return current_state  # Nếu đạt được trạng thái mục tiêu, trả về kết quả
    
        # Sinh các trạng thái kế tiếp và thêm vào hàng đợi
        for move in current_state.generate_moves():
            if tuple(map(tuple, move.state)) not in visited:
                queue.append(move)
                visited.add(tuple(map(tuple, move.state))) 
                move.path = current_state.path + [move]
    return None

def ucs_search(initial_state):
    queue = [(0, initial_state)]  # Danh sách để lưu trữ các trạng thái cần xem xét

    visited = set()  # Lưu trữ các trạng thái đã xem
    
    while queue:
        queue = sorted(queue, key=lambda x: x[0])  # Sắp xếp danh sách theo chi phí
        
        cost, current_state = queue.pop(0)  # Lấy trạng thái hiện tại từ đầu danh sách
        
        if current_state.is_complete():
            return current_state  # Nếu đạt được trạng thái mục tiêu, trả về kết quả
    
        # Sinh các trạng thái kế tiếp và thêm vào danh sách
        for move in current_state.generate_moves():
            if tuple(map(tuple, move.state)) not in visited:
                new_cost = cost + 1  # Tính toán chi phí mới cho trạng thái kế tiếp
                queue.append((new_cost, move))
                visited.add(tuple(map(tuple, move.state))) 
                move.path = current_state.path + [move]
        print(cost)
    return None