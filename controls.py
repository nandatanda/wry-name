import tkinter as tk


class Frame(tk.Frame):
    def __init__(self, parent, x=0, y=0, width=1, height=1, background="white"):
        tk.Frame.__init__(self, parent, bg=background)

    def set_background(self, color):
        self.configure(bg=color)


class Listbox(tk.Listbox):
    def __init__(self, parent):
        tk.Listbox.__init__(self, parent)

    def items(self):
        """Return a list of listbox contents."""
        return [self.get(index) for index in range(self.size())]

    def index(self, item):
        """Return the index of an item."""
        contents = self.items()
        try:
            return contents.index(item)
        except ValueError:
            return 0

    def selected_index(self):
        """Return the index of the currently selected item."""
        try:
            return self.curselection()[0]
        except IndexError:
            return 0

    def clear_items(self):
        """Remove all items from the listbox."""
        self.delete(0, self.size() - 1)
        return

    def populate(self, items):
        """Remove all items and replace them with elements from the given list."""
        index = self.selected_index()
        self.clear_items()
        for index, item in enumerate(items):
            self.insert(index, item)

    def select_index(self, index):
        """Select an item by its index."""
        last = self.size() - 1
        if index > last: index = last
        self.select_clear(0, last)
        self.select_set(index)
        self.activate(index)
        self.see(index)
        return

    def select_item(self, item):
        """Select an item by its name."""
        index = self.index(item)
        last = self.size() - 1
        self.select_clear(0, last)
        self.select_set(index)
        self.activate(index)
        self.see(index)
        return

    def alpha_insert(self, item):
        """Insert an item while respecting alphabetical order."""
        latest_index = self.selected_index()
        contents = self.items()
        contents.append(item)
        contents.sort()
        self.clear_items()
        for index, content in enumerate(contents):
            self.insert(index, content)
        self.select_index(latest_index)
        return

    def remove(self, item):
        """Delete one item from the listbox."""
        contents = self.items()
        contents.remove(item)
        self.populate(contents)
        return