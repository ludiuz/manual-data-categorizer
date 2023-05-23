import tkinter as tk
from tkinter import simpledialog, messagebox
import pickle
import random

class Item:
    def __init__(self, name):
        self.name = name
        self.group = "Not specified"

    def __str__(self):
        return f'{self.name}\n\nGroup: {self.group}'

class Data:
    def __init__(self):
        self.groups = {"Not specified": []}
        self.items = []

    def __getitem__(self, index):
        return self.items[index]

    def __len__(self):
        return len(self.items)

    def append(self, item):
        self.items.append(item)
        self.groups["Not specified"].append(item)

    def create_group(self, name):
        self.groups[name] = []

    def delete_group(self, name):
        if name in self.groups:
            for item in self.groups[name]:
                item.group = "Not specified"
                self.groups["Not specified"].append(item)
            del self.groups[name]

    def add_to_group(self, index, group):
        item = self.items[index]
        self.groups[item.group].remove(item)
        item.group = group
        self.groups[group].append(item)

    def save_data(self, file_name):
        with open(file_name, 'wb') as f:
            pickle.dump(self.items, f)

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("manual data categorizer")
        self.grid(sticky="nsew")

        self.index = 0
        self.data = Data()
        self.groups_buttons = {}

        mockup_input_data = ["Apple", "Banana", "Orange", "Strawberry", "Lettuce", "Cabbage", "Carrot", 
                             "Pot", "Pan", "Spoon", "Fork", "Knife", "Motherboard", "CPU", "GPU", 
                             "RAM", "Hard drive", "Mercedes", "BMW", "Audi", "Nintendo", "Sony", 
                             "Microsoft", "Vodka", "Whiskey", "Beer", "Wine", "Gucci", "Prada", 
                             "Versace", "Milk chocolate", "Dark chocolate", "White chocolate", 
                             "Fruit and nut chocolate"]
        random.shuffle(mockup_input_data)
        for item_string in mockup_input_data[:20]:
            self.data.append(Item(item_string))

        self.prev_button = tk.Button(self, text="<<", command=self.prev_string)
        self.prev_button.grid(row=0, column=0, rowspan=6, sticky="nsew")

        self.item_text = tk.Text(self, height=15, width=30)
        self.item_text.grid(row=0, column=1, rowspan=6, sticky="nsew")

        self.next_button = tk.Button(self, text=">>", command=self.next_string)
        self.next_button.grid(row=0, column=2, rowspan=6, sticky="nsew")

        self.add_group_button = tk.Button(self, text="+", command=self.add_group)
        self.add_group_button.grid(row=0, column=3, sticky="nsew")

        self.del_group_button = tk.Button(self, text="-", command=self.delete_group)
        self.del_group_button.grid(row=1, column=3, sticky="nsew")

        self.export_button = tk.Button(self, text="e", command=self.export_data)
        self.export_button.grid(row=2, column=3, sticky="nsew")

        self.groups_buttons_frame = tk.Frame(self)
        self.groups_buttons_frame.grid(row=0, column=4, rowspan=6, sticky="nsew")

        for group_name in self.data.groups:
            button = tk.Button(self.groups_buttons_frame, text=group_name, 
                               command=lambda group_name=group_name: self.set_group(group_name))
            button.pack(fill="x")
            self.groups_buttons[group_name] = button

        self.update_text()

    def update_text(self):
        self.item_text.config(state='normal')
        self.item_text.delete(1.0, tk.END)
        self.item_text.insert(tk.END, str(self.data[self.index]))
        self.item_text.config(state='disabled')

        for button in self.groups_buttons_frame.winfo_children():
            button.config(bg='grey')

        if self.data[self.index].group in self.groups_buttons:
            self.groups_buttons[self.data[self.index].group].config(bg='lime')

    def prev_string(self):
        self.index = (self.index - 1) % len(self.data)
        self.update_text()

    def next_string(self):
        self.index = (self.index + 1) % len(self.data)
        self.update_text()

    def add_group(self):
        name = simpledialog.askstring("Input", "Enter category name",
                                      parent=self.master)
        if name is not None:
            if name not in self.data.groups:
                self.data.create_group(name)
                button = tk.Button(self.groups_buttons_frame, text=name[:15]+'...' if len(name)>15 else name, 
                                   command=lambda group_name=name: self.set_group(group_name))
                button.pack(fill="x")
                self.groups_buttons[name] = button
            else:
                messagebox.showinfo("Info", "Category already exists!")

    def delete_group(self):
        name = simpledialog.askstring("Input", "Enter category name",
                                      parent=self.master)
        if name is not None:
            if name in self.data.groups and name != "Not specified":
                self.data.delete_group(name)
                self.groups_buttons[name].destroy()
                del self.groups_buttons[name]
            else:
                messagebox.showinfo("Info", "Category does not exist!")

    def set_group(self, group_name):
        self.data.add_to_group(self.index, group_name)
        self.index = (self.index + 1) % len(self.data)
        self.update_text()

    def export_data(self):
        self.data.save_data("data.pkl")
        messagebox.showinfo("Info", "Data saved successfully!")

root = tk.Tk()
root.geometry('480x380')
root.resizable(0, 0)
app = Application(master=root)
root.mainloop()
