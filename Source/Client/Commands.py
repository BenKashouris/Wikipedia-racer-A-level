"""Module defining the services used by the client"""
import SocketController as SC
import re
from functools import reduce
from typing import List, Dict, Tuple

_USERNAME_AND_PASSWORD_REGEX = re.compile(r"""([a-z]|[0-9]|[A-Z])+""")

def connect_to_server(IP, port):
    global SocketController
    SocketController = SC.SocketController(IP, port)

def process_response(GUIcontroller):
    """Recieve the response and do what it says to do"""
    func_name, data = SocketController.receive()

    if func_name == "logged_in":
        GUIcontroller.get_page("LogInPage").clear()
        GUIcontroller.get_page("SignUpPage").clear()
        GUIcontroller.show_page("MainPage")
    elif func_name == "error":
        GUIcontroller.message_box(data.get("message"))
    elif func_name == "packet_error":
        GUIcontroller.message_box(data.get("message"))
    elif func_name == "leaderboard":
        GUIcontroller.show_page("LeaderBoardPage")
        for i, s in data.items():
            GUIcontroller.get_page("LeaderBoardPage").add_to_leaderboard(i, s)
    elif func_name == "game_found":
        GUIcontroller.show_page("GamePage")
        GUIcontroller.get_page("GamePage").start_game(**data)
    elif func_name == "chain":
        GUIcontroller.show_page("AnalysisPage")
        make_graph(GUIcontroller, **data)
    elif func_name == "possible_move":
        print("Here 1", data)
        GUIcontroller.get_page("GamePage").next_page_container.update_possible_moves(**data)
    elif func_name == "game_over":
        GUIcontroller.show_page("GameOverPage").show_result(**data)

def make_graph(GUIcontroller, depth: Dict[str, List[int]], edges: List[Tuple[Tuple[int, int], Tuple[int, int]]]):
    """make a the tree visular on AnalyisPage"""
    depth_fixed = {}  # Due to json the keys may have been converted from ints to string this will be after those are fixed
    pageIDs = reduce(lambda z, y :z + y, depth.values())  # Flatten values to a single list in order to get all pageIDs present
    pageID_to_title = get_titles(pageIDs) ## Get the pageID to title dictionary
    for key, value in depth.items():  # Make dictionary with int key and the page title
        value_new = []
        for i in value:
            value_new.append(pageID_to_title[str(i)])
        depth_fixed[int(key)] = value_new ## make a new depth dictionary with a integer key and a value of the article title not the article pageID
    GUIcontroller.get_page("AnalysisPage").make_graph(depth_fixed, edges)  # Pass to the page to deal with the data

def make_move(GUIcontroller, pageID: int):
    """ask the server to a make move then process the response"""
    SocketController.send("make_move", {"pageID": pageID})
    process_response(GUIcontroller)

def _valid_username_or_password(test_string: str) -> bool:
    """Test if a string is a valid username/password
         Rules: Must consist only of lowercase or uppercase letter or number and must be less than 33 characters
         Parameter: test_string: the string to test
         Returns: True or False"""
    return re.fullmatch(_USERNAME_AND_PASSWORD_REGEX, test_string) != None and len(test_string) < 33

def login(username: str, password: str, GUIcontroller) -> None:
    """ask the serer to login and process the response"""
    if not (_valid_username_or_password(username) and _valid_username_or_password(password)): 
        GUIcontroller.message_box("Invalid Password or username. Must be less than 32 characters and only be letters or numbers")
    else:
        SocketController.send("log_in", {"username": username, "password": password})
        process_response(GUIcontroller)

def sign_up(username: str, password: str, confirm_password: str, GUIcontroller) -> None:
    """ask the serer to sign_up and process the response"""
    if password != confirm_password: 
        GUIcontroller.message_box("passwords did not match")
    elif not (_valid_username_or_password(username) and _valid_username_or_password(password)): 
        GUIcontroller.message_box("Invalid Password or username. Must be less than 32 characters and only be letters or numbers")
    else:
        SocketController.send("sign_up", {"username": username, "password": password})
        process_response(GUIcontroller)

def leaderboard(GUIcontroller):
    """ask the server for the leaderboard and process the response"""
    GUIcontroller.get_page("LeaderBoardPage").clear()
    SocketController.send("get_leaderboard", {})
    process_response(GUIcontroller)

def queue(GUIcontroller):
    """ask the server to queue and process the response"""
    GUIcontroller.show_page("WaitingPage")
    SocketController.send("queue", {})
    while not SocketController.is_readable(): # while the socket control is not readable keep the page alive
        GUIcontroller.update()  # This stop windows from thinking the program has crashed
    process_response(GUIcontroller)

def analysis(GUIcontroller, start_pageID: int, end_pageID: int): 
    """ask the server to analyis these chain between this page and process the response"""
    SocketController.send("get_chain", {"start_pageID": start_pageID, "end_pageID": end_pageID})
    process_response(GUIcontroller)

def get_titles(pageIDs: List[int]):
    """get the titles of the pageIDs"""
    pageIDs_copy = pageIDs.copy() ## This shouldnt be nessary but sometimes this function causes unexpeccted behavoiour
    data = {}  # this will hold the server response
    section = []  # Since the maxiumum request size is 1024 pageIDs must be sent in section this will hold the current sections
    while pageIDs_copy != []:  # While we havent send all the pageIDs to the server
        section.append(pageIDs_copy.pop(0))  # Append to sections the first pageID in the list
        length = get_cumaltive_length(section)  # Caluclate the number of digits in the entire list
        if length > 900 or pageIDs_copy == []:  # If the length is bigger than 900 or pageIDs is empty 
            if length > 1000: ## if the length is bigger than 1000 it would be too long
                pageIDs_copy.append(section.pop(0)) # so remove a element 
            if section == []: break
            SocketController.send("get_titles", {"pageIDs": section})  # Send the section
            func_name, d = SocketController.receive()  # recieve the data
            data.update(d)  # update the data with the new data recieved
            section = []  # clear section
    return data

def get_cumaltive_length(l: list):
    sum = 0
    for i in l:
        sum += len(str(i))
    return sum 