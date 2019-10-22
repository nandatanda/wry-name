from tkinter import filedialog
from tkinter import Tk
from time import sleep
import tkinter as tk
import os


def imported_files():
    if not current_directory == "":
        files = [f for f in os.listdir(current_directory)]
        return sorted(files)
    return []


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
    try:
        return listbox.curselection()[0]
    except IndexError:
        return 0


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

def remove_item(listbox, item):
    items = contents(listbox)
    items.remove(item)
    populate(listbox, items)
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


def clear_text(entry):
    entry.delete('0', tk.END)
    return


def search(files, number, padding):
    return [
        f
        for f in files
        if str(number).zfill(padding) in f
    ]


def debug():
    print("\n**************** DEBUG INFO ***************")
    print("The windows dimensions are ({}, {}).".format(window_width, window_height))
    print("\nThe current working directory is {}".format(current_directory))
    print("\nEpisodes to be renamed:")
    for episode in imported_files(): print("\t{}".format(episode))
    #print("\nEpisodes saved for manual review:")
    #for episode in saved_for_later: print("\t{}".format(episode))
    print("\nEpisodes removed from list:")
    for episode in removed_files: print("\t{}".format(episode))
    print("\nSelected formats:")
    for f, v in formats.items(): print("\t{} : {}".format(f, v))
    return


#----------------------------------------------------------------


def select_folder_button_click():
    global current_directory
    current_directory = filedialog.askdirectory(title="Select Folder:")
    if not current_directory == "":
        populate(episodes_listbox, imported_files())
    select_index(episodes_listbox, 0)
    return


def remove_file_button_click():
    if imported_files():
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
    filtered_list = apply_filters(imported_files(), formats)

    if removed_files:
        for episode in removed_files:
            if episode in filtered_list:
                filtered_list.remove(episode)

    populate(episodes_listbox, filtered_list)
    select_item(episodes_listbox, latest_selection)
    return


def series_title_changed(series_title):
    fill = padding_selection.get()
    title = series_title.get()
    new_name = title + " - {}.mkv".format("1".zfill(fill))
    if not title == "":
        preview_label.config(text=new_name)
    else:
        preview_label.config(text="(^~^;)/")


def padding_selection_changed(padding_selection):
    fill = padding_selection.get()
    title = series_title.get()
    new_name = title + " - {}.mkv".format("1".zfill(fill))
    if not title == "" and not title == "Enter a new title here...":
        preview_label.config(text=new_name)
    else:
        preview_label.config(text="(^~^;)/")


def rename_button_click():
    if contents(episodes_listbox):
        files = [os.path.join(current_directory, filename) for filename in contents(episodes_listbox)]
        target_directory = current_directory
        padding = padding_selection.get()
        file_number = 0
        unmatched = 0
        title = series_title.get()

        while files:
            file_number +=1
            results = search(files, file_number, padding)
            if results:
                    if len(results) > 1:
                        unmatched += 1
                        print("Multiple matches found. Skipping this pass...")
                    else:
                        match = results[0]
                        ext = os.path.splitext(match)[1]
                        num = str(file_number).zfill(padding)
                        new = os.path.join(target_directory, "{} - {}{}".format(title, num, ext))
                        os.rename(match, new)
                        files.remove(match)
                        remove_item(episodes_listbox, os.path.basename(match))
                        file_number = 0
                        unmatched = 0
                        print("Renamed file '{}' to '{}'.".format(match, new))
            else:
                print("No matches found for episode {}.".format(file_number))
            print()
            if files and len(files) == unmatched:
                print("NEED USER INPUT!\n")
                break
            elif len(files) == 0:
                print("FILES SUCCESSFULLY RENAMED!\n")


#----------------------------------------------------------------


# ROOT
window_width = 800
window_height = 600
background_color = "light grey"
root = Tk()
root.title("WRYName")
canvas = tk.Canvas(root, width=window_width, height=window_height)
canvas.pack()
current_directory = ""
removed_files = []
formats = {
    ".mkv" : False, ".mp4" : False,
    ".mov" : False, ".flv" : False}
padding_selection = tk.IntVar(value=2)
series_title = tk.StringVar(value="")

# FRAMES
menu_frame = tk.Frame(root, bg="light blue")
menu_frame.place(relwidth=1, relheight=.2)
body_frame = tk.Frame(root, bg=background_color)
body_frame.place(rely=.2, relwidth=1, relheight=.8)

# LABELS
episodes_label = tk.Label(body_frame, bg=background_color, text="Episodes to rename:")
episodes_label.place(relx=.20, rely=0, relwidth=.3, relheight=.1)
saved_for_review_label = tk.Label(body_frame, bg=background_color, text="Saved for manual review:")
saved_for_review_label.place(relx=.20, rely=.6, relwidth=.3, relheight=.1)
formats_label = tk.Label(body_frame, bg=background_color, text="Filter by format:")
formats_label.place(relx=.7, rely=0, relwidth=.3, relheight=.1)
padding_label = tk.Label(body_frame, bg=background_color, text="Zero padding:")
padding_label.place(relx=.7, rely=.4, relwidth=.3, relheight=.1)
series_title_label = tk.Label(body_frame, bg=background_color, text="Series title:")
series_title_label.place(relx=.7, rely=.7, relwidth=.3, relheight=.1)
preview_label = tk.Label(body_frame, bg=background_color, text="(^~^;)/")
preview_label.place(relx=.7, rely=.85, relwidth=.3, relheight=.1)


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
apply_filters_button.place(relx=.775, rely=.3, relwidth=.15, relheight=.05)

# CHECKBOXES
mkv_checkbox = tk.Checkbutton(body_frame, bg=background_color, text=".mkv", command=mkv_checkbox_click)
mkv_checkbox.place(relx=.7, rely=.1, relwidth=.15, relheight=.05)
mp4_checkbox = tk.Checkbutton(body_frame, bg=background_color, text=".mp4", command=mp4_checkbox_click)
mp4_checkbox.place(relx=.7, rely=.2, relwidth=.15, relheight=.05)
mov_checkbox = tk.Checkbutton(body_frame, bg=background_color, text=".mov", command=mov_checkbox_click)
mov_checkbox.place(relx=.85, rely=.1, relwidth=.15, relheight=.05)
flv_checkbox = tk.Checkbutton(body_frame, bg=background_color, text=".flv", command=flv_checkbox_click)
flv_checkbox.place(relx=.85, rely=.2, relwidth=.15, relheight=.05)

# ENTRY
series_title_entry = tk.Entry(body_frame, textvariable=series_title)
series_title_entry.place(relx=.72, rely=.8, relwidth=.25)
series_title_entry.config(justify="center")
series_title_entry.insert(tk.INSERT, "Enter a new title here...")
series_title.trace_add("write", lambda name, index, mode = series_title: series_title_changed(series_title))

# RADIOBUTTONS
one_digit_radiobutton = tk.Radiobutton(body_frame, bg=background_color, var=padding_selection, value=0, text="No padding")
one_digit_radiobutton.place(relx=.7, rely=.5, relwidth=.15, relheight=.05)
two_digits_radiobutton = tk.Radiobutton(body_frame, bg=background_color, var=padding_selection, value=2, text="Two digits")
two_digits_radiobutton.place(relx=.85, rely=.5, relwidth=.15, relheight=.05)
three_digits_radiobutton = tk.Radiobutton(body_frame, bg=background_color, var=padding_selection, value=3, text="Three digits")
three_digits_radiobutton.place(relx=.70, rely=.6, relwidth=.15, relheight=.05)
four_digits_radiobutton = tk.Radiobutton(body_frame, bg=background_color, var=padding_selection, value=4, text="Four digits")
four_digits_radiobutton.place(relx=.85, rely=.6, relwidth=.15, relheight=.05)
padding_selection.trace_add("write", lambda name, index, mode = padding_selection: padding_selection_changed(padding_selection))

# LISTBOXES
episodes_listbox = tk.Listbox(body_frame, relief=tk.GROOVE)
episodes_listbox.place(relx=0, rely=.1, relwidth=.7, relheight=.5)
saved_for_review_listbox = tk.Listbox(body_frame, relief=tk.GROOVE)
saved_for_review_listbox.place(relx=0, rely=.7, relwidth=.7, relheight=.3)

root.mainloop()