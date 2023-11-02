
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from tkinter import ttk
from SokobanState import *

_ROOT = os.path.abspath(os.path.dirname(__file__))
class Level(object):
    wall = '#'
    box = 'b'
    box_target = 'g'
    box_on_target = 'x'
    player = 'p'
    player_on_target = 'u'


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
        self.open_file_level(os.path.join(_ROOT, "map/level6.txt"))
        # Kích thước ô trong trò chơi (đơn vị pixel)
        self.CELL_SIZE = 100

        self.title("Sokoban")
        self.geometry(f"{len(self.GAME_MAP.state[0]) * self.CELL_SIZE + 300}x{len(self.GAME_MAP.state) * self.CELL_SIZE}")

        self.main_frame = tk.Frame(self)  # Tạo main frame
        self.main_frame.pack(side="left")

        self.canvas = tk.Canvas(self.main_frame, width=len(self.GAME_MAP.state[0]) * self.CELL_SIZE, height=len(self.GAME_MAP.state) * self.CELL_SIZE, background='white')
        self.canvas.pack(side="left")

        self.images = {}
        self.draw_game_map()

        tk.Label(self.main_frame,text="SUPPORT", fg = "black" , relief = tk.SUNKEN, font = ("Times", 14, "bold"), background= "white", borderwidth = 1).pack(side="top")
        tk.Label(self.main_frame,text="---------").pack(side="top")
        self.restart_button = tk.Button(self.main_frame, text = "Restart", font = ("Times", 12, "bold"), borderwidth = 3, width = 10, height = 2, background = "pink", fg = "black", command = self.restart_game)
        self.restart_button.pack(side="top")
        
        tk.Label(self.main_frame,text="---------").pack(side="top")
        self.undo_button = tk.Button(self.main_frame, text="Undo", font = ("Times", 12, "bold"), borderwidth = 3, width = 10, height = 2, background = "yellow", fg = "black", command=self.undo_move)
        self.undo_button.pack(side="top")
        
        tk.Label(self.main_frame,text="---------").pack(side="top")
        lblLevel = tk.Label(self.main_frame, text = "LEVEL", font = ("Times", 10, "bold"))
        lblLevel.pack(side="top")
        n = tk.StringVar()
        self.choosenLevel = ttk.Combobox(self.main_frame, width = 15, textvariable = n, state="readonly")
        levels =[]
        for i in range(1,16):
            levels.append("level{}".format(i))
        self.choosenLevel['values'] = tuple(levels)
        self.choosenLevel.pack(side="top")
        self.choosenLevel.current(0)
        self.choosenLevel.bind("<<ComboboxSelected>>", self.on_level_select)

        self.algorithms_frame = tk.Frame(self)
        self.algorithms_frame.pack(side="top")
        
        tk.Label(self.algorithms_frame,text="ALGORITHMS", fg = "black" , relief = tk.SUNKEN, font = ("Times", 14, "bold"), background= "white", borderwidth = 1).pack(side="top")
        tk.Label(self.algorithms_frame,text="---------").pack(side="top")
        self.bfs_button = tk.Button(self.algorithms_frame, text="BFS", font = ("Times", 12, "bold"), borderwidth = 3, width = 10, height = 2, background = "green", fg = "white", command=self.solve_with_bfs)
        self.bfs_button.pack(side="top")
        tk.Label(self.algorithms_frame,text="---------").pack(side="top")
        self.dfs_button = tk.Button(self.algorithms_frame, text="DFS", font = ("Times", 12, "bold"), borderwidth = 3, width = 10, height = 2, background = "black", fg = "white", command=self.solve_with_dfs)
        self.dfs_button.pack(side="top")
        tk.Label(self.algorithms_frame,text="---------").pack(side="top")
        self.ucs_button = tk.Button(self.algorithms_frame, text="UCS", font = ("Times", 12, "bold"), borderwidth = 3, width = 10, height = 2, background = "red", fg = "white", command=self.solve_with_ucs)
        self.ucs_button.pack(side="top")
        tk.Label(self.algorithms_frame,text="---------").pack(side="top")
        self.ids_button = tk.Button(self.algorithms_frame, text="IDS", font = ("Times", 12, "bold"), borderwidth = 3, width = 10, height = 2, background = "brown", fg = "white", command=self.solve_with_ids)
        self.ids_button.pack(side="top")
        tk.Label(self.algorithms_frame,text="---------").pack(side="top")
        self.greedy_button = tk.Button(self.algorithms_frame, text="Greedy Search", font = ("Times", 12, "bold"), borderwidth = 3, width = 10, height = 2, background = "orange", fg = "white", command=self.solve_with_greedy)
        self.greedy_button.pack(side="top")
        tk.Label(self.algorithms_frame,text="---------").pack(side="top")
        self.a_star_button = tk.Button(self.algorithms_frame, text="A Star", font = ("Times", 12, "bold"), borderwidth = 3, width = 10, height = 2, background = "blue", fg = "white", command=self.solve_with_a_star)
        self.a_star_button.pack(side="top")
        
    def on_level_select(self,event):
        self.focus_set()
        self.open_file_level(os.path.join(_ROOT, "map/{}.txt".format(self.choosenLevel.get())))
        self.draw_game_map()
        
    def open_file_level(self,filepath):
        if os.path.exists(filepath) :
            with open(filepath, "r") as file:
                lines = file.readlines()
            lines = [line.strip() for line in lines]
            
            self.GAME_MAP = Sokoban(lines)
            for line in self.GAME_MAP.state:
                print(line) 
        else:
            messagebox.showerror("Sorry","Không tìm thấy file map level!!")
            self.GAME_MAP = Sokoban([
                "0#####0",
                "#00000#",
                "#00p00#",
                "#00000#",
                "#00b00#",
                "#00g00#",
                "#######"
            ])
        
    def draw_game_map(self):
        for y, row in enumerate(self.GAME_MAP.state):
            for x, cell in enumerate(row):
                if cell == Level.player or cell == Level.player_on_target:
                    self.player_pos = (x, y)
        self.canvas.delete("all")

        for y, row in enumerate(self.GAME_MAP.state):
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
                    self.canvas.create_image(x1, y1, anchor="nw", image=image)
                    self.canvas.image = image

        self.canvas.pack()
                
             
    def move_player(self, dx, dy):
        x, y = self.player_pos
        new_map = [list(row) for row in self.GAME_MAP.state]
        for row in self.GAME_MAP.state:
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
            self.player_pos = (new_x, new_y)
            
        elif new_cell == '0':
            if cell == Level.player:
                new_map[y][x] = '0'
            else: 
                new_map[y][x] = Level.box_target
            new_map[new_y][new_x] = Level.player
            self.player_pos = (new_x, new_y)
            
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
                self.player_pos = (new_x, new_y)
            else:
                new_map[new_y][new_x] = Level.player
                self.player_pos = (new_x, new_y)
            if new_cell_next == '0':
                new_map[new_y2][new_x2] = Level.box
            elif new_cell_next == Level.box_target:
                new_map[new_y2][new_x2] = Level.box_on_target
            
        self.GAME_MAP.state = ["".join(r) for r in new_map]
        self.draw_game_map()
        if self.GAME_MAP.is_complete():
            messagebox.showinfo("Congratulations", "You win !!")

    def restart_game(self):
        # Implement code to restart the game here
        pass

    def undo_move(self):
        # Implement code to undo the last move here
        pass

    def solve_with_bfs(self):
        # Implement code to solve the game with BFS algorithm here
        pass

    def solve_with_dfs(self):
        # Implement code to solve the game with DFS algorithm here
        pass

    def solve_with_ucs(self):
        # Implement code to solve the game with UCS algorithm here
        pass

    def solve_with_ids(self):
        # Implement code to solve the game with IDS algorithm here
        pass

    def solve_with_greedy(self):
        # Implement code to solve the game with Greedy Search algorithm here
        pass

    def solve_with_a_star(self):
        # Implement code to solve the game with A Star algorithm here
        pass
    
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