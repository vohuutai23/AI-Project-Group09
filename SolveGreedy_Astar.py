from SokobanState import Sokoban
from queue import PriorityQueue

def greedy_search(initial_state):
  visited = set()
  queue = PriorityQueue()
  queue.put((0, initial_state))
  cell_counter = 0 
  while not queue.empty():
      _, current_state = queue.get()

      if current_state.is_complete():
          return current_state, cell_counter

      for move in current_state.generate_moves():
          if tuple(map(tuple, move.state)) not in visited:
              visited.add(tuple(map(tuple, move.state)))
              heuristic_value = move.heuristic_value
              queue.put((heuristic_value,move))
              move.path = current_state.path + [move]
              cell_counter += 1 
  return None, cell_counter

  
def astar_search(initial_state):
    visited = set()

    queue = PriorityQueue()
    queue.put((0, initial_state))
    cell_counter = 0 
    while not queue.empty():
        _, current_state = queue.get()
    state_list = [(0, initial_state)]

    while state_list:
        state_list.sort(key=lambda x: x[0])
        _, current_state = state_list.pop(0)

        if current_state.is_complete():
            return current_state, cell_counter

        for move in current_state.generate_moves():
            if tuple(map(tuple, move.state)) not in visited:
                visited.add(tuple(map(tuple, move.state)))
                g_cost = current_state.cost_astar + 1
                heuristic_val = move.heuristic_value
                f_func = g_cost + heuristic_val
                state_list.append((f_func, move))
                current_state.cost_astar = g_cost
                move.path = current_state.path + [move]
                cell_counter += 1 
    return None, cell_counter


def hill_climbing(initial_state):
    visited = set()
    state_initial = [(initial_state)]

    while state_initial:
        stack = [state_initial.pop()]
        while stack:
            current_state = stack.pop()
            if current_state.is_complete():
                return current_state
            for move in current_state.generate_moves():
                if tuple(map(tuple, move.state)) not in visited:
                    visited.add(tuple(map(tuple, move.state)))
                    move.path = current_state.path + [move]
                    if move.heuristic_value <= current_state.heuristic_value:
                        stack.append(move)
                    else:
                        state_initial.append(move)

    return None

