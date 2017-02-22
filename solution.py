import sys
import logging
from sudoku_utils import cross, display

# Assigned board positions for displaying in pygame
assignments = []

# Board configuration
rows = 'ABCDEFGHI'
cols = '123456789'
logger = logging.getLogger('sudoku logger')

# Basic definitions of board elements
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
cols_inv = cols[::-1]
#diagA_units = [[rows[i]+cols[i] for i in range(len(rows))]]
#diagB_units = [[rows[i]+cols_inv[i] for i in range(len(rows))]]
diagonal_units = [[r+c for r,c in zip(rows,cols)], [r+c for r,c in zip(rows,cols[::-1])]]

unitlist = row_units + column_units + square_units + diagonal_units #diagA_units + diagB_units
boxes = cross(rows, cols)
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

# Update assignments
def assign_value(values, box, value):
    """
    Function to update values dictionary.
    Assigns a value to a given box. If it updates the board it is recorded here.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
        logger.info('Assigned: ' + value)
    return values

# Strategy: Naked twins
def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    naked_twins = find_twins(values)
    values = eliminate_twins(naked_twins, values)
    return values

def find_twins(values):
    """Find all instances of naked twins"""
    # Find all boxes with twins
    all_twins = [box for box in values.keys() if len(values[box]) == 2]
    # Filter the naked twins out of all the twins found
    naked_twins = [[boxA,boxB] for boxA in all_twins \
        for boxB in peers[boxA] \
        if set(values[boxA])==set(values[boxB]) ]
    return naked_twins

def eliminate_twins(naked_twins, values):
    """Eliminate the naked twins as possibilities for their peers"""
    for i in range(len(naked_twins)):
        boxA = naked_twins[i][0]
        boxB = naked_twins[i][1]
        #Compute the intersection of the peers
        peersA = set(peers[boxA])
        peersB = set(peers[boxB])
        peers_int = peersA & peersB
        #Delete the two elements in the naked twins from all the common peers
        for peer_val in peers_int:
            if len(values[peer_val])>2:
                for rm_val in values[boxA]:
                    values = assign_value(values, peer_val, values[peer_val].replace(rm_val,''))
    return values

# Calculation: Grid values
def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81, "Input grid must be a string of length 81 (9x9)"
    return dict(zip(boxes, values))

# Strategy : Eliminate values
def eliminate(values):
    """ The strategy to eliminate values by removing single values from peer boxes"""
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
            values = assign_value(values, peer, values[peer])
    return values

# Strategy : Only choice 
def only_choice(values):
    """ Only choice strategy """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)
    return values

# Collective strategy : Reduce puzzle
def reduce_puzzle(values):
    """ Reduce using eliminate, only_choice, naked_twins strategies"""
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the Naked Twins Strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            logger.error('Box with zero available values found:' + values)
            return False
    return values

# Collective Strategy: Search
def search(values):
    """Using depth-first search and propagation, trying all possible values."""
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

# Solution overall
def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    result = grid_values(grid)
    result = search(result)
    return result

# Main program entry point
if __name__ == '__main__':
    """
    Note: Manually override the lowest-severity log message level
    that the logger will handle from the command line by executing with flags:
    i.e. python main.py --log=WARNING

    Sample usage:
        logger.debug('debug message')
        logger.info('info message')
        logger.warning('warn message')
        logger.error('error message')
    """

    # Create logger

    logger.setLevel('ERROR') # specifies lowest-severity log message a logger will handle

    if len(sys.argv):
        log_args = [arg for arg in sys.argv if '--log=' in arg]
        if len(log_args) > 0:
            logger.setLevel(get_log_level(log_args))

    # Get current logging level
    numeric_level = logging.getLogger().getEffectiveLevel()
    logger.info('Starting Sudoku')

    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    #diag_sudoku_grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

    display(solve(diag_sudoku_grid), boxes, rows, cols)

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    #except:
    #    logger.error('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

    logger.info('Finished Sudoku')