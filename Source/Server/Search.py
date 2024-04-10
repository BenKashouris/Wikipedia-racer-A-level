"""Module defining a bidirection breadth first search"""
from typing import Dict, List, Set
import time

def bi_bfs(start_pageID: int, end_pageID: int, database):
    """Bidirectional breadth first search between two pageIDs
    parameters: start_pageID, the start node of the search
                end_pageID, the end node of the search
                database, a database object used to find the next page
    returns: A list of list of int with each sub list being each pageID in the path between each path"""
    forwards_parents: Dict[int: int] = {}
    backwards_parents: Dict[int: int] = {}

    forwards_unvisited: List[int] = [start_pageID]
    backwards_unvisited: List[int] = [end_pageID]

    forwards_visted: Set[int] = {start_pageID}
    backwards_visted: Set[int] = {end_pageID}

    if start_pageID == end_pageID: return [[start_pageID, end_pageID]]

    start_time = time.time()
    while True:
        v = forwards_unvisited.pop(0)  # Search forward
        for e in database.get_links(True, v):
            if not e in forwards_visted:
                forwards_unvisited.append(e)
                forwards_visted.add(e)
                forwards_parents[e] = v

        middle_nodes = forwards_visted.intersection(backwards_visted)  # Check for intersections
        if middle_nodes != set():
            break

        v = backwards_unvisited.pop(0)  # Search Backwards
        for e in database.get_links(False, v):
            if not e in backwards_visted:
                backwards_unvisited.append(e)
                backwards_visted.add(e)
                backwards_parents[e] = v

        middle_nodes = forwards_visted.intersection(backwards_visted)  # Check for intersections
        if middle_nodes != set():
            break

        if time.time() - start_time > 20: # If we have been searching for more than 20 seconds stop
            return -1

    paths = []
    for i in middle_nodes:
        paths.append(expand_from_middle(forwards_parents, backwards_parents, i, start_pageID, end_pageID))
    return paths

def expand_from_middle(forwards_parents, backwards_parents, middle_node, start_node, end_node) -> List[int]:
    """Find the path of a node from the middle node
    returns: a list of integers the fist element the start_node and the last element the end_node"""
    x = [middle_node]
    while x[-1] != end_node:
        x.append(backwards_parents[x[-1]])
    while x[0] != start_node:
        x.insert(0, forwards_parents[x[0]])
    return x

if __name__ == "__main__":   
    ## https://en.wikipedia.org/?curid=  url for looking up a wikipage by pageid
    import Database
    def print_path(path):
        p = x.get_titles(path)
        path = list(map(lambda e: p.get(e), path))
        print(" -> ".join(path))
    x = Database.Database()
    print(bi_bfs(30598, 1577493, x))
    for m in bi_bfs(30598, 1577493, x):
        print_path(m)