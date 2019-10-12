from tkinter import filedialog
from tkinter import Tk
import tkinter as tk
import os


window_width = 800
window_height = 600
current_directory = ""
imported_files = []
removed_files = []
formats = {
    ".mkv" : False, ".mp4" : False,
    ".mov" : False, ".flv" : False}


def apply_filters(files, extensions):
    filters = [e for e in extensions if extensions[e]]
    if filters:
        return [f for f in files if os.path.splitext(f)[1] in filters]
    return files


def type_checked(item, extensions):
    filters = [ext for ext, val in extensions.items() if val]
    if filters:
        if os.path.splitext(item)[1] in filters:
            return True
        else:
            return False
    return True


def contents(listbox):
    items = []
    for index in range(listbox.size()):
        items.append(listbox.get(index))
    return items


def index(listbox, item):
    files = contents(listbox)
    try:
        return files.index(item)
    except ValueError:
        return 0


def selected_index(listbox):
    return listbox.curselection()[0] if episodes_listbox.size() else 0


def selected_item(listbox):
    index = selected_index(listbox)
    return listbox.get(index)


def select_index(listbox, index):
    last = listbox.size() - 1
    if index > last: index = last
    listbox.select_clear(0, last)
    listbox.select_set(index)
    listbox.activate(index)
    listbox.see(index)
    return


def select_item(listbox, item):
    i = index(listbox, item)
    listbox.select_clear(0, listbox.size() - 1)
    listbox.select_set(i)
    listbox.activate(i)
    listbox.see(i)
    return


def insert(listbox, item):
    index = selected_index(listbox)
    files = contents(listbox)
    files.append(item)
    files.sort()
    clear(listbox)
    for index, episode in enumerate(files):
        episodes_listbox.insert(index, episode)
    select_index(listbox, index)
    return


def populate(listbox, items):
    index = selected_index(listbox)
    clear(listbox)
    for index, episode in enumerate(items):
        episodes_listbox.insert(index, episode)
    select_index(listbox, index)
    return


def clear(listbox):
    listbox.delete(0, listbox.size() - 1)
    return


def debug():
    print("\n**************** DEBUG INFO ***************")
    print("The windows dimensions are ({}, {}).".format(window_width, window_height))
    print("\nThe current working directory is {}".format(current_directory))
    print("\nEpisodes to be renamed:")
    for episode in imported_files: print("\t{}".format(episode))
    #print("\nEpisodes saved for manual review:")
    #for episode in saved_for_later: print("\t{}".format(episode))
    print("\nEpisodes removed from list:")
    for episode in removed_files: print("\t{}".format(episode))
    print("\nSelected formats:")
    for f, v in formats.items(): print("\t{} : {}".format(f, v))


#----------------------------------------------------------------


def select_folder_button_click():
    global current_directory
    global imported_files
    current_directory = filedialog.askdirectory(title="Select Folder:")
    if not current_directory == "":
        imported_files = [f for f in os.listdir(current_directory)]
        imported_files.sort()
        populate(episodes_listbox, imported_files)
    select_index(episodes_listbox, 0)
    return


def remove_file_button_click():
    if imported_files:
        index = selected_index(episodes_listbox)
        selected_episode = selected_item(episodes_listbox)

        episodes_listbox.delete(index)
        removed_files.append(selected_episode)

        select_index(episodes_listbox, index)
    return


def undo_button_click():
    if removed_files:
        last_removed_episode = removed_files[-1]
        if type_checked(last_removed_episode, formats):
            insert(episodes_listbox, last_removed_episode)
            removed_files.remove(last_removed_episode)

            target_index = index(episodes_listbox, last_removed_episode)
            select_index(episodes_listbox, target_index)
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
    latest_selection = selected_item(episodes_listbox)
    filtered_list = apply_filters(imported_files, formats)

    if removed_files:
        for episode in removed_files:
            if episode in filtered_list:
                filtered_list.remove(episode)

    populate(episodes_listbox, filtered_list)
    select_item(episodes_listbox, latest_selection)
    return


def rename_button_click():
    # The main stuffs will happen here.
    pass


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