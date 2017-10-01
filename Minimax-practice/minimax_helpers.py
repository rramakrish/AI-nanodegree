
def terminal_test(gameState):
    """ Return True if the game is over for the active player
    and False otherwise.
    """
    return not bool(gameState.get_legal_moves())  # by Assumption 1


def min_value(gameState):
    """ Return the value for a win (+1) if the game is over,
    otherwise return the minimum value over all legal child
    nodes.
    """
    print("*********** min values move **********")
    if terminal_test(gameState):
        print("In Terminal Min value")
        return 1  # by Assumption 2
    v = float("inf")
    print("INSIDE MIN VALUES")
    for m in gameState.get_legal_moves():
        #print(m)
        #print("-----------------------------------")
        print(max_value(gameState.forecast_move(m)))
        v = min(v, max_value(gameState.forecast_move(m)))
        #print("++++++++++++++++++++++++++++++++++++")
        #print(v)
    return v


def max_value(gameState):
    """ Return the value for a loss (-1) if the game is over,
    otherwise return the maximum value over all legal child
    nodes.
    """
    print("*********** max values move **********")
    if terminal_test(gameState):
        print("In Terminal Max value")
        return -1  # by assumption 2
    v = float("-inf")
    print("INSIDE MAX VALUES")

    for m in gameState.get_legal_moves():
        #print(m)
        #print("-----------------------------------")
        v = max(v, min_value(gameState.forecast_move(m)))
        #print("++++++++++++++++++++++++++++++++++++")
        #print(v)
    return v
