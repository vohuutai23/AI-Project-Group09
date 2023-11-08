import tkinter as tk
from tkinter import *


root = tk.Tk()
root.resizable(False, False)
root.title("Sokoban game")
root.geometry("800x500+500+100")
canvas = Canvas(root, height=500, width=800, bd=0, highlightthickness=1, relief="ridge")
canvas.place(x=0, y=0)
background_img = PhotoImage(file=f"images/background2.png")
background = canvas.create_image(400.0, 250.0, image=background_img)
#info = canvas.create_text(400.0, 100, text="SOKOBAN", fill="red", font=("Rockwell Extra Bold", int(80.0)))


def start_game():
    root.destroy()
    # Thực hiện các hành động cần thiết để bắt đầu trò chơi
    print("Game started!")
    import GUI_level_selection
    GUI_level_selection.main()

start_img = PhotoImage(file=f"images/start2.png")
start = Button(image=start_img, borderwidth=0, highlightthickness=0, relief="flat", command = start_game)
start.place(x=318, y=380, width=200, height=86)


info_img = PhotoImage(file=f"images/SOKOBAN.png")
info = canvas.create_image(400.0, 100.0, image=info_img)

# Danh sách chọn chế độ chơi
game_modes = ["1 Player", "Player VS Player", "AI VS AI", "Player VS AI"]
selected_mode = StringVar(value=game_modes[0])

# Label hiển thị chế độ chơi
mode_label = Label(root, textvariable=selected_mode, bg="#4392F1", fg="white", font=("Arial", 16))
mode_label.place(x=318, y=200, width=200, height=86)

# Nút "<" để di chuyển sang chế độ trước đó
def previous_mode():
    current_index = game_modes.index(selected_mode.get())
    previous_index = (current_index - 1) % len(game_modes)
    selected_mode.set(game_modes[previous_index])

previous_button = Button(root, text="<", command=previous_mode)
previous_button.place(x=250, y=200, width=50, height=86)

# Nút ">" để di chuyển sang chế độ kế tiếp
def next_mode():
    current_index = game_modes.index(selected_mode.get())
    next_index = (current_index + 1) % len(game_modes)
    selected_mode.set(game_modes[next_index])

next_button = Button(root, text=">", command=next_mode)
next_button.place(x=530, y=200, width=50, height=86)



root.mainloop()

