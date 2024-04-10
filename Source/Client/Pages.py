"""Method defining the pages"""
import tkinter as tk
from tkinter.constants import END ##importing tkinter modules
from Colors import COLORS
import Commands
import DirectedGraphWidget

class LogInPage(tk.Frame):
    def __init__(self, parent, root_controller):
        tk.Frame.__init__(self, parent) 
        self.root_controller = root_controller

        self.container = tk.Frame(self, width=250, height=650)  # Container to hold the log in widgets
        self.container.place(relx=.5, rely=.5, anchor="c")

        tk.Label(self.container, text="Wikipedia Races", font=("Arial", 25)).place(relx = 0.5, rely = 0.2, anchor="center")  # Title Label

        tk.Label(self.container, text="Username", font=("Arial", 10)).place(relx = 0.2, rely = 0.375, anchor="center")  # Username Label
        self.username_entry = tk.Entry(self.container, width = 35)  # Text Input for username
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")

        tk.Label(self.container, text="Password", font=("Arial", 10)).place(relx = 0.2, rely = 0.45, anchor="center")  # Password Label
        self.password_entry = tk.Entry(self.container, width = 35, show="*")  # Text input for password
        self.password_entry.place(relx=0.5, rely=0.475, anchor="center")

        tk.Button(self.container, text="          Login           ", font=("Arial", 15), fg = COLORS.HYPERLINK_BLUE,  # Login Button
                  command = lambda: Commands.login(self.username_entry.get(), self.password_entry.get(), self.root_controller)
                  ).place(relx=0.5, rely=0.53, anchor="center")
        tk.Button(self.container, text="Sign Up", font=("Arial", 10), fg = COLORS.HYPERLINK_BLUE, command = lambda: self.root_controller.show_page("SignUpPage")).place(relx=0.5, rely=0.6, anchor="center")  # Sign up Page

    def clear(self):
        """Clear the username and password entry"""
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)

class MainPage(tk.Frame):
    def __init__(self, parent, root_controller):
        tk.Frame.__init__(self, parent) 
        self.root_controller = root_controller

        tk.Button(self, text="Play", font=("Arial", 15), fg = COLORS.HYPERLINK_BLUE,
                  command = lambda: Commands.queue(self.root_controller)).place(relx=0.5, rely=0.50, anchor="center", width = 300)  # Play Button
        tk.Button(self, text="Analysis mode", font=("Arial", 15), fg = COLORS.HYPERLINK_BLUE,
                  command = lambda: self.root_controller.show_page("AnalysisInputPage")).place(relx=0.5, rely=0.55, anchor="center", width = 300)  # Analysis Mode Button
        tk.Button(self, text="Leadboard", font=("Arial", 15), fg = COLORS.HYPERLINK_BLUE,
                  command = lambda: Commands.leaderboard(self.root_controller)).place(relx=0.5, rely=0.6, anchor="center", width = 300)  # Leadboard mode

class SignUpPage(tk.Frame):
    def __init__(self, parent, root_controller):
        tk.Frame.__init__(self, parent) 
        self.root_controller = root_controller

        self.container = tk.Frame(self, width=250, height=650)  # Container to hold the log in widgets
        self.container.place(relx=.5, rely=.5, anchor="c")

        tk.Label(self.container, text="Wikipedia Races", font=("Arial", 25)).place(relx = 0.5, rely = 0.2, anchor="center")  # Title Label

        tk.Label(self.container, text="Username", font=("Arial", 10)).place(relx = 0.2, rely = 0.375, anchor="center")  # Username Label
        self.username_entry = tk.Entry(self.container, width = 35)  # Text Input for username
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")

        tk.Label(self.container, text="Password", font=("Arial", 10)).place(relx = 0.2, rely = 0.45, anchor="center")  # Password Label
        self.password_entry = tk.Entry(self.container, width = 35, show="*")  # Text input for password
        self.password_entry.place(relx=0.5, rely=0.475, anchor="center")

        tk.Label(self.container, text="Confirm Password", font=("Arial", 10)).place(relx = 0.28, rely = 0.525, anchor="center")  # Confirm Password Label
        self.password_confirm_entry = tk.Entry(self.container, width = 35, show="*")  # Text input for confirm password
        self.password_confirm_entry.place(relx=0.5, rely=0.55, anchor="center")

        tk.Button(self.container, text="        Sign Up         ", font=("Arial", 15), fg = COLORS.HYPERLINK_BLUE,  # Sign Up Button
                  command = lambda: Commands.sign_up(self.username_entry.get(), self.password_entry.get(), self.password_confirm_entry.get(), self.root_controller)
                  ).place(relx=0.5, rely=0.605, anchor="center")
        tk.Button(self.container, text="Login", font=("Arial", 10), fg = COLORS.HYPERLINK_BLUE, command = lambda: self.root_controller.show_page("LogInPage")).place(relx=0.5, rely=0.675, anchor="center")  # log in Button

    def clear(self):
        """Clear the username and password entry"""
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.password_confirm_entry.delete(0, END)

class LeaderBoardPage(tk.Frame):
    def __init__(self, parent, root_controller):
        tk.Frame.__init__(self, parent) 
        self.root_controller = root_controller
        self.bind("<Configure>", self.resize)

        tk.Label(self, text="Leaderboard", font=("Arial", 30)).place(relx = 0.25, rely = 0.05, anchor="center")
        tk.Label(self, text="Username", font=("Arial", 10)).place(relx = 0.333, rely = 0.09, anchor="center")
        tk.Label(self, text="Elo", font=("Arial", 10)).place(relx = 0.666, rely = 0.09, anchor="center")

        self.leaderboard_usernames = tk.Listbox(self, width=100, height=10)
        self.leaderboard_usernames.place(relx = 0.333, rely = 0.5, anchor="center")

        self.leaderboard_elo = tk.Listbox(self, width=100, height=10)
        self.leaderboard_elo.place(relx = 0.666, rely = 0.5, anchor="center")

        tk.Button(self, text="Main Page", font=("Arial", 15), fg = COLORS.HYPERLINK_BLUE,
            command = lambda: self.root_controller.show_page("MainPage")).place(relx=0.5, rely=0.95, anchor="center", width = 300)

    def add_to_leaderboard(self, index: int, data: tuple[str, int]):
        """Add a entry to the leaderboard at index, with username of data[0] and elo of data[1]"""
        self.leaderboard_usernames.insert(index, data[0])
        self.leaderboard_elo.insert(index, data[1])

    def resize(self, e):
        """Resize the leaderboard"""
        self.leaderboard_usernames["width"] = int(e.width / 20)
        self.leaderboard_usernames["height"] = int(0.05 * e.height)
        self.leaderboard_elo["width"] = int(e.width / 20)
        self.leaderboard_elo["height"] = int(0.05 * e.height)

    def clear(self):
        """Clear the leaderboard"""
        self.leaderboard_usernames.delete(0,END)
        self.leaderboard_elo.delete(0,END)

class WaitingPage(tk.Frame):
    def __init__(self, parent, root_controller):
        tk.Frame.__init__(self, parent) 
        self.root_controller = root_controller

        tk.Label(self, text="Waiting For Game", font=("Arial", 10)).place(relx = 0.5, rely = 0.5, anchor="center")

class GamePage(tk.Frame):
    def __init__(self, parent, root_controller):
        tk.Frame.__init__(self, parent) 
        self.root_controller = root_controller

        tk.Label(self, text="Start Page:", font=("Arial", 10)).place(relx = 0.05, rely = 0.1, anchor="center")
        tk.Label(self, text="End Page:", font=("Arial", 10)).place(relx = 0.5, rely = 0.1, anchor="center")

        self.start_page_title_label = tk.Label(self, text="", font=("Arial", 10))
        self.end_page_title_label = tk.Label(self, text="", font=("Arial", 10))

        self.start_page_title_label.place(relx = 0.25, rely = 0.1, anchor="center")
        self.end_page_title_label.place(relx = 0.75, rely = 0.1, anchor="center")

        self.next_page_container = NextPage(self, self.root_controller)
        self.next_page_container.place(relx = 0.5, rely = 0.5, anchor="center")

    def start_game(self, start_page_title: str, end_page_title: str):
        """Update the title labels and the next page list"""
        self.start_page_title_label["text"] = start_page_title.replace("_", " ")
        self.end_page_title_label["text"] = end_page_title.replace("_", " ")
        Commands.process_response(self.root_controller)

class NextPage(tk.Frame):
    def __init__(self, parent, GUIController):
        tk.Frame.__init__(self, parent, height = 50, width = 100)
        self.GUIController = GUIController

        self.scrollbar = tk.Scrollbar(self, orient="vertical")
        self.scrollbar.pack(side="right",fill="y")

        self.next_pages = tk.Listbox(self, yscrollcommand = self.scrollbar.set, height = 50, width = 100)
        self.next_pages.bind("<<ListboxSelect>>", self.line_pressed)
        self.next_pages.pack(side = tk.LEFT, fill = tk.BOTH)

    def update_possible_moves(self, pageIDs: list[int]):
        """Add new possible moves"""
        self.next_pages.delete(0, tk.END)# clear all current pages
        self.pageID_to_title = Commands.get_titles(pageIDs)
        self.index_to_pageID = dict(enumerate(pageIDs))
        for i, pageID in self.index_to_pageID.items():
            self.next_pages.insert(i, self.pageID_to_title[str(pageID)])

    def line_pressed(self, event):
        """Handle when a page is clicked on from the list of next pages"""
        selection = event.widget.curselection()
        if selection:
            Commands.make_move(self.GUIController, self.index_to_pageID[selection[0]])

class AnalysisPage(tk.Frame):
    def __init__(self, parent, root_controller):
        tk.Frame.__init__(self, parent) 
        self.root_controller = root_controller

        tk.Button(self, text="Home", font=("Arial", 10), fg = COLORS.HYPERLINK_BLUE, command = self.go_home).pack(anchor="s", pady = 100)  # log in Button

    def go_home(self):
        """Delete the graph diagram and return to the main page"""
        self.g.forget()
        self.root_controller.show_page("MainPage")

    def make_graph(self, depth, edges):
        """Make the graph diagram"""
        self.g = DirectedGraphWidget.DirectedGraph(self, depth, edges, text_color= COLORS.HYPERLINK_BLUE) 
        self.g.pack(expand = 1, fill = tk.BOTH)

class GameOverPage(tk.Frame):
    def __init__(self, parent, root_controller):
        tk.Frame.__init__(self, parent) 
        self.root_controller = root_controller
        
        self.result = tk.Label(self, text="", font=("Arial", 10)).place(relx = 0.5, rely = 0.4, anchor="center")
        tk.Button(self, text="Main Menu", font=("Arial", 15), fg = COLORS.HYPERLINK_BLUE,  # Login Button
            command = lambda: root_controller.show_page("MainPage")
            ).place(relx=0.5, rely=0.6, anchor="center")

    def show_result(self, result: str):
        """Update the result of the game"""
        self.result["text"] = "You " + result

class AnalysisInputPage(tk.Frame):
    def __init__(self, parent, root_controller):
        tk.Frame.__init__(self, parent) 
        self.root_controller = root_controller

        self.container = tk.Frame(self, width=250, height=650)  # Container to hold the log in widgets
        self.container.place(relx=.5, rely=.5, anchor="c")

        tk.Label(self.container, text="Start Page:", font=("Arial", 10)).place(relx = 0.2, rely = 0.375, anchor="center")
        tk.Label(self.container, text="End Page:", font=("Arial", 10)).place(relx = 0.2, rely = 0.45, anchor="center")

        self.start_page_entry = tk.Entry(self.container, width = 35)
        self.start_page_entry.place(relx=0.5, rely=0.4, anchor="center")

        self.end_page_entry = tk.Entry(self.container, width = 35)
        self.end_page_entry.place(relx=0.5, rely=0.475, anchor="center")

        tk.Button(self.container, text="          Analyise           ", font=("Arial", 15), fg = COLORS.HYPERLINK_BLUE,  # Login Button
            command = lambda: Commands.analysis(self.root_controller, int(self.start_page_entry.get()), int(self.end_page_entry.get()))
            ).place(relx=0.5, rely=0.53, anchor="center")

pages = (LogInPage, MainPage, SignUpPage, LeaderBoardPage, WaitingPage, GamePage, AnalysisPage, AnalysisInputPage, GameOverPage)

