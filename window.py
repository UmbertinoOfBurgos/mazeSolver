from tkinter import Tk, Canvas, BOTH
import time

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2
    
    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(
            self.point1.x, self.point1.y,
            self.point2.x, self.point2.y,
            fill=fill_color, width=2
        )

import random

class Cell:
    def __init__(self, win: 'Window' = None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = win
    
    def draw(self, x1: int, y1: int, x2: int, y2: int):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        
        if self.__win is None:
            return
        
        # Draw left wall (or erase it if it doesn't exist)
        line = Line(Point(x1, y1), Point(x1, y2))
        self.__win.draw_line(line, "black" if self.has_left_wall else "white")
        
        # Draw top wall (or erase it if it doesn't exist)
        line = Line(Point(x1, y1), Point(x2, y1))
        self.__win.draw_line(line, "black" if self.has_top_wall else "white")
        
        # Draw right wall (or erase it if it doesn't exist)
        line = Line(Point(x2, y1), Point(x2, y2))
        self.__win.draw_line(line, "black" if self.has_right_wall else "white")
        
        # Draw bottom wall (or erase it if it doesn't exist)
        line = Line(Point(x1, y2), Point(x2, y2))
        self.__win.draw_line(line, "black" if self.has_bottom_wall else "white")
    
    def draw_move(self, to_cell, undo=False):
        """
        Draw a line from the center of this cell to the center of another cell
        
        Args:
            to_cell: The target cell to draw a line to
            undo: If True, draw the line in gray (for backtracking)
        """
        if not isinstance(to_cell, Cell):
            raise TypeError("to_cell must be an instance of Cell")
            
        # Check if cells are properly initialized
        if any(coord < 0 for coord in [self.__x1, self.__y1, self.__x2, self.__y2]):
            raise ValueError("Source cell is not properly initialized")
            
        if any(coord < 0 for coord in [to_cell.__x1, to_cell.__y1, to_cell.__x2, to_cell.__y2]):
            raise ValueError("Target cell is not properly initialized")
        
        try:
            # Calculate center of current cell
            center_x1 = (self.__x1 + self.__x2) // 2
            center_y1 = (self.__y1 + self.__y2) // 2
            
            # Calculate center of target cell
            center_x2 = (to_cell.__x1 + to_cell.__x2) // 2
            center_y2 = (to_cell.__y1 + to_cell.__y2) // 2
            
            # Choose color based on undo flag
            color = "gray" if undo else "red"
            
            # Only draw if window exists
            if self.__win is not None:
                # Create and draw the line
                line = Line(Point(center_x1, center_y1), Point(center_x2, center_y2))
                self.__win.draw_line(line, color)
        except Exception as e:
            raise RuntimeError(f"Failed to draw move between cells: {e}")

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        # Input validation
        if num_rows <= 0 or num_cols <= 0:
            raise ValueError("Number of rows and columns must be positive")
        if cell_size_x <= 0 or cell_size_y <= 0:
            raise ValueError("Cell dimensions must be positive")
            
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []
        
        # Set the random seed if provided
        if seed is not None:
            random.seed(seed)
            
        self.__create_cells()
    
    def __create_cells(self):
        """Create a 2D list of Cell objects and draw them"""
        # Initialize the 2D list - columns first, then rows
        for i in range(self.__num_cols):
            column = []
            for j in range(self.__num_rows):
                cell = Cell(self.__win)
                column.append(cell)
            self.__cells.append(column)
        
        # Draw all the cells
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__draw_cell(i, j)
        
        # Break the entrance and exit walls
        self.__break_entrance_and_exit()
        
        # Start the recursive wall-breaking from the top-left corner
        if self.__num_cols > 0 and self.__num_rows > 0:
            self.__break_walls_r(0, 0)
            
        # Reset all cells' visited flags for future use
        self.__reset_cells_visited()
    
    def __draw_cell(self, i, j):
        """Draw a cell at column i, row j"""
        # Calculate the x/y position based on i/j and cell size
        x1 = self.__x1 + i * self.__cell_size_x
        y1 = self.__y1 + j * self.__cell_size_y
        x2 = x1 + self.__cell_size_x  
        y2 = y1 + self.__cell_size_y
        
        # Draw the cell
        self.__cells[i][j].draw(x1, y1, x2, y2)
        
        # Animate the drawing
        self.__animate()
    
    def __break_walls_r(self, i, j):
        """
        Recursively break walls to create a maze using depth-first search
        
        Args:
            i: column index of current cell
            j: row index of current cell
        """
        # Mark the current cell as visited
        current = self.__cells[i][j]
        current.visited = True
        
        while True:
            # List to store possible directions to move (i, j, direction)
            to_visit = []
            
            # Check all four possible directions
            # Left
            if i > 0 and not self.__cells[i-1][j].visited:
                to_visit.append((i-1, j, "left"))
            # Right
            if i < self.__num_cols - 1 and not self.__cells[i+1][j].visited:
                to_visit.append((i+1, j, "right"))
            # Up
            if j > 0 and not self.__cells[i][j-1].visited:
                to_visit.append((i, j-1, "up"))
            # Down
            if j < self.__num_rows - 1 and not self.__cells[i][j+1].visited:
                to_visit.append((i, j+1, "down"))
            
            # If no directions to go, draw the cell and return
            if not to_visit:
                self.__draw_cell(i, j)
                return
            
            # Choose a random direction to go
            next_i, next_j, direction = random.choice(to_visit)
            next_cell = self.__cells[next_i][next_j]
            
            # Break the walls between current cell and next cell
            if direction == "left":
                current.has_left_wall = False
                next_cell.has_right_wall = False
            elif direction == "right":
                current.has_right_wall = False
                next_cell.has_left_wall = False
            elif direction == "up":
                current.has_top_wall = False
                next_cell.has_bottom_wall = False
            elif direction == "down":
                current.has_bottom_wall = False
                next_cell.has_top_wall = False
            
            # Draw the cells to show the wall removal
            self.__draw_cell(i, j)
            self.__draw_cell(next_i, next_j)
            
            # Recursively visit the next cell
            self.__break_walls_r(next_i, next_j)
    
    def __reset_cells_visited(self):
        """Reset the visited flag of all cells to False"""
        for col in self.__cells:
            for cell in col:
                cell.visited = False
    
    def __break_entrance_and_exit(self):
        """
        Remove the top wall of the entrance (top-left cell) and 
        the bottom wall of the exit (bottom-right cell)
        """
        if not self.__cells:
            return
            
        # Break the entrance (top-left cell)
        entrance = self.__cells[0][0]
        entrance.has_top_wall = False
        self.__draw_cell(0, 0)
        
        # Break the exit (bottom-right cell)
        exit_row = self.__num_rows - 1
        exit_col = self.__num_cols - 1
        if exit_row >= 0 and exit_col >= 0:
            exit_cell = self.__cells[exit_col][exit_row]
            exit_cell.has_bottom_wall = False
            self.__draw_cell(exit_col, exit_row)
    
    def solve(self):
        """
        Solve the maze using depth-first search
        Returns True if a solution was found, False otherwise
        """
        return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        """
        Recursively solve the maze using depth-first search
        
        Args:
            i: current column index
            j: current row index
            
        Returns:
            bool: True if the end was reached, False otherwise
        """
        # Animate the current step
        self.__animate()
        
        # Mark the current cell as visited
        current = self.__cells[i][j]
        current.visited = True
        
        # If we've reached the end cell, return True
        if i == self.__num_cols - 1 and j == self.__num_rows - 1:
            return True
        
        # Define possible moves: (new_i, new_j, direction, wall_attr, opposite_wall_attr)
        moves = [
            (i-1, j, "left", "has_left_wall", "has_right_wall"),    # Left
            (i+1, j, "right", "has_right_wall", "has_left_wall"),   # Right
            (i, j-1, "up", "has_top_wall", "has_bottom_wall"),      # Up
            (i, j+1, "down", "has_bottom_wall", "has_top_wall")     # Down
        ]
        
        # Try each possible direction
        for new_i, new_j, direction, wall_attr, opposite_wall_attr in moves:
            # Check if the move is within bounds
            if 0 <= new_i < self.__num_cols and 0 <= new_j < self.__num_rows:
                next_cell = self.__cells[new_i][new_j]
                
                # Check if we can move in this direction
                if not getattr(current, wall_attr) and not next_cell.visited:
                    # Draw the move
                    current.draw_move(next_cell)
                    
                    # Recursively try to solve from the next cell
                    if self._solve_r(new_i, new_j):
                        return True
                    
                    # If we get here, the path didn't lead to the end
                    # Undo the move
                    current.draw_move(next_cell, undo=True)
        
        # If no direction worked, return False
        return False
    
    def __animate(self):
        """Animate the drawing by redrawing and sleeping briefly"""
        if self.__win is not None:
            self.__win.redraw()
            time.sleep(0.05)

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Cell Demo")
        self.__canvas = Canvas(self.__root, width=width, height=height, bg="white")
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
    
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.__canvas, fill_color)
    
    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
    
    def close(self):
        self.__running = False
