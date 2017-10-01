assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

d1_units = []
d2_units = []
diagonals = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]


def getDiagonal1():
    """Eliminate values using the naked twins strategy.
    Args:
        none

    Returns:
        diagonal 1 - [A1,B2,C3,D4,E5,F6,G7,H8,I9].
    """
    d=[]
    i=0
    for val in cols:
        d.append(rows[i]+val)
        i=i+1
    return d

def getDiagonal2():
    """Eliminate values using the naked twins strategy.
    Args:
        none

    Returns:
        diagonal 2 - [A9,B8,C7,D6,E5,F4,G3,H2,I1].
    """
    d=[]
    i=0
    for val in cols[::-1]:
        d.append(rows[i]+val)
        i=i+1
    return d

d1_units = getDiagonal1()
d2_units = getDiagonal2()
diagonals.append(d1_units)
diagonals.append(d2_units)


#form the unitlist of rows columns boxes/squares and diagonals
unitlist = row_units + column_units + square_units + diagonals
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)



def assign_value(values, box, value):
    """
    Assigns a value to a given box. If it updates the board record it.

    Returns:
        dictionary with assigned values
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    twin = 0
    for unit in unitlist: #for every unit (row, column, box, diagonal)
        for i in range(0, len(unit)): # setup 2 counters within every unit i and j
            for j in range(i+1, len(unit)):
                if(len(values[unit[i]]) == 2):#check the length of the values in the cell
                    if(values[unit[i]] == values[unit[j]]): #check if exact match is found elsewhere in the unit
                        twin = values[unit[i]]
                        twin_key=unit[i] #get the location where the value was found
                        for box in unit:#iterate throuh the unit
                        # and for every digit in the twin check an occurance in the cell (except the cell with exact match)
                            if((twin[0] in values[box]) or (twin[1] in values[box])):
                                if(twin != values[box]):
                                    #eliminate the occurances
                                    temp = values[box].replace(twin[0],'')
                                    values[box] = temp.replace(twin[1],'')
    return values




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

    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
    values =  dict(zip(boxes, grid))
    for key in values.keys():
        value = values.get(key)
        if (value == "."):# if value is . replace it with 123456789
            value = '123456789'
            values[key] = value
    return values

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
    loop through the peers of each cell and eliminate occurances of the value which is the
    right fit for the cell

    Args:
        values(dict): The sudoku in dictionary form
    """

    for key in values.keys():  #for every cell in dict
        value = values.get(key) #get the value
        if (len(value) == 1):
            value_in_grid = value
            peer_values = peers.get(key) #get all peers
            for peer_value in peer_values: #for all peers
                peer_val_grid = values.get(peer_value)
                if (value_in_grid in peer_val_grid):#if the value is in any of the peer value
                    new_peer_val_grid = peer_val_grid.replace(value_in_grid,'')#eliminate the value from peer
                    values[peer_value] = new_peer_val_grid #assign it to the dict

    return values

def only_choice(values):
    """
    loop through unit find a cell with a number 1-10
    if found and that is the only number is the cell then
    pin that number to the cell

    Args:
        values(dict): The sudoku in dictionary form
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1: # if this is the only number (length of the cell is 1)
                #this number is the only choice, add it to the cell.
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """ This is a  function, that first calls eliminate values to eliminate
        possibilites and only choice
        Function also checks to see if everytime this function runs there are more values determined
        if not, this means that the function will not reduce possibilites anymore and will return
        Args:
            values(dict): The sudoku in dictionary form
        return:
            dictionary only if no new numbers are eliminated from the cells
    """



    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        # Your code here: Use the Only Choice Strategy

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    """ This is a recursive function, that first calls reduce_puzzle to eliminate
        possibilites and reduces the soduku to as much as possible to apply
        depth-first search
        Args:
            values(dict): The sudoku in dictionary form
        return:
            final solved soduku (if length of each cell is 1)
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    input_dict = grid_values(grid) #get a 9X9 grid representation in rowsXcolumn form
    return search(input_dict) # call search


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
