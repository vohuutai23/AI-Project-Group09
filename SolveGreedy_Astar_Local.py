from SokobanState import *
from queue import PriorityQueue
from collections import deque


def greedy_search(initial_state):
    visited = set()
    stack = [(0, initial_state)]
    cell_counter = 0
    while stack:
        stack.sort(key=lambda x: x[0])
        # for st in state_list:
        #     print(st[0])
        _, current_state = stack.pop(0)

        if current_state.is_complete():
            return current_state, cell_counter

        for move in current_state.generate_moves():
            if tuple(map(tuple, move.state)) not in visited:
                cell_counter += 1
                visited.add(tuple(map(tuple, move.state)))
                heuristic_val = move.heuristic_value
                stack.append((heuristic_val, move))
                move.path = current_state.path + [move]

    return None, cell_counter


def astar_search(initial_state):
    visited = set()
    state_list = [(0,0, initial_state)]
    cell_counter = 0
    while state_list:
        state_list.sort(key=lambda x: x[0])
        f_star, cost, current_state = state_list.pop(0)

        if current_state.is_complete():
            return current_state, cell_counter

        for move in current_state.generate_moves():
            if tuple(map(tuple, move.state)) not in visited:
                cell_counter += 1
                visited.add(tuple(map(tuple, move.state)))
                g_cost = cost + calculate_move_cost(move, current_state)
                h_heuris = move.heuristic_value
                f_count = g_cost + h_heuris
                state_list.append((f_count,g_cost, move))
                move.path = current_state.path + [move]

    return None, cell_counter

def hill_climbing(initial_state):
    stack = [(initial_state)]  # Stack để lưu trữ các trạng thái cần xem xét

    visited = set()  # Lưu trữ các trạng thái đã xem
    cell_counter = 0
    while stack:
        current_state = stack.pop()  # Lấy trạng thái hiện tại từ stack

        if current_state.is_complete():
            return current_state, cell_counter  # Nếu đạt được trạng thái mục tiêu, trả về kết quả

        # Sinh các trạng thái kế tiếp và thêm vào stack
        for move in current_state.generate_moves():
            if tuple(map(tuple, move.state)) not in visited:
                visited.add(tuple(map(tuple, move.state)))
                if move.heuristic_value < current_state.heuristic_value:
                    stack.append(move)
                    move.path = current_state.path + [move]
                cell_counter += 1
    return None, cell_counter

# def hill_climbing(initial_state):
#     visited = set()
#     state_initial = [(initial_state)]
#     cell_counter = 0
#     while state_initial:
#         stack = [state_initial.pop()]
#         while stack:
#             current_state = stack.pop()
#             if current_state.is_complete():
#                 return current_state, cell_counter
#             for move in current_state.generate_moves():
#                 if tuple(map(tuple, move.state)) not in visited:
#                     cell_counter += 1
#                     visited.add(tuple(map(tuple, move.state)))
#                     move.path = current_state.path + [move]
#                     if move.heuristic_value <= current_state.heuristic_value:
#                         stack.append(move)
#                     else:
#                         state_initial.append(move)
#
#     return None, cell_counter
# def hill_climbing(initial_state):
#     current_state = initial_state
#     visited = set()
#     cell_counter = 0
#
#     while True:
#         moves = current_state.generate_moves()
#         visited.add(tuple(map(tuple, current_state.state)))
#
#         next_state = None
#         best_heuristic = current_state.heuristic_value
#
#         for move in moves:
#             if tuple(map(tuple, move.state)) not in visited:
#                 if move.heuristic_value < best_heuristic:
#                     best_heuristic = move.heuristic_value
#                     next_state = move
#
#         if next_state is None or current_state.is_complete():
#             # Không có trạng thái nào tốt hơn hoặc đã đạt trạng thái hoàn thành
#             return current_state, cell_counter
#
#         current_state = next_state
#         cell_counter += 1
#         current_state.path.append(next_state)  # Lưu trữ bước di chuyển
#
#     # Nếu quá trình lặp không tìm thấy trạng thái hoàn thành, trả về trạng thái hiện tại và số ô đã thăm
#     return current_state, cell_counter

def BeamSearch(initial_state, k):
    queue = deque([initial_state])  
  
    visited = set()  # Lưu trữ các trạng thái đã xem
    visited.add(tuple(map(tuple, initial_state.state)))
    cell_counter = 0
    while queue:
        k_loop = k
        current_state = queue.popleft()  
  
        if current_state.is_complete():
            return current_state, cell_counter  # Nếu đạt được trạng thái mục tiêu, trả về kết quả
        
        schedule = current_state.generate_moves()
        schedule = sorted(schedule , key=lambda x: x.heuristic_value, reverse=True)
        # Sinh các trạng thái kế tiếp và thêm vào queue
        for move in schedule:
            if tuple(map(tuple, move.state)) not in visited:
                visited.add(tuple(map(tuple, move.state))) 
                move.path = current_state.path + [move]
                cell_counter += 1
                if k_loop > 0:
                    queue.append(move)
                    k_loop = k_loop - 1

    return None, cell_counter


def calculate_move_cost(new_state, current_state):
    base_cost = 1  # Chi phí cơ bản cho mỗi bước di chuyển
    box_move_cost = 2  # Chi phí khi di chuyển hộp

    # Kiểm tra xem có di chuyển hộp hay không
    if moved_box(new_state, current_state):
        return base_cost + box_move_cost
    else:
        return base_cost

def moved_box(new_state, current_state):
    # Hàm này kiểm tra xem có hộp nào được di chuyển giữa hai trạng thái hay không
    new_player_pos = new_state.player_pos
    old_player_pos = current_state.player_pos

    # Lấy vị trí giữa người chơi cũ và mới
    #between_pos = (old_player_pos[0] + (new_player_pos[0] - old_player_pos[0]) // 2, old_player_pos[1] + (new_player_pos[1] - old_player_pos[1]) // 2)
    if old_player_pos != new_player_pos:
    # Kiểm tra xem vị trí giữa có phải là vị trí của hộp trong trạng thái cũ hay không
        if current_state.state[new_player_pos[1]][new_player_pos[0]] in [Level.box, Level.box_on_target]:
        #if current_state.state[between_pos[1]][between_pos[0]] in [Level.box, Level.box_on_target]:
            return True
    return False