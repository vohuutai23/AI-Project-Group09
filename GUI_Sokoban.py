# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 17:48:38 2023

@author: DELL
"""

import tkinter as tk
from tkinter import messagebox

class SokobanGame(tk.Tk):
    def __init__(self):
        super().__init__()
        # Bản đồ mẫu
        self.GAME_MAP = [
            "#######",
            "#00000#",
            "#00p00#",
            "#00000#",
            "#00b00#",
            "#00g00#",
            "#######"
        ]
        # Kích thước ô trong trò chơi (đơn vị pixel)
        self.CELL_SIZE = 100

        self.title("Sokoban")
        self.geometry(f"{len(self.GAME_MAP[0]) * self.CELL_SIZE}x{len(self.GAME_MAP) * self.CELL_SIZE}")

        self.canvas = tk.Canvas(self, width=len(self.GAME_MAP[0]) * self.CELL_SIZE, height=len(self.GAME_MAP) * self.CELL_SIZE)
        self.canvas.pack()
        for y, row in enumerate(self.GAME_MAP):
            for x, cell in enumerate(row):
                if cell == 'p' or cell == 'u':
                    self.player_pos = (x, y)
        self.draw_game_map()

    def draw_game_map(self):
        self.canvas.delete("all")

        for y, row in enumerate(self.GAME_MAP):
            for x, cell in enumerate(row):
                x1, y1 = x * self.CELL_SIZE, y * self.CELL_SIZE
                x2, y2 = x1 + self.CELL_SIZE, y1 + self.CELL_SIZE

                if cell == "#":
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="gray")
                elif cell == "p":
                    self.canvas.create_oval(x1, y1, x2, y2, fill="blue")
                elif cell == "b":
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="red")
                elif cell == "g":
                    self.canvas.create_oval(x1, y1, x2, y2, fill="yellow")
                elif cell == "u":
                    self.canvas.create_oval(x1, y1, x2, y2, fill="green")
                elif cell == "x":
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")

    def move_player(self, dx, dy):
        x, y = self.player_pos
        new_map = [list(row) for row in self.GAME_MAP]
        for row in self.GAME_MAP:
            print(row)
        print()
        cell = new_map[y][x]
        new_x, new_y = x + dx, y + dy
        new_cell = new_map[new_y][new_x]
        if new_cell == "#" :
            return  
        elif new_cell == "g":
            new_map[y][x] = '0'
            new_map[new_y][new_x] = 'u'
            self.player_pos = (new_x,new_y)
        elif new_cell == '0':
            if cell == 'p':
                new_map[y][x] = '0'
            else: 
                new_map[y][x] = 'g'
            new_map[new_y][new_x] = 'p'
            self.player_pos = (new_x,new_y)
        elif new_cell == 'b' or new_cell == 'x':
            new_x2, new_y2 = new_x + dx, new_y + dy
            new_cell_next = new_map[new_y2][new_x2]
            if new_cell_next == 'x' or new_cell_next == 'b' or new_cell_next == '#':
                return
            if cell == 'p':
                new_map[y][x] = '0'
            else: 
                new_map[y][x] = 'g'
            if new_cell == 'x':
                new_map[new_y][new_x] = 'u'
                self.player_pos = (new_x,new_y)
            else:
                new_map[new_y][new_x] = 'p'
                self.player_pos = (new_x,new_y)
            if new_cell_next == '0':
                new_map[new_y2][new_x2] = 'b'
            elif new_cell_next == 'g':
                new_map[new_y2][new_x2] = 'x'
                
        self.GAME_MAP = ["".join(r) for r in new_map]
        self.draw_game_map()
        if self.is_complete():
            messagebox.showinfo("Congratulations", "You win !!")
        
    def is_complete(self):
        for row in self.GAME_MAP:
            if 'b' in row:
                return False
        return True

def main():
    game = SokobanGame()

    def on_key(event):
        if event.keysym == "Up":
            game.move_player(0, -1)
        elif event.keysym == "Down":
            game.move_player(0, 1)
        elif event.keysym == "Left":
            game.move_player(-1, 0)
        elif event.keysym == "Right":
            game.move_player(1, 0)

    game.bind("<Key>", on_key)
    game.mainloop()

if __name__ == "__main__":
    main()