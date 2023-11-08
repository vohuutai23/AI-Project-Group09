# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 17:50:50 2023

@author: DELL
"""

import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import os
from GUI_Sokoban import main

root = tk.Tk()
root.title("Start Game")
root.geometry("500x500")

canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
canvas.pack()
_ROOT = os.path.abspath(os.path.dirname(__file__))
PNG_FILE = os.path.join(_ROOT, 'images/background.png')
PNG_FILE_START = os.path.join(_ROOT, 'images/start_game.png')
PNG_FILE_EXIT = os.path.join(_ROOT, 'images/exit.png')

# Chuyển đổi tệp PNG thành định dạng PGM hoặc GIF
image = Image.open(PNG_FILE)
image = image.convert("P")  # Chuyển đổi thành định dạng PGM (Portable Gray Map)

# Chuyển đổi thành PhotoImage
background_image = ImageTk.PhotoImage(image)

# Hiển thị hình ảnh nền
canvas.create_image(0, 0, image=background_image, anchor=tk.NW)

# Hàm để bắt đầu trò chơi khi nhấn nút "Start"
def start_game():
    root.destroy()
    # Thực hiện các hành động cần thiết để bắt đầu trò chơi
    print("Game started!")
    main()
   

image_start = tk.PhotoImage(file=PNG_FILE_START)
button_start = tk.Button(root, text="Start", image= image_start, command=start_game)
button_start.image = image_start
button_start_window = canvas.create_window(150, 250, window=button_start)  # Đặt vị trí của button trên canvas

image_exit = tk.PhotoImage(file=PNG_FILE_EXIT)
button_exit = tk.Button(root, text="Exit", image= image_exit, command=root.destroy)
button_start.image = image_start
button_exit_window = canvas.create_window(350, 250, window=button_exit)


root.mainloop()