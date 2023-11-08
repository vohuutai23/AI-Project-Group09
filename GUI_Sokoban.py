
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

        self.open_file_level(os.path.join(_ROOT, FILE_MAP))
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

        # Count steps and times
        self.step_time_frame = tk.Frame(self)
        self.step_time_frame.pack(side="bottom")
        self.step_label = tk.Label(self.step_time_frame, text="Steps: 0", font=("Times", 12, "bold"), background="white", anchor="center")
        self.step_label.pack(side="top")
        self.time_label = tk.Label(self.step_time_frame, text="Time: 0.00 seconds", font=("Times", 12, "bold"), background="white", anchor="center")
        self.time_label.pack(side="top")

    def update_gui_info(self, step_counter, elapsed_time):
        self.step_label.config(text=f"Steps: {step_counter}")
        self.time_label.config(text=f"Time: {elapsed_time:.2f} seconds")
        self.update()
        
    def on_level_select(self,event):
        global FILE_MAP
        FILE_MAP = "map/{}.txt".format(self.choosenLevel.get())
        self.focus_set()
        self.open_file_level(os.path.join(_ROOT, FILE_MAP))
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
        self.update()
        
        if self.GAME_MAP.is_complete():
            messagebox.showinfo("Congratulations", "You win !!")

    def restart_game(self):
        global FILE_MAP
        self.open_file_level(os.path.join(_ROOT, FILE_MAP))
        self.draw_game_map()
        self.check_use_algorithm = False
        
    def undo_move(self):
        if self.GAME_MAP.stack:
            new_state = self.GAME_MAP.stack.pop()
            self.GAME_MAP = Sokoban(sokoban = new_state, stack = self.GAME_MAP.stack)
            self.draw_game_map()


    def solve_with_bfs(self):
        self.step_counter = 0
        if self.check_use_algorithm == True:
            messagebox.showwarning("Restart","You need press the RESTART button!")
            return
        self.start_time = time.time()
        # self.start_update_time_thread()
        result = bfs_search(self.GAME_MAP)
        if result == None:
            messagebox.showinfo("Problem","Don't find the path!")
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        # self.time_counter = self.stop_update_time_thread()
        print("PATH")
        for sokoban in result.path:
            self.GAME_MAP = sokoban
            self.step_counter += 1
            self.update_gui_info(self.step_counter,elapsed_time)
            self.draw_game_map()
            for row in sokoban.state:
                print(row)
            print()
            time.sleep(0.1)
        self.check_use_algorithm = True
        # self.update_gui_info(self.step_counter, elapsed_time)

    # def solve_with_bfs(self):
    #     step_counter = 0
    #     # self.restart_game()
    #     if self.check_use_algorithm == True:
    #         messagebox.showwarning("Restart","You need press the RESTART button!")
    #         return
    #     result = bfs_search(self.GAME_MAP)
    #     if result == None:
    #         messagebox.showinfo("Problem","Don't find the path!")
    #     print("PATH")
    #     start_time = time.time()
    #     # self.start_update_time_thread(start_time)
    #     for sokoban in result.path:
    #         self.GAME_MAP = sokoban
    #         step_counter += 1
    #         elapsed_time = time.time() - start_time
    #         self.update_gui_info(step_counter, elapsed_time)
    #         self.draw_game_map()
    #         for row in sokoban.state:
    #             print(row)
    #         print()
    #         time.sleep(0.1)
    #     # self.stop_update_time_thread()
    #     self.check_use_algorithm = True
    def solve_with_dfs(self):
        self.step_counter = 0
        if self.check_use_algorithm == True:
            messagebox.showwarning("Restart","You need press the RESTART button!")
            return
        self.start_time = time.time()
        # self.start_update_time_thread()
        result = dfs_search(self.GAME_MAP)
        if result == None:
            messagebox.showinfo("Problem","Don't find the path!")
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        # self.time_counter = self.stop_update_time_thread()
        print("PATH")
        for sokoban in result.path:
            self.GAME_MAP = sokoban
            self.step_counter += 1
            self.update_gui_info(self.step_counter,elapsed_time)
            self.draw_game_map()
            for row in sokoban.state:
                print(row)
            print()
            time.sleep(0.1)
        self.check_use_algorithm = True

    def solve_with_ucs(self):
        self.step_counter = 0
        if self.check_use_algorithm == True:
            messagebox.showwarning("Restart","You need press the RESTART button!")
            return
        self.start_time = time.time()
        # self.start_update_time_thread()
        result = ucs_search(self.GAME_MAP)
        if result == None:
            messagebox.showinfo("Problem","Don't find the path!")
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        # self.time_counter = self.stop_update_time_thread()
        print("PATH")
        for sokoban in result.path:
            self.GAME_MAP = sokoban
            self.step_counter += 1
            self.update_gui_info(self.step_counter,elapsed_time)
            self.draw_game_map()
            for row in sokoban.state:
                print(row)
            print()
            time.sleep(0.1)
        self.check_use_algorithm = True


    def solve_with_ids(self):
        self.step_counter = 0
        if self.check_use_algorithm == True:
            messagebox.showwarning("Restart","You need press the RESTART button!")
            return
        self.start_time = time.time()
        # self.start_update_time_thread()
        result = ids_search(self.GAME_MAP,5)
        if result == None:
            messagebox.showinfo("Problem","Don't find the path!")
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        # self.time_counter = self.stop_update_time_thread()
        print("PATH")
        for sokoban in result.path:
            self.GAME_MAP = sokoban
            self.step_counter += 1
            self.update_gui_info(self.step_counter,elapsed_time)
            self.draw_game_map()
            for row in sokoban.state:
                print(row)
            print()
            time.sleep(0.1)
        self.check_use_algorithm = True

    def solve_with_greedy(self):
        self.step_counter = 0
        if self.check_use_algorithm == True:
            messagebox.showwarning("Restart","You need press the RESTART button!")
            return
        self.start_time = time.time()
        # self.start_update_time_thread()
        result = greedy_search(self.GAME_MAP)
        if result == None:
            messagebox.showinfo("Problem","Don't find the path!")
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        # self.time_counter = self.stop_update_time_thread()
        print("PATH")
        for sokoban in result.path:
            self.GAME_MAP = sokoban
            self.step_counter += 1
            self.update_gui_info(self.step_counter,elapsed_time)
            self.draw_game_map()
            for row in sokoban.state:
                print(row)
            print()
            time.sleep(0.1)
        self.check_use_algorithm = True

    def solve_with_a_star(self):
        self.step_counter = 0
        if self.check_use_algorithm == True:
            messagebox.showwarning("Restart","You need press the RESTART button!")
            return
        self.start_time = time.time()
        # self.start_update_time_thread()
        result = astar_search(self.GAME_MAP)
        if result == None:
            messagebox.showinfo("Problem","Don't find the path!")
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        # self.time_counter = self.stop_update_time_thread()
        print("PATH")
        for sokoban in result.path:
            self.GAME_MAP = sokoban
            self.step_counter += 1
            self.update_gui_info(self.step_counter,elapsed_time)
            self.draw_game_map()
            for row in sokoban.state:
                print(row)
            print()
            time.sleep(0.1)
        self.check_use_algorithm = True

    
def main():
    
    #a = "map/level11.txt"
    #FILE_MAP = map_link(a)
    
    game = SokobanGame()

    def on_key(event):
        if event.keysym == "Up":
            game.GAME_MAP.move_player(0, -1, game)
        elif event.keysym == "Down":
            game.GAME_MAP.move_player(0, 1, game)
        elif event.keysym == "Left":
            game.GAME_MAP.move_player(-1, 0, game)
        elif event.keysym == "Right":
            game.GAME_MAP.move_player(1, 0, game)
        
    
    game.bind("<Key>", on_key)
    game.mainloop()

if __name__ == "__main__":
    main()