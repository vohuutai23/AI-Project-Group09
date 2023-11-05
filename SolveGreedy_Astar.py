from SokobanState import Sokoban
from queue import PriorityQueue

def greedy_search(initial_state):
        visited = set()
        queue = PriorityQueue()
        queue.put((0, initial_state))

        while not queue.empty():
            _, current_state = queue.get()

            if current_state.is_complete():
                return current_state

            for move in current_state.generate_moves():
                if tuple(map(tuple, move.state)) not in visited:
                    visited.add(tuple(map(tuple, move.state)))
                    heuristic_value = move.heuristic_value
                    queue.put((heuristic_value,move))
                    move.path = current_state.path + [move]
        return None

def astar_search(initial_state):
    visited = set()
    queue = PriorityQueue()
    queue.put((0, initial_state))

    while not queue.empty():
        _, current_state = queue.get()

        if current_state.is_complete():
            return current_state

        for move in current_state.generate_moves():
            if tuple(map(tuple, move.state)) not in visited:
                visited.add(tuple(map(tuple, move.state)))
                g_cost = current_state.cost + 1
                f_cost = g_cost + move.heuristic_value  # Tổng chi phí di chuyển và heuristic
                queue.put((f_cost, move))
                move.cost = g_cost  # Cập nhật chi phí di chuyển
                move.path = current_state.path + [move]

    return None