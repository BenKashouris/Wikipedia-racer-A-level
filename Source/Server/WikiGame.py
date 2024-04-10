"""Module defining game logic for a WikiGame"""
from datetime import datetime
import Search
class Player:
    """A game player object"""
    def __init__(self, client, username):
        self.client, self.username = client, username
        self.current_pageID: int = None

    def send(self, func_name: str, data: dict):
        """Send a message to this player througth the client object
        parameters func_name the function name as defined by the protcol
                   data the data for the function"""
        self.client.send(func_name, data)

class WikiGame:
    def __init__(self, player_one, player_two, database):
        """Start a game"""
        self.player_one, self.player_two, self.database = player_one, player_two, database
        self.ID = hash(datetime.now())  # Set the ID of the game to be the hash of the datetime when the game started

        while True:
            self.start_pageID = database.get_random_pageID()  # Generate a start_pageID and end_pageID
            self.end_pageID = database.get_random_pageID()
            if Search.bi_bfs(self.start_pageID, self.end_pageID, self.database) != -1: break  # If the search has a path then stop generating
        #  Get the titles for both pageIDs
        start_page, end_page = database.get_titles([self.start_pageID])[self.start_pageID],  database.get_titles([self.end_pageID])[self.end_pageID]
        self.player_one.send("game_found", {"start_page_title": start_page, "end_page_title": end_page}) # Tell the client a game has been found and give them the start and end titles
        self.player_two.send("game_found", {"start_page_title": start_page, "end_page_title": end_page})
        self.make_move(player_one.client, self.start_pageID)  # Make a move for both clients as if they had clicked on the start_pageID
        self.make_move(player_two.client, self.start_pageID)

    def make_move(self, client, pageID):
        """Make a move for client making move towards pageID"""
        current_player = self.player_one if client.get_session_id() == self.player_one.client.get_session_id() else self.player_two  # Work out which player the request has come from 
        current_oponnent = self.player_one if client.get_session_id() != self.player_one.client.get_session_id() else self.player_two
        ## Check if move was possible
        if current_player.current_pageID != None:  # If not the first move
            possible_moves = self.database.get_links(True, current_player.current_pageID)  # Get the moves you could go to from the current pageID
            if not pageID in possible_moves:  # If its not a possible move tell the client then exist this function
                current_player.send("error", {"message": "Invalid move"})
                return 
        current_player.current_pageID = pageID
        if current_player.current_pageID == self.end_pageID:  #If the player has made it to the end page then end the game
            self.update_winner_elo(current_player)  # Update the player elo
            current_player.send("game_over", {"result": "win"})  # Tell the current player they have won 
            current_oponnent.send("game_over", {"result": "loss"})
        else:
            next_pageIDs = self.database.get_links(True, current_player.current_pageID)  # Get the next possible pages
            current_player.send("possible_move", {"pageIDs": next_pageIDs})  # Tell the player the next possible pages

    def update_winner_elo(self, winning_player):
        self.database.update_player_elo(self.player_one.username, self.player_one == winning_player, self.player_two.username)
        self.database.update_player_elo(self.player_two.username, self.player_two == winning_player, self.player_one.username)
