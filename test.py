from tkinter import Tk
import tkinter as tk
import controls
import os


#----------------------------------------------------------------


# ROOT
window_width = 800
window_height = 600
background_color = "light grey"
root = Tk()
root.title("WRYName")
canvas = tk.Canvas(root, width=window_width, height=window_height)
canvas.pack()

menu_frame = controls.Frame(root)
menu_frame.place(relwidth=1, relheight=.075)
menu_frame.set_background("gray")

body_frame = controls.Frame(root)
body_frame.place(rely=.075, relwidth=1, relheight=.925)
body_frame.set_background("light gray")

listbox1 = controls.Listbox(body_frame)
listbox1.place(relwidth=.6, relheight=1.0)
listbox1.populate(['a', 'b', 'c', 'e'])
listbox1.select_item('c')
listbox1.alpha_insert('d')
listbox1.remove('b')

root.mainloop()