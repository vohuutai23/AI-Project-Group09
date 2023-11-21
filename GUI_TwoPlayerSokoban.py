import pygame
import tkinter as tk
from tkinter import messagebox

import os
from tkinter import ttk
from PIL import Image, ImageTk
import time
from SokobanState import *
from SolveDFS_IDS import *
from SolveBFS_UCS import *
import time
from SolveGreedy_Astar import *

_ROOT = os.path.abspath(os.path.dirname(__file__))
FILE_MAP = "map/level6.txt"


def update_file_map(new_file_map):
    global FILE_MAP
    FILE_MAP = new_file_map


class Image(object):
    wall = os.path.join(_ROOT, 'images/wall.gif')
    box = os.path.join(_ROOT, 'images/box.gif')
    box_target = os.path.join(_ROOT, 'images/box_target.gif')
    box_on_target = os.path.join(_ROOT, 'images/box_on_target.gif')
    player = os.path.join(_ROOT, 'images/player.gif')
    player_on_target = os.path.join(_ROOT, 'images/player_on_target.gif')


class SokobanGame(tk.Tk):
    def __init__(self):

        super().__init__()

        self.check_use_algorithm = False

        #self.open_file_level(os.path.join(_ROOT, FILE_MAP))
        self.open_file_level_1(os.path.join(_ROOT, FILE_MAP))
        self.open_file_level_2(os.path.join(_ROOT, FILE_MAP))

        # Kích thước ô trong trò chơi (đơn vị pixel)
        self.CELL_SIZE = 100

        self.title("Sokoban")
        self.geometry(
            f"{len(self.GAME_MAP_1.state[0]) * self.CELL_SIZE + 300}x{len(self.GAME_MAP_1.state) * self.CELL_SIZE}")

        self.frame_player1 = tk.Frame(self)  # Tạo main frame
        self.frame_player1.pack(side="left")

        self.canvas_player1 = tk.Canvas(self.frame_player1, width=len(self.GAME_MAP_1.state[0]) * self.CELL_SIZE,
                                height=len(self.GAME_MAP_1.state) * self.CELL_SIZE, background='white')
        self.canvas_player1.pack(side="left")

        self.frame_player2 = tk.Frame(self)  # Tạo main frame
        self.frame_player2.pack(side="right")
        self.canvas_player2 = tk.Canvas(self.frame_player2, width=len(self.GAME_MAP_2.state[0]) * self.CELL_SIZE,
                                        height=len(self.GAME_MAP_2.state) * self.CELL_SIZE, background='white')
        self.canvas_player2.pack(side="right")
        self.images = {}
        self.step_counter = -1



        self.draw_game_map_1()
        self.draw_game_map_2()


    def open_file_level_1(self, filepath):
        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                lines = file.readlines()
            lines = [line.strip() for line in lines]

            self.GAME_MAP_1 = Sokoban(lines)
            for line in self.GAME_MAP_1.state:
                print(line)
        else:
            messagebox.showerror("Sorry", "Không tìm thấy file map level!!")
            self.GAME_MAP_1 = Sokoban([
                "0#####00",
                "#00000#0",
                "#00p00#0",
                "#00000#0",
                "#00b00#0",
                "#00g00#0",
                "#######0",
                "00000000"
            ])

    def open_file_level_2(self, filepath):
        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                lines = file.readlines()
            lines = [line.strip() for line in lines]

            self.GAME_MAP_2 = Sokoban(lines)
            for line in self.GAME_MAP_2.state:
                print(line)
        else:
            messagebox.showerror("Sorry", "Không tìm thấy file map level!!")
            self.GAME_MAP_2 = Sokoban([
                "0#####00",
                "#00000#0",
                "#00p00#0",
                "#00000#0",
                "#00b00#0",
                "#00g00#0",
                "#######0",
                "00000000"
            ])
    def draw_game_map_1(self):
        self.canvas_player1.delete("all")
        for y, row in enumerate(self.GAME_MAP_1.state):
            for x, cell in enumerate(row):
                x1, y1 = x * self.CELL_SIZE, y * self.CELL_SIZE
                x2, y2 = x1 + self.CELL_SIZE, y1 + self.CELL_SIZE

                image = None  # Biến để lưu trữ thể hiện của ImageTk.PhotoImage

                if cell == Level.wall:
                    if Image.wall not in self.images:  # Kiểm tra xem đã tạo thể hiện cho hình ảnh này chưa
                        self.images[Image.wall] = ImageTk.PhotoImage(file=Image.wall)
                    image = self.images[Image.wall]
                elif cell == Level.box:
                    if Image.box not in self.images:
                        self.images[Image.box] = ImageTk.PhotoImage(file=Image.box)
                    image = self.images[Image.box]
                elif cell == Level.box_target:
                    if Image.box_target not in self.images:
                        self.images[Image.box_target] = ImageTk.PhotoImage(file=Image.box_target)
                    image = self.images[Image.box_target]
                elif cell == Level.box_on_target:
                    if Image.box_on_target not in self.images:
                        self.images[Image.box_on_target] = ImageTk.PhotoImage(file=Image.box_on_target)
                    image = self.images[Image.box_on_target]
                elif cell == Level.player:

                    if Image.player not in self.images:
                        self.images[Image.player] = ImageTk.PhotoImage(file=Image.player)
                    image = self.images[Image.player]
                elif cell == Level.player_on_target:
                    if Image.player_on_target not in self.images:
                        self.images[Image.player_on_target] = ImageTk.PhotoImage(file=Image.player_on_target)
                    image = self.images[Image.player_on_target]

                if image:
                    self.canvas_player1.create_image(x1, y1, anchor="nw", image=image)
                    self.canvas_player1.image = image



        if self.GAME_MAP_1.is_complete():
            messagebox.showinfo("Congratulations", "You win !!")

    def draw_game_map_2(self):

        self.canvas_player2.delete("all")
        for y, row in enumerate(self.GAME_MAP_2.state):
            for x, cell in enumerate(row):
                x1, y1 = x * self.CELL_SIZE, y * self.CELL_SIZE
                x2, y2 = x1 + self.CELL_SIZE, y1 + self.CELL_SIZE

                image = None  # Biến để lưu trữ thể hiện của ImageTk.PhotoImage

                if cell == Level.wall:
                    if Image.wall not in self.images:  # Kiểm tra xem đã tạo thể hiện cho hình ảnh này chưa
                        self.images[Image.wall] = ImageTk.PhotoImage(file=Image.wall)
                    image = self.images[Image.wall]
                elif cell == Level.box:
                    if Image.box not in self.images:
                        self.images[Image.box] = ImageTk.PhotoImage(file=Image.box)
                    image = self.images[Image.box]
                elif cell == Level.box_target:
                    if Image.box_target not in self.images:
                        self.images[Image.box_target] = ImageTk.PhotoImage(file=Image.box_target)
                    image = self.images[Image.box_target]
                elif cell == Level.box_on_target:
                    if Image.box_on_target not in self.images:
                        self.images[Image.box_on_target] = ImageTk.PhotoImage(file=Image.box_on_target)
                    image = self.images[Image.box_on_target]
                elif cell == Level.player:

                    if Image.player not in self.images:
                        self.images[Image.player] = ImageTk.PhotoImage(file=Image.player)
                    image = self.images[Image.player]
                elif cell == Level.player_on_target:
                    if Image.player_on_target not in self.images:
                        self.images[Image.player_on_target] = ImageTk.PhotoImage(file=Image.player_on_target)
                    image = self.images[Image.player_on_target]

                if image:

                    self.canvas_player2.create_image(x1, y1, anchor="nw", image=image)
                    self.canvas_player2.image = image


        if self.GAME_MAP_2.is_complete():
            messagebox.showinfo("Congratulations", "You win !!")





def main():
    # a = "map/level11.txt"
    # FILE_MAP = map_link(a)

    game = SokobanGame()

    # def on_key(event):
    #     if event.keysym == "Up":
    #         game.GAME_MAP_1.move_player(0, -1, game)
    #     elif event.keysym == "Down":
    #         game.GAME_MAP_1.move_player(0, 1, game)
    #     elif event.keysym == "Left":
    #         game.GAME_MAP_1.move_player(-1, 0, game)
    #     elif event.keysym == "Right":
    #         game.GAME_MAP_1.move_player(1, 0, game)
    def on_key(event):
        # Xử lý đầu vào cho cả hai người chơi
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            if event.keysym == "Up":
                game.GAME_MAP_1.move_player_1(0, -1, game)
            elif event.keysym == "Down":
                game.GAME_MAP_1.move_player_1(0, 1, game)
            elif event.keysym == "Left":
                game.GAME_MAP_1.move_player_1(-1, 0, game)
            elif event.keysym == "Right":
                game.GAME_MAP_1.move_player_1(1, 0, game)
        elif event.keysym in ["w", "s", "a", "d"]:
            if event.keysym == "w":
                game.GAME_MAP_2.move_player_2(0, -1, game)
            elif event.keysym == "s":
                game.GAME_MAP_2.move_player_2(0, 1, game)
            elif event.keysym == "a":
                game.GAME_MAP_2.move_player_2(-1, 0, game)
            elif event.keysym == "d":
                game.GAME_MAP_2.move_player_2(1, 0, game)

    game.bind("<Key>", on_key)
    game.mainloop()


if __name__ == "__main__":
    main()