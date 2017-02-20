# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver
This is an extended implementation of Sudoku Solver project of AIND program to use naked-twin strategy and to cover diagonal sudoku scenario.

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  

A: Constraint propagation is the technique of applying constraints locally in a subset of original search space and propagating it across the whole space to solve the problem.  In naked twins 
strategy we identify a pair of boxes located in the same unit that would ensure that those twin values can be safely eliminated from other boxes in their respective units. As we repeat this across 
the search space we would have potentially eliminated several redundant elements remaining in the whole space.

The implementation would involve identifying all the boxes that have twins (boxes with only two elements in the same unit), then identifying a set of naked twins (twins that are with the same values in the same unit). Then we remove the corresponding digits from all the respective peers of each of the twins.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  

A: Original sudoku uses the constraints that require the sudoku uniqueness in row units, column units and the 3x3 square units.  
In order to make it diagonal sudoku it would be necessary to add the right diagonal and left diagonal entries to the constraints.  
Thus we propagate the constraings beyond the 3 original units to add these 2 additional units.  This will ensure that the solution set
we find satisfies the peer diagonal constraints of the 2 diagonal units also. 

### Install

This project requires **Python 3**.

This also uses [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 

##### Optional: Pygame

Pygame was used to test the project visually. pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - Core solution.
* `solution_test.py` - Test provided for validating.  Run as: `python solution_test.py`.
* `PySudoku.py` - Code for visualizing the solution.
* `visualize.py` - Code for visualizing the solution.

### Visualizing

To visualize your solution, ```assign_values``` function was used in the solution.py.