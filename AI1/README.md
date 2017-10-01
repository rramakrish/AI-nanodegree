# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: constraints are conditions imposed which must be met by variables. In the Naked twins problem, the constraint is if 2 cells which are on the same row, column or box in a sudoku grid have identical 2 digit numbers - then no other cell in the row, column or square can have either of the digits. To solve this we first identify the twins and the column, row or square they belong, then iterate through the identified columns, rows and boxes to eliminate any occurrences of either of the 2 digits thereby dramatically reducing the possibilities of numbers that are the right fit within each box.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: First step is to model the Diagonals of the square in a row/column format (example A1, B2, C3...& A9, B8, C7...) and now along with the rows, columns and squares the diagonals should be included as units in the unit list. Once we have that modeled we should recursively apply breadth first search , elimination and only choice techniques to arrive at one possible answer for the cell & finally solving the sudoku

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `test_solution.py` - Do not modify this. You can test your solution by running `python -m unittest`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.
