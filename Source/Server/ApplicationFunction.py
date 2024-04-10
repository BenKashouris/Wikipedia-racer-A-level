"""Module defining applicaton functions used as services for network protcol"""
from json import decoder
import Database
from typing import List, Dict, Tuple
import WikiGame
import Search
from HelperFunctions import _valid_username_or_password
from Decoder import EncoderClient

database = Database.Database()
sessionsID_to_username = {}

### For all functions it is important to remeber that decoder client do not stay consistent over connection, only the sessionID stays consistent over a connection
def log_in(client: EncoderClient, username: str, password: str):
    """Log a client in"""
    if not (_valid_username_or_password(password) and _valid_username_or_password(username)):
        client.send("error", {"message": "Invalid username or password"})
        return
    real_password = database.get_password(username)
    if real_password == None: 
        client.send("error", {"message": "No account with this username"})
    elif password == real_password: 
        client.send("logged_in", {})
        sessionsID_to_username[client.get_session_id()] = username
    else: 
        client.send("error", {"message": "Incorrect Password"})

def sign_up(client: EncoderClient, username: str, password: str):
    """Sign up a client"""
    if not (_valid_username_or_password(password) and _valid_username_or_password(username)):
        client.send("error", {"message": "Invalid username or password"})
        return
    real_password = database.get_password(username)
    if real_password != None: 
        client.send("error", {"message": "Username taken"})
    else:
        database.add_user(username, password)
        client.send("logged_in", {})
        sessionsID_to_username[client.get_session_id()] = username

_client_game_queue = []
def queue(client: EncoderClient):
    """Add a client to the queue"""
    _client_game_queue.append(client) # Add client to queue at back
    while len(_client_game_queue) >= 2:
        player_one_client = _client_game_queue.pop(0)
        player_two_client = _client_game_queue.pop(0)
        make_game(player_one_client, player_two_client)

_games = {}
def make_game(player_one_client: EncoderClient, player_two_client: EncoderClient):
    """Create a game between player_one_client and player_two_client"""
    print("Game started", player_one_client, player_two_client)
    player_one = WikiGame.Player(player_one_client, sessionsID_to_username[player_one_client.get_session_id()])
    player_two = WikiGame.Player(player_two_client, sessionsID_to_username[player_two_client.get_session_id()])
    game = WikiGame.WikiGame(player_one, player_two, database)
    _games[player_one_client.get_session_id()] = game
    _games[player_two_client.get_session_id()] = game

def make_move(client: EncoderClient, pageID: int):
    """Make a move to the pageID"""
    game = _games.get(client.get_session_id())
    if game == None: 
        client.send("error", {"message": "Not currently in game"})
    else:
        game.make_move(client, pageID)

def get_titles(client: EncoderClient, pageIDs: List[int]):
    """Get the a the titles of pageIDs
    paramters: pageIDs a list of pageIDs
    returns: a dictionary with key of pageID and value of it resepective title"""
    titles = database.get_titles(pageIDs)
    for key, value in titles.items():
        titles[key] = value.replace("_", " ").replace("-", " ")  # Replace _ or - with spaces in titles
    client.send("titles", titles)

def get_chain(client: EncoderClient, start_pageID: int, end_pageID: int):
    """Get the chain between a two pageIDs
    paramters: start_pageID and end_pageID as integers
    returns: a depth dictionary with key of the depth and a value of a list of pageIDs at that depth
             a list of edges with a tuple of two i, j points representing a edge"""
    paths = Search.bi_bfs(start_pageID, end_pageID, database) 
    if paths == -1:  # if the search timed out
        client.send("error", {"message": "No path exists"})
        return
    depth = dict((i, []) for i in range(len(paths[0])))  # Make a dictionary with keys of depth and value of empty list. All paths should be same length so suffient to look at len of path[0]
    element_to_index: Dict[int, Tuple[int, int]] = {}
    edges = []
    for path in paths: # For each path
        for i, e in enumerate(path):  # Go thourgth each element in the path, i here will be the depth in the path
            if not (e in depth[i]): depth[i].append(e)  # If e not already in this depth add it to this depth
            element_to_index[e] = (i, len(depth[i]) - 1)  # Associate this element with the index. len(depth) - 1 is the index of the last slot added
    for path in paths:
        for i in range(len(path) - 1):
            edges.append((element_to_index[path[i]], element_to_index[path[i + 1]]))  # Then create the edges by going thougth each path and finding the i, j for each adjacent pair in that path
    client.send("chain", {"depth": depth, "edges": edges})

def get_leaderboard(client: EncoderClient):
    """Get the current leaderboard"""
    client.send("leaderboard", dict(enumerate(database.get_leaderboard(), start = 1)))

def error_packet(client: EncoderClient, message: str):
    """Send a error packet"""
    client.send("packet_error", {"message": message})

##https://en.wikipedia.org/?curid=
