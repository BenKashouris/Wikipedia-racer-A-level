from typing import List, Tuple, Dict
import sqlite3

USERDB_PATH = "C:/Users/benja/source/repos/NEA-Server/user_database.db"
WIKIPEDIADB_PATH = "C:/Users/benja/source/repos/NEA-Server/wikipedia_database.db"

class Database:
    """A helper database connection"""
    def __init__(self):
        self.wikiDB_conn = sqlite3.connect(WIKIPEDIADB_PATH)
        self.wikiDB_cur = self.wikiDB_conn.cursor()

        self.userDB_conn = sqlite3.connect(USERDB_PATH)
        self.userDB_cur = self.userDB_conn.cursor()

    def get_leaderboard(self) -> List[Tuple[str, int]]:
        """Gets the Leaderboard:
        parameters: None
        returns: List of Tuple with username and elo. List is in order, max length 100"""
        self.userDB_cur.execute("SELECT username, elo FROM users ORDER BY elo DESC LIMIT 100")
        return self.userDB_cur.fetchall()

    def get_password(self, username: str) -> (str | None):
        """Gets the password for a username
        parameters: username
        returns: the password if one exist else None"""
        self.userDB_cur.execute("SELECT password FROM users WHERE username = ?", (username,))
        password = self.userDB_cur.fetchone()
        if password != None: return password[0]

    def add_user(self, username: str, password: str) -> None:
        """Adds a user to the database
        Parameters: username, password
        returns: None"""
        self.userDB_cur.execute("INSERT INTO users (username, password) Values (?, ?)", (username, password))
        self.userDB_conn.commit()

    def update_player_elo(self, username: str, win: bool, opponent_username: str) -> int:
        """Changes a player elo for a win or loss against a opponent
        Parameters: username: the username of the player elo to update
                    win: a bool of wether they won the game or not
                    opponent_username: the username of the player they played against
        Returns: None"""
        self.userDB_cur.execute("SELECT elo FROM users WHERE username = ?", (opponent_username,))
        opponent_rating = self.userDB_cur.fetchone()[0]
        self.userDB_cur.execute("""UPDATE users SET num_of_wins = num_of_wins + ?,
                                                  num_of_losses = num_of_losses + ?,
                                                  sum_of_opponents_ratings = sum_of_opponents_ratings + ?
                                                  WHERE username = ?""", (int(win), int(not win), opponent_rating, username))
        # Update the users stats, by converting win to a int since int(True) = 1 and int(False) = 0
        self.userDB_conn.commit()
        self.userDB_cur.execute("""UPDATE users SET elo = (sum_of_opponents_ratings + 400 * (num_of_wins - num_of_losses)) / (num_of_wins + num_of_losses)
                                                  WHERE username = ?""", (username,))
        self.userDB_conn.commit()

    def get_links(self, isOutgoing: bool, pageID: int) -> List[int]:
        """Gets the links for a page
        Parameters: isOutgoing: (if true gets outgoing links else gets incoming links)
                   pageID
        returns: A list of pageIDs that this page link to"""
        direction = "outgoing_links" if isOutgoing else "incoming_links"
        self.wikiDB_cur.execute("SELECT {} FROM links WHERE pageID = ?".format(direction), (pageID,))
        links = self.wikiDB_cur.fetchone()
        if links == None: return []  # If no links for this page return the empty list
        return list(map(int, links[0].split("|")))  # Convert the | separated values to a list of ints

    def get_titles(self, pageIDs: List[int]) -> Dict[int, str]:
        """Gets the titles of pages
        Parameters: a list of the pageIDs
        Returns: A dictionary with key of the pageID and value of page title, if no pageID exist then it will not be included"""
        output = {}
        for pageID in pageIDs:
            self.wikiDB_cur.execute("SELECT page_title FROM page_titles WHERE pageID = ?", (pageID,))
            page_title = self.wikiDB_cur.fetchone()
            if page_title:
                output[pageID] = page_title[0]
        return output

    def close(self):
        """Close the database"""
        self.userDB_conn.close()
        self.wikiDB_conn.close()

    def get_random_pageID(self) -> int:
        """Get a random pageID
        returns: a random pageID"""
        self.wikiDB_cur.execute("SELECT pageID FROM page_titles ORDER BY RANDOM() LIMIT 1")
        return self.wikiDB_cur.fetchone()[0]

if __name__ == "__main__":
    x = Database()
    print(x.get_password("Ben"))
    print(x.get_password("Test"))
    print(x.get_leaderboard())
    print(x.update_player_elo("Ben", False, "Test1"))
    print(x.get_leaderboard())
    print(x.get_titles([12]))
    print(x.get_titles([12, 25, 39, 290, 5]))
    print(x.get_link_counts(False, [12, 25, 39]))
    print(x.get_link_counts(True, [12, 25, 39]))
    print(x.get_links(True, 12))
    print(x.get_random_pageID())
    x.close()
