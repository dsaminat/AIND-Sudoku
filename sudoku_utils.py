#Utility / Helper methods and definitions for Sudoku

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

# Utility : Display values
def display(values, boxes, rows, cols):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

