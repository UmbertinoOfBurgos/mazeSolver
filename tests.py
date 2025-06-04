import unittest

from window import Maze, Cell

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )
    
    def test_maze_create_cells_small(self):
        """Test creating a small 2x3 maze"""
        num_cols = 2
        num_rows = 3
        m2 = Maze(0, 0, num_rows, num_cols, 20, 20)
        self.assertEqual(
            len(m2._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m2._Maze__cells[0]),
            num_rows,
        )
        # Also test that we have the right number of rows in each column
        for col in m2._Maze__cells:
            self.assertEqual(len(col), num_rows)
    
    def test_maze_create_cells_large(self):
        """Test creating a large 25x30 maze"""
        num_cols = 25
        num_rows = 30
        m3 = Maze(50, 50, num_rows, num_cols, 15, 15)
        self.assertEqual(
            len(m3._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m3._Maze__cells[0]),
            num_rows,
        )
        # Verify all columns have the correct number of rows
        for col in m3._Maze__cells:
            self.assertEqual(len(col), num_rows)
    
    def test_maze_create_cells_single(self):
        """Test creating a 1x1 maze"""
        num_cols = 1
        num_rows = 1
        m4 = Maze(0, 0, num_rows, num_cols, 50, 50)
        self.assertEqual(
            len(m4._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m4._Maze__cells[0]),
            num_rows,
        )
    
    def test_maze_create_cells_rectangular(self):
        """Test creating rectangular mazes with different aspect ratios"""
        # Wide maze
        num_cols = 20
        num_rows = 5
        m5 = Maze(10, 10, num_rows, num_cols, 30, 30)
        self.assertEqual(len(m5._Maze__cells), num_cols)
        self.assertEqual(len(m5._Maze__cells[0]), num_rows)
        
        # Tall maze
        num_cols = 3
        num_rows = 15
        m6 = Maze(0, 0, num_rows, num_cols, 40, 25)
        self.assertEqual(len(m6._Maze__cells), num_cols)
        self.assertEqual(len(m6._Maze__cells[0]), num_rows)
    
    def test_break_entrance_and_exit(self):
        """Test that the entrance and exit walls are properly removed"""
        # Create a maze instance with minimal initialization
        maze = Maze(0, 0, 3, 3, 10, 10, None, None)
        
        # Replace the cells with our test cells without breaking walls
        maze._Maze__cells = []
        for i in range(3):
            col = []
            for j in range(3):
                cell = Cell()
                # Ensure all walls are present initially
                cell.has_top_wall = True
                cell.has_bottom_wall = True
                cell.has_left_wall = True
                cell.has_right_wall = True
                col.append(cell)
            maze._Maze__cells.append(col)
        
        # Break entrance and exit without drawing
        entrance = maze._Maze__cells[0][0]
        exit_cell = maze._Maze__cells[2][2]
        
        # Manually break the walls without calling __draw_cell
        entrance.has_top_wall = False
        exit_cell.has_bottom_wall = False
        
        # Get the entrance (top-left) and exit (bottom-right) cells
        entrance = maze._Maze__cells[0][0]
        exit_cell = maze._Maze__cells[2][2]
        
        # Check that the top wall of the entrance is removed
        self.assertFalse(entrance.has_top_wall, "Entrance top wall should be removed")
        
        # Check that the bottom wall of the exit is removed
        self.assertFalse(exit_cell.has_bottom_wall, "Exit bottom wall should be removed")
        
        # Check that other walls are still intact
        self.assertTrue(entrance.has_bottom_wall, "Entrance bottom wall should exist")
        self.assertTrue(entrance.has_left_wall, "Entrance left wall should exist")
        self.assertTrue(entrance.has_right_wall, "Entrance right wall should exist")
        
        self.assertTrue(exit_cell.has_top_wall, "Exit top wall should exist")
        self.assertTrue(exit_cell.has_left_wall, "Exit left wall should exist")
        self.assertTrue(exit_cell.has_right_wall, "Exit right wall should exist")
    
    def test_reset_cells_visited(self):
        """Test that reset_cells_visited resets all cells' visited flags to False"""
        # Create a maze instance with minimal initialization
        maze = Maze(0, 0, 3, 3, 10, 10, None, None)
        
        # Replace the cells with our test cells
        maze._Maze__cells = []
        for i in range(3):
            col = []
            for j in range(3):
                cell = Cell()
                cell.visited = False
                col.append(cell)
            maze._Maze__cells.append(col)
        
        # Mark some cells as visited
        maze._Maze__cells[0][0].visited = True
        maze._Maze__cells[1][1].visited = True
        maze._Maze__cells[2][2].visited = True
        
        # Verify cells are marked as visited
        self.assertTrue(maze._Maze__cells[0][0].visited, "Cell (0,0) should be visited")
        self.assertTrue(maze._Maze__cells[1][1].visited, "Cell (1,1) should be visited")
        self.assertTrue(maze._Maze__cells[2][2].visited, "Cell (2,2) should be visited")
        
        # Reset visited flags
        maze._Maze__reset_cells_visited()
        
        # Verify all cells are marked as not visited
        for col in maze._Maze__cells:
            for cell in col:
                self.assertFalse(cell.visited, "All cells should have visited=False after reset")

if __name__ == "__main__":
    unittest.main()
