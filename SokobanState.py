# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 17:18:34 2023

@author: DELL
"""
from tkinter import messagebox

class Level(object):
    wall = '#'
    box = 'b'
    box_target = 'g'
    box_on_target = 'x'
    player = 'p'
    player_on_target = 'u'
    
class Sokoban:
    def __init__(self, sokoban, depth=0, path = [], cost = 0, heuristic = 0):
        self.state = sokoban  
        self.depth = depth 
        self.path = path
        self.cost = cost
        self.heuristic = heuristic
    
    def move_player(self, dx, dy, SokobanGame):
        x, y = SokobanGame.player_pos
        new_map = [list(row) for row in self.state]
        for row in self.state:
            print(row)
        print()
        cell = new_map[y][x]
        new_x, new_y = x + dx, y + dy
        new_cell = new_map[new_y][new_x]
        if new_cell == Level.wall:
            return  
        
        elif new_cell == Level.box_target:
            if cell == Level.player_on_target:
                new_map[y][x] = Level.box_target
            elif cell == Level.player:
                new_map[y][x] = '0'
            new_map[new_y][new_x] = Level.player_on_target
            SokobanGame.player_pos = (new_x, new_y)
            
        elif new_cell == '0':
            if cell == Level.player:
                new_map[y][x] = '0'
            else: 
                new_map[y][x] = Level.box_target
            new_map[new_y][new_x] = Level.player
            SokobanGame.player_pos = (new_x, new_y)
            
        elif new_cell == Level.box or new_cell == Level.box_on_target:
            new_x2, new_y2 = new_x + dx, new_y + dy
            new_cell_next = new_map[new_y2][new_x2]
            if new_cell_next == Level.box_on_target or new_cell_next == Level.box or new_cell_next == Level.wall:
                return
            if cell == Level.player:
                new_map[y][x] = '0'
            else: 
                new_map[y][x] = Level.box_target
            if new_cell == Level.box_on_target:
                new_map[new_y][new_x] = Level.player_on_target
                SokobanGame.player_pos = (new_x, new_y)
            else:
                new_map[new_y][new_x] = Level.player
                SokobanGame.player_pos = (new_x, new_y)
            if new_cell_next == '0':
                new_map[new_y2][new_x2] = Level.box
            elif new_cell_next == Level.box_target:
                new_map[new_y2][new_x2] = Level.box_on_target
            
        self.state = ["".join(r) for r in new_map]
        SokobanGame.draw_game_map()
        if self.is_complete():
            messagebox.showinfo("Congratulations", "You win !!")
        
    def is_complete(self):
        for row in self.state:
            if 'b' in row:
                return False
        return True
    
        