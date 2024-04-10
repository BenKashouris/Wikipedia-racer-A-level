import tkinter

class MultipageRoot(tkinter.Tk):
    """Tk root that has the ability to swap frames that are shown
        Parameters:
            pages: Tuple of Classes that inherit Frame
    """
    def __init__(self, pages, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)  # Make the parent Root

        self.container = tkinter.Frame(self)  # Container for the frames that will hold the pages
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        for page in pages:  # Create a instance of the frames ontop of each other
            self.pages[page.__name__] = page(self.container, self) 
            self.pages[page.__name__].grid(row=0, column=0, sticky="nsew") 

    def show_page(self, page_name):
        """Function to show a page
        Parametera:
            page_name: The string name of the class"""
        self.pages[page_name].tkraise()   # Raise the selected frame to the top
