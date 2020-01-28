import tkinter as tk

# episodes_listbox = tk.Listbox(body_frame, relief=tk.GROOVE)
# episodes_listbox.place(relx=0, rely=.1, relwidth=.7, relheight=.5)
# saved_for_review_listbox = tk.Listbox(body_frame, relief=tk.GROOVE)
# saved_for_review_listbox.place(relx=0, rely=.7, relwidth=.7, relheight=.3)

class Listbox():
    def __init__(self, x=0, y=0, width=1, height=1):
        self.master = tk.Listbox(body_frame, relief=tk.GROOVE)
        self.master.place(relx=x, rely=y, relwidth=width, relheight=height)

    def items(self):
        return [
            self.master.get(index)
            for index in range(self.master.size())
        ]

    def selected_index(self):
        try:
            return self.master.curselection()[0]
        except IndexError:
            return 0

    def clear_items(self):
        self.master.delete(0, self.master.size() - 1)
        return

    def populate(self, items):
        index = self.selected_index()
        self.clear_items()
        for index, item in enumerate(items):
            self.master.insert


    # def populate(listbox, items):
        # index = selected_index(listbox)
        # clear(listbox)
        # for index, episode in enumerate(items):
            # episodes_listbox.insert(index, episode)
        # select_index(listbox, index)
        # return
