import Tkinter as tk
import os
import time


class FileManager(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.frame = tk.Frame(self)

        self.frame.rowconfigure(0, weight=0)
        self.frame.rowconfigure(1, weight=5)
        self.frame.rowconfigure(2, weight=5)
        self.frame.columnconfigure(0, weight=2)
        self.frame.columnconfigure(1, weight=4)
        self.frame.columnconfigure(2, weight=3)
        self.frame.columnconfigure(3, weight=3)
        self.frame.columnconfigure(4, weight=3)
        self.frame.columnconfigure(5, weight=6)

        self.path_txt = tk.Entry(self.frame, fg='blue', font='Arial20')
        self.path_txt.insert(0, 'Enter a Path')
        self.path_txt.grid(row=0, column=0, columnspan=2, sticky="news", padx=5, pady=5)
        self.path_txt.bind("<FocusIn>", lambda event: self.path_txt.delete(0, tk.END)
                                                    if self.path_txt.get() == 'Enter a Path' else None)
        self.bind("<Return>", self.open_dir)

        self.dir_listbox = tk.Listbox(self.frame)
        self.dir_listbox.grid(row=1, column=0, rowspan=2, columnspan=2, sticky="news", padx=5, pady=5)
        self.dir_listbox.bind('<<ListboxSelect>>', self.dir_onselect)

        self.files_listbox = tk.Listbox(self.frame)
        self.files_listbox.grid(row=0, column=2, rowspan=3, columnspan=3, sticky="nesw", padx=5, pady=5)
        self.files_listbox.bind('<<ListboxSelect>>', self.file_onselect)

        self.files_attributes_listbox = tk.Listbox(self.frame)
        self.files_attributes_listbox.grid(row=0, column=5, rowspan=3, sticky="nesw", padx=5, pady=5)

        self.frame.grid(row=0, column=0, sticky="news", padx=5, pady=5)
        self.rowconfigure(0, weight=7)
        self.columnconfigure(0, weight=7)
        self.configure(background='yellow')
        self.frame.configure(background='light blue')
        self.title('Simple File Explorer')
        self.minsize(700, 300)

        self.last_dir = None
        self.last_file = None

    def open_dir(self, event=None, path=None):
        if not path:
            path = self.path_txt.get()
        self.clear_all()
        self.last_dir = "\\".join(path.split("\\")[0:-1])  # save the last path
        # insert the back option ('..') in the directory listbox
        self.dir_listbox.insert(tk.END, '..')
        for root, dirs, files in os.walk(path):
            # update directories
            for dir in dirs:
                self.dir_listbox.insert(tk.END, dir)
            # update files
            for file in files:
                self.files_listbox.insert(tk.END, file)
            break

    def update_path(self, path):
        self.path_txt.delete(0, tk.END)
        self.path_txt.insert(0,path)

    def dir_onselect(self, event):
        if self.dir_listbox.curselection():
            index = int(self.dir_listbox.curselection()[0])
            dir = self.dir_listbox.get(index)
            if self.last_file:
                path = "\\".join(self.path_txt.get().split("\\")[0:-1])
                self.update_path(path)
                self.last_file = None
            if dir == '..' and self.last_dir:
                path = self.last_dir
            else:
                path = "\\".join(self.path_txt.get().split("\\")+[dir])
            self.update_path(path)
            self.open_dir(path=path)

    def file_onselect(self, event):
        if self.files_listbox.curselection():
            index = int(self.files_listbox.curselection()[0])
            file = self.files_listbox.get(index)
            if self.last_file:
                path = "\\".join(self.path_txt.get().split("\\")[0:-1] + [file])
            else:
                path = "\\".join(self.path_txt.get().split("\\") + [file])
            self.last_file = file
            self.update_path(path)
            self.show_file_attributes_listbox()

    def show_file_attributes_listbox(self):
        if file:
            path = self.path_txt.get()
            file_obj = os.stat(path)
            self.files_attributes_listbox.delete(0, tk.END)  # make sure the listbox is cleared
            self.files_attributes_listbox.insert(tk.END, "File Size (in bytes): " + str(file_obj.st_size))
            self.files_attributes_listbox.insert(tk.END, "Last Accessed: %s" % time.ctime(file_obj.st_atime))
            self.files_attributes_listbox.insert(tk.END, "Last Modified: %s" % time.ctime(file_obj.st_mtime))


    def clear_all(self):
        self.dir_listbox.delete(0, tk.END)
        self.files_listbox.delete(0, tk.END)
        self.files_attributes_listbox.delete(0, tk.END)


def __main__():
    if __name__ == "__main__":
        f = FileManager()
        f.mainloop()

__main__()




