from collections import Counter
assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

"""
Cross product of elements in A and elements in B."
"""
def cross(A, B):
    return [s+t for s in A for t in B]

boxes = cross(rows, cols) # Individual boxes in grid
row_units = [cross(r, cols) for r in rows] #Rows boxes in grid
column_units = [cross(rows, c) for c in cols] #Column boxed in grid
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')] # 3x3 square units
diag1 = [a[0]+a[1] for a in zip(rows,cols)] # Boxes which form the diagonal in grid
diag2 = [a[0]+a[1] for a in zip(rows,cols[::-1])] # Boxes which form the diagonal in grid
 
unitlist = row_units + column_units + square_units +[diag1]+[diag2]
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    This function is used to update the values in dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    
    return values

"""
In this function, we evaluate each unit repeatedly to remove numbers from possible values. 
Unit in this case can be either a row, a column or a grid.Within the unit we look for cells 
with only two possibilties and check if there are duplicates to it.We can detect digits in the duplicates 
which cannot be used among other cells in the unit
"""

def naked_twins(grid):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    #Consider each of the unit in the entire unitlist.A unit, can be a single row/column/squareunit/diagonal
    for unit in unitlist:
        unit_count = {k:v for k, v in grid.items() if k in unit}       
        #Build a counter for each of the item values in the unit. 
        unit_count = Counter(unit_count.values())
        #Lets go through each of the item in the given unit, looking for naked twins
        for item in unit:
            value = grid[item]
            #If any 2-digit item value has counter > 2,means we have spotted naked twins 
            #We now proceed to remove digits in naked_twins from other cells in the unit
            if unit_count[value] >=2 and len(value) == 2:
                # check across all items in the unit except for naked twins and solved items
                for item_inner in unit:
                    if grid[item_inner] != value and len(grid[item_inner]) >= 2:
                        # consider each number/digit in the item value, remove those from boxes 
                        for num in value:
                            if num in grid[item_inner]:
                                grid[item_inner] = grid[item_inner].replace(num, '')

    return grid

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
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
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

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    #solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    # Choose one of the unfilled squares with the fewest possibilities
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
    # If you're stuck, see the solution.py tab!

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    #print("inside solve")
    values = grid_values(grid)
    values = search(values)
    if values is False:
        return False ## Failed earlier
    else:
        return values
        
 #  print("diagnal",diag2)
    
if __name__ == '__main__':

    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
