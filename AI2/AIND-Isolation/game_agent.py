"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # If score < 0 then the game is lost by player
    if game.is_loser(player):
        return float("-inf")
    # If score > 0 then the game is won by player
    if game.is_winner(player):
        return float("inf")

    #human/coder player moves
    own_moves = len(game.get_legal_moves(player))
    #Computer player moves
    opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))
    #Play aggresive, if >0 human/coder wins, else computer player wins
    return float(own_moves - 2*opponent_moves)







def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # If score < 0 then the game is lost by player
    if game.is_loser(player):
        return float("-inf")
    # If score > 0 then the game is won by player
    if game.is_winner(player):
        return float("inf")

    # list of bad moves, if the player corners themselves to these positions rather than
    # playing in the center, the player had relatively more chance of losing
    bad_moves = [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),
                 (1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),
                 (7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7),
                 (1,7),(2,7),(3,7),(4,7),(5,7),(6,7)]
    '''bad_moves = [(0,0),(0,7),(7,0),(7,7)]'''
    player1_score = 0
    player2_score = 0
    game_location_1 = game.get_player_location(player)
    #Discredit players for playing in the corners. This is for player1 and player2
    if(game_location_1 in bad_moves):
        player1_score = player1_score-1
    game_location_2 = game.get_player_location(game.get_opponent(player))
    if(game_location_2 in bad_moves):
        player2_score = player2_score-1
    #If positive human/coder wins else computer player wins
    return float(player1_score - player2_score)

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # If score < 0 then the game is lost by player
    if game.is_loser(player):
        return float("-inf")
    # If score > 0 then the game is won by player
    if game.is_winner(player):
        return float("inf")

    blank_spaces = game.get_blank_spaces()
    own_moves = len(game.get_legal_moves(player))
    opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))
    # If the blankspaces are more then play more aggresively else play less aggresively
    if len(blank_spaces) >= 35:
        return float(own_moves - 3*opponent_moves)
    else:
        return float(3*own_moves - opponent_moves)



class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)
        if (len(game.get_legal_moves()) > 0):
            best_move = game.get_legal_moves()[0]


        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            return best_move  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()


        legal_moves = game.get_legal_moves() #get legal moves
        if not legal_moves or depth==0: #check for depth and not legal moves
           return self.score(game, self) # score self
        best_move=legal_moves[0] # Assign the first legal move to the best move
        # this is to avoid forefits
        best_score = float("-inf") # We are calling min first so, assign best score to -inf
        # nothing can be less than -inf
        for m in legal_moves:
            #Call the minimize function
            v = self.min_value(game.forecast_move(m),depth-1)# decrement depth
            # compare the best score with -inf, it will always be more than -inf
            if v >= best_score:
                best_score = v
                best_move = m
        # return the best move (m). This is the topmost level, hence we return
        # the best move
        return best_move



    def min_value(self,game,depth):
        """ Return the value for a win (+1) if the game is over,
        otherwise return the minimum value over all legal child
        nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()#get legal moves
        if not legal_moves or depth==0: #check for depth and not legal moves
           return self.score(game, self) # score self
        best_move=legal_moves[0]# Assign the first legal move to the best move
        # this is to avoid forefits
        best_score = float("inf")# We are calling max here so, assign best score to inf
        # nothing can be more than inf
        for m in legal_moves:
            best_score =min(best_score, self.max_value(game.forecast_move(m),depth-1)) # decrement depth
            # get the min of all the max values. First node was max, now its min
            #if score <= best_score:
            #   best_score = score
        return best_score # retrun best_score


    def max_value(self,game,depth):
        """ Return the value for a loss (-1) if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """
        #search_depth=1
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        legal_moves = game.get_legal_moves()#get legal moves
        if not legal_moves or depth==0:#check for depth and not legal moves
           return self.score(game, self)# score self
        best_move=legal_moves[0]# Assign the first legal move to the best move
        # this is to avoid forefits
        best_score = float("-inf")# We are calling max here so, assign best score to -inf
        # nothing can be less than inf so we can get the best score.
        for m in legal_moves:
            best_score =max(best_score, self.max_value(game.forecast_move(m),depth-1))# decrement depth
            # get the max of all the min values. First node was max then min, now its max
            #if score >= best_score:
            #    best_score = score
        return best_score # return best_score


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left


        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)
        best_move = legal_moves[0]
        depth=0
        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            while True:
                best_move = self.alphabeta(game, depth)
                depth=depth+1
            #return best_move

        except SearchTimeout:
            #pass  # Handle any actions required after timeout as needed
            return best_move

        # Return the best move from the last completed search iteration
        return best_move





    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        # Alpha beta follows the same pattern as min max, but takes in additional
        #parameters, alpha and beta
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()#get legal moves

        if not legal_moves:#not legal move, score self and return
            #return (-1,-1)
            return self.score(game, self)
        best_move=legal_moves[0]#assign the best more to avoid forefit
        best_score = float("-inf") # like min max, we start with a max node hence calling min value
        # which is the next node in an alternating min max
        for m in legal_moves:
            #get the best score
            v = self.min_value_alphaBeta(game.forecast_move(m),depth-1,alpha,beta)
            # v will always be more than best_score.
            if v > best_score:
                best_score = v
                best_move = m
            # keep updating alpha for all the legal moves
            alpha = max(alpha,best_score)
        # since this is the top most node return the best_move.
        return best_move




    def max_value_alphaBeta(self,game,depth,alpha,beta):
        """ Return the value for a win (+1) if the game is over,
        otherwise return the minimum value over all legal child
        nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves() #get legal moves
        if depth == 0 or not legal_moves: # if depth =0 or not legal moves, score and return
            return self.score(game, self)
        best_move=legal_moves[0] # assign the best move to avoid forefits
        best_score = float("-inf")
        for m in legal_moves:
            # calling min here and taking the max of it
             best_score =max(best_score, self.min_value_alphaBeta(game.forecast_move(m),depth-1,alpha,beta))
             #if score > best_score:
            #    best_score = score
             if best_score >= beta:
                return best_score
             # update alpha for all legal move
             alpha = max(alpha,best_score)
        #here return the best_score (propogate scores up till you return the best move)
        return best_score


    def min_value_alphaBeta(self,game,depth,alpha,beta):
        """ Return the value for a loss (-1) if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        legal_moves = game.get_legal_moves()#get legal moves
        if depth == 0 or not legal_moves:
            return self.score(game, self)

        best_move=legal_moves[0]# assign the best move to avoid forefits

        best_score = float("inf")
        for m in legal_moves:
            #here call max , so max cannot be > inf and hence the best score will always
            # be returned when you take a min of all the max values.
            best_score =min(best_score, self.max_value_alphaBeta(game.forecast_move(m),depth-1,alpha,beta))
            #if score < best_score:
            #   best_score = score

            if best_score <= alpha:
               return best_score
            beta = min(beta,best_score)
        #here return the best_score (propogate scores up till you return the best move)
        return best_score
