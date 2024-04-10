import MultipageRoot
from tkinter import messagebox

class GUIController(MultipageRoot.MultipageRoot):
    def message_box(self, msg: str):
        messagebox.showerror('Wikipedia Races', msg)

    def get_page(self, page_name: str):
        return self.pages[page_name]