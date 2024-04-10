import tkinter as tk
from typing import Dict, Tuple, List
from Colors import COLORS


class DirectedGraph(tk.Frame):
    """Object which displays a graph
    Parameters: root: a tkinter Tk object for the widget to be displayed in
                depths: A dictionary of depths with a key of the integer of the depth to display a node and a value of a tuple of strings of the text to display in the node
                edges: A dictionary of Tuple of 2 integers the key representing the i j of the start node and the value the i j of the end node
    Internal x and y refer to the pixel coordinates and i and j refer to the grid cooridnates of each node"""
    def __init__(self, root, depths: Dict[int, Tuple[str, ...]], edges: Tuple[Tuple[int, int], Tuple[int, int]], text_color = "Black"):
        tk.Frame.__init__(self, root)
        self._c: tk.Canvas = tk.Canvas(self)  # create canvas that will be drawn on
        self._c.pack(expand = 1, fill = tk.BOTH)
        self.bind("<Configure>", self.resize)  # Whenever the widget is resized call resize

        self._vertices: List[_vertex] = []  
        self._edges: Tuple[Tuple[int, int], Tuple[int, int]] = edges
        self.text_color = text_color
        self.max_i, self.max_j = max(depths.keys()), 0 
        self.dx, self.dy = 0, 0 # The difference in x/y between each node
       
        for i in depths.keys():
            self.max_j = max(self.max_j, len(depths[i]))
            for j, text in enumerate(depths[i]):
                self._vertices.append(_vertex(i, j, text)) 

    def draw_vertices(self):
        """Draw the vertices to the graph"""
        r = min(max(0.05 * (self.dx + 2 * self.dy), 10), self.dy)  # Calulate the radius of the circles. This is the average of dy and dx with a min of 10 and a max of dy
        for v in self._vertices:
            i, j = v.get_grid_coords()
            x, y = self._calc_x_y(i, j) # Calculating the on screen coordinates
            self._create_circle(x, y, r, fill = "white")
            self._create_text(x, y, v.text, fill = self.text_color)

    def _calc_dx_dy(self):
        """Calucalte dx and dy for the current width height"""
        self.dx = self.get_width_height()[0] / (self.max_i + 2)  # Plus 2 as to make sure end-nodes are not on the edge of the widget 
        self.dy = self.get_width_height()[1] / (self.max_j + 1) 

    def draw_edges(self):
        """Draw the edges to the graph"""
        for (i1, j1), (i2, j2) in self._edges:
            x1, y1 = self._calc_x_y(i1, j1)
            x2, y2 = self._calc_x_y(i2, j2)
            self._create_line(x1, y1, x2, y2)

    def _calc_x_y(self, i, j):
        """Calculate a (x,y) point for a (i, j) point 
           Parameter: i and j colums index
           Returns: x and y given by that i and j"""
        return i * self.dx + self.dx, j * self.dy + self.dy

    def _create_line(self, x1, y1, x2, y2, **kwargs):
        """Creates a line between (x1, y1) to (x2, y2) on the canvas"""
        self._c.create_line(x1, y1, x2, y2, **kwargs)
            
    def __getitem__(self, index: Tuple[int, int]):
        """Paramater: index: a tuple of the i and j of a vertex
        Returns: A vertex object at that grid position"""
        for v in self._vertices:
            if v.get_grid_coords == index:
                return v

    def get_width_height(self):
        """Returns: The x and y of the frame currently"""
        return (self.winfo_width(), self.winfo_height())

    def _create_text(self, x, y, text, **kwargs):
        """Create text at (x, y) on the canvas"""
        return self._c.create_text(x, y, text = text, **kwargs)

    def _create_circle(self, x, y, r, **kwargs):
        """Draws a circle radius r to the canvas at (x,y)"""
        return self._c.create_oval(x-r, y-r, x+r, y+r, **kwargs)
       
    def _clear(self):
        """Clears the canvas"""
        self._c.delete("all")

    def resize(self, e: tk.Event):
        """Resizing the frame"""
        self._clear()
        self._calc_dx_dy()
        self.draw_edges()
        self.draw_vertices()


class _vertex():
    """Object which stores the data for a vertex"""
    def __init__(self, i, j, text):
        self.i, self.j, self.text = i, j, text

    def get_grid_coords(self):
        return (self.i, self.j)

if __name__ == "__main__":
    depths = {0: ('108095',),
              1: ("43583", "4239", "42343"),
              2: ("5353", "2764", "578478", "215432", "4637"),
              3: ('923867', '427303', '62649', '64238', '12353', '980964', '53846', '2846'),
              4: ('836553',)}
    edges = (
             ((0, 0), (1,0)), ((0, 0), (1, 1)), ((0, 0), (1, 2)),
             ((1, 0), (2, 0)), ((1, 0), (2, 1)), ((1, 1), (2, 2)), ((1, 2), (2, 3)), ((1, 2), (2, 4)),
             ((2, 0), (3, 0)), ((2, 0), (3, 1)), ((2, 0), (3, 2)), ((2, 1), (3, 3)), ((2, 2), (3, 4)), ((2, 3), (3, 5)), ((2, 4), (3, 6)), ((2, 4), (3, 7)),
             ((3, 0), (4, 0)), ((3, 1), (4, 0)), ((3, 2), (4, 0)), ((3, 3), (4, 0)), ((3, 4), (4, 0)), ((3, 5), (4, 0)), ((3, 6), (4, 0)), ((3, 7), (4, 0))
             )

    root = tk.Tk()
    g = DirectedGraph(root, depths, edges, text_color= COLORS.HYPERLINK_BLUE)
    g.pack(expand = 1, fill = tk.BOTH)
    root.mainloop()