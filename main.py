import time
from tkinter import Tk, Canvas, BOTH
from window import Window, Cell, Maze

def create_and_display_maze(win, x, y, rows, cols, cell_width, cell_height, title, seed=None):
    """Helper function to create and display a maze with error handling"""
    print(f"Creating {rows}x{cols} maze...")
    try:
        maze = Maze(x, y, rows, cols, cell_width, cell_height, win, seed=seed)
        print(f"Successfully created {rows}x{cols} maze")
        return maze
    except Exception as e:
        print(f"Error creating maze: {e}")
        return None

def main():
    try:
        # Create a window for the small maze
        win = Window(800, 600)
        
        # Test with a small maze first (3x3)
        # Using a fixed seed (0) for consistent results during development
        maze_small = create_and_display_maze(win, 50, 50, 3, 3, 50, 50, "Small Maze", seed=0)
        
        # Wait a bit before creating the larger maze
        print("Waiting before creating larger maze...")
        time.sleep(2)
        
        # Create a window for the larger maze
        win2 = Window(1000, 800)
        
        # Create a larger maze (10x15)
        # Using the same seed for consistent results
        maze_large = create_and_display_maze(win2, 50, 50, 10, 15, 60, 50, "Large Maze", seed=0)
        
        # Solve the maze
        if maze_large:
            print("Solving the maze...")
            solved = maze_large.solve()
            if solved:
                print("Maze solved!")
            else:
                print("No solution found for the maze.")
        
        if maze_large and hasattr(maze_large, '_Maze__cells') and maze_large._Maze__cells:
            try:
                # Test draw_move with error handling
                if len(maze_large._Maze__cells) > 1 and len(maze_large._Maze__cells[0]) > 1:
                    # Draw a red move from (0,0) to (1,0)
                    maze_large._Maze__cells[0][0].draw_move(maze_large._Maze__cells[1][0])
                    time.sleep(0.5)
                    
                    # Draw a gray (undo) move from (1,0) to (1,1)
                    if len(maze_large._Maze__cells[0]) > 1:  # Check if there's a cell at (1,1)
                        maze_large._Maze__cells[1][0].draw_move(maze_large._Maze__cells[1][1], undo=True)
                        time.sleep(0.5)
                    
                    # Draw another red move from (1,1) to (2,1)
                    if len(maze_large._Maze__cells) > 2 and len(maze_large._Maze__cells[1]) > 1:
                        maze_large._Maze__cells[1][1].draw_move(maze_large._Maze__cells[2][1])
            except Exception as e:
                print(f"Error during maze drawing: {e}")
        
        # Keep the window open
        win2.wait_for_close()
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Maze demo completed.")

if __name__ == "__main__":
    main()
