from tkinter import filedialog
from tkinter import Tk
import tkinter as tk
import os

window_width = 800
window_height = 600
current_directory = ""
episodes = []
saved_for_later = []
removed = []
formats = {
    ".mkv" : False, ".mp4" : False,
    ".mov" : False, ".flv" : False}

def choose_directory():
    return filedialog.askdirectory(title="Select Folder:")

def filter(items, extensions):
    filters = [ext for ext, val in extensions.items() if val]
    if filters:
        results = []
        for item in items:
            if os.path.splitext(item)[1] in filters:
                results.append(item)
        return results
    return items

def select_folder_button_click():
    global current_directory
    global episodes
    current_directory = choose_directory()
    if not current_directory == "":
        episodes = [f for f in os.listdir(current_directory)]
        episodes_listbox.delete(0, episodes_listbox.size() - 1)
        for i, f in enumerate(episodes):
            episodes_listbox.insert(i, f)   
    episodes_listbox.select_set(0)
    return

def remove_file_button_click():
    if episodes:
        index = episodes_listbox.curselection()[0]
        removed.append((episodes_listbox.get(index), index))
        episodes_listbox.delete(index)
        episodes.remove(episodes[index])
        episodes_listbox.select_set(index)
    return

def undo_button_click():
    episode = ""
    index = 0
    if removed:
        episode, index = removed[-1]
        episodes_listbox.insert(index, episode)
        episodes.insert(index, episode)
        removed.remove(removed[-1])
        episodes_listbox.select_clear(0, tk.END)
        episodes_listbox.select_set(index)
        episodes_listbox.activate(index)
    return

def mkv_checkbox_click():
    if formats[".mkv"]: formats[".mkv"] = False
    else: formats[".mkv"] = True
    return

def mp4_checkbox_click():
    if formats[".mp4"]: formats[".mp4"] = False
    else: formats[".mp4"] = True
    return

def mov_checkbox_click():
    if formats[".mov"]: formats[".mov"] = False
    else: formats[".mov"] = True
    return

def flv_checkbox_click():
    if formats[".flv"]: formats[".flv"] = False
    else: formats[".flv"] = True
    return

def apply_filters_button_click():
    filtered_list = filter(episodes, formats)
    if episodes_listbox.size() > 0:
        index = episodes_listbox.curselection()[0]
    else: index = 0

    episodes_listbox.delete(0, episodes_listbox.size() - 1)

    for i, f in enumerate(filtered_list):
        episodes_listbox.insert(i, f)

    if index > episodes_listbox.size() - 1:
        index = episodes_listbox.size() - 1

    episodes_listbox.select_clear(0, tk.END)
    episodes_listbox.select_set(index)
    episodes_listbox.activate(index)
    episodes_listbox.see(index)
    
def rename_button_click():
    pass

def debug():
    print("\n**************** DEBUG INFO ***************")
    print("The windows dimensions are ({}, {}).".format(window_width, window_height))
    print("\nThe current working directory is {}".format(current_directory))
    print("\nEpisodes to be renamed:")
    for episode in episodes: print("\t{}".format(episode))
    print("\nEpisodes saved for manual review:")
    for episode in saved_for_later: print("\t{}".format(episode))
    print("\nEpisodes removed from list:")
    for episode in removed: print("\t{}".format(episode))
    print("\nSelected formats:")
    for f, v in formats.items(): print("\t{} : {}".format(f, v))

#----------------------------------------------------------------

# ROOT
root = Tk()
root.title("AniRename")
canvas = tk.Canvas(root, width=window_width, height=window_height)
canvas.pack()

# FRAMES
menu_frame = tk.Frame(root, bg="light blue")
menu_frame.place(relwidth=1, relheight=.2)
body_frame = tk.Frame(root, bg="light grey")
body_frame.place(rely=.2, relwidth=1, relheight=.8)

# LABELS
episodes_label = tk.Label(body_frame, bg="light grey", text="Episodes to rename:")
episodes_label.place(relx=.20, rely=0, relwidth=.3, relheight=.1)
saved_for_review_label = tk.Label(body_frame, bg="light grey", text="Saved for manual review:")
saved_for_review_label.place(relx=.20, rely=.6, relwidth=.3, relheight=.1)
formats_label = tk.Label(body_frame, bg="light grey", text="Filter by format:")
formats_label.place(relx=.7, rely=0, relwidth=.3, relheight=.1)

# BUTTONS
select_folder_button = tk.Button(menu_frame, text="Select Folder...", underline=0, command=select_folder_button_click)
select_folder_button.place(relwidth=.15, relheight=.2, relx=.1, rely=.4)
remove_file_button = tk.Button(menu_frame, text="Remove File", command=remove_file_button_click)
remove_file_button.place(relx=.3, rely=.4, relwidth=.15, relheight=.2)
undo_button = tk.Button(menu_frame, text="Undo", command=undo_button_click)
undo_button.place(relwidth=.15, relheight=.2, relx=.5, rely=.4)
rename_button = tk.Button(menu_frame, bg="light green", text="Rename", command=rename_button_click)
rename_button.place(relwidth=.15, relheight=.2, relx=.7, rely=.4)
debug_button = tk.Button(menu_frame, text="DEBUG", underline=0, command=debug)
debug_button.place(relwidth=.06, relheight=.2, relx=.93, rely=.75)
apply_filters_button = tk.Button(body_frame, text="Apply", command=apply_filters_button_click)
apply_filters_button.place(relx=.775, rely=.30, relwidth=.15, relheight=.05)

# CHECKBOXES
mkv_checkbox = tk.Checkbutton(body_frame, bg="light grey", text=".mkv", command=mkv_checkbox_click)
mkv_checkbox.place(relx=.7, rely=.1, relwidth=.15, relheight=.05)
mp4_checkbox = tk.Checkbutton(body_frame, bg="light grey", text=".mp4", command=mp4_checkbox_click)
mp4_checkbox.place(relx=.7, rely=.2, relwidth=.15, relheight=.05)
mov_checkbox = tk.Checkbutton(body_frame, bg="light grey", text=".mov", command=mov_checkbox_click)
mov_checkbox.place(relx=.85, rely=.1, relwidth=.15, relheight=.05)
flv_checkbox = tk.Checkbutton(body_frame, bg="light grey", text=".flv", command=flv_checkbox_click)
flv_checkbox.place(relx=.85, rely=.2, relwidth=.15, relheight=.05)

# LISTBOXES
episodes_listbox = tk.Listbox(body_frame, relief=tk.GROOVE)
episodes_listbox.place(relx=0, rely=.1, relwidth=.7, relheight=.5)
saved_for_review_listbox = tk.Listbox(body_frame, relief=tk.GROOVE)
saved_for_review_listbox.place(relx=0,rely=.7, relwidth=.7, relheight=.3)

root.mainloop()