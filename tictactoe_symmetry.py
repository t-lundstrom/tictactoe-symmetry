import math
import time

# This is a simple tic-tac-toe game where the computer computes the entire game tree at the beginning of the game and then plays the game in an optimal way.
# Only small boards e.g. 3x3 and 4x4 are computable in reasonable time.
# The game tree is computed only up to symmetry.
# For example, the boards 
# X | X |             O |   | X
#   | O | X    and      | O | X 
# O |   |               | X |   
# are related by a 90 degree clockwise rotation, and hence are essentially the same.
# Therefore only one of them needs to be considered. 

# The game tree will be a dictionary whose keys are strings representing the board 
# and the values are either 'X', 'O', 'T' depending on who has a winning strategy from that point onward.
# Here 'T' is for 'tie', but more accurately it means that from that point onward neither has a winning strategy.
# Of course, if the player makes a silly move at a 'T' node, then the computer might then have a winning strategy.

# Boards are encoded as strings, reading the board row by row.
# We use 'e' to denote the empty square.
# For example, the 3x3 board
# X | X | 
#   | O | X
# O |   | 
# is encoded as the string 'XXeeOXOee'

def symmetries_of_square(n):
    # input: 'n' which is the side length of the square
    # output: all symmetries of the square, implemented as lists that record where each index goes
    # The indices of the square are written as, e.g. for n = 3,
    # 0 | 1 | 2 
    # 3 | 4 | 5
    # 6 | 7 | 8
    # The perumatations are then lists of these indices after the corresponding permutation.
    # For example, the rotation by 90 degrees clockwise gives
    # 6 | 3 | 0 
    # 7 | 4 | 1 
    # 8 | 5 | 2
    # This permutation is then recorded as the list [6,3,0,7,4,1,8,5,2].
    # The reflection along the vertical axis gives
    # 2 | 1 | 0
    # 5 | 4 | 3
    # 8 | 7 | 6
    # which is recorded as [2,1,0,5,4,3,8,7,6].
    # In fact, these two permutations generate the group of all symmetries of the square.

    identity = [i for i in range(n**2)]

    cw_rot_90 = [] # clockwise rotation by 90 degress
    p = n * (n-1) # the index of the bottom left corner
    for i in range(n):
        # On the i-th row of the rotated square we have the numbers [p + i - k * n for k in range(n)]
        cw_rot_90 += [p + i - k * n for k in range(n)] 

    # Clockwise rotation by 180 degress
    # Obtained by rotating 90 degrees twice
    cw_rot_180 = [cw_rot_90[i] for i in cw_rot_90] 

    # Clockwise rotation by 270 degress
    # Obtained by rotating first 180 degrees and then 90 degrees
    cw_rot_270 = [cw_rot_90[i] for i in cw_rot_180] 

    vert_refl = [] # Reflection along vertical axis
    for i in range(n**2):
        a = i - (i % n) # the smallest number of the row that i is on
        b = a + n - 1 # the largest number of the row that i is on. Note that there are n numbers on each row so b - a + 1 = n.
        vert_refl.append(a+b-i) # a+b-i is the symmetric counterpart of i on the same row

    # Reflection along horizontal axis
    # Obtained by first rotating 180 degress and then reflecting along the vertical axis
    hor_refl = [vert_refl[i] for i in cw_rot_180]

    # Reflection along the bottom-right top-left diagonal.
    # Obtained by first rotating 90 degrees clockwise and then reflecting along the horizontal axis
    diag1_refl = [hor_refl[i] for i in cw_rot_90]

    # Reflection along the bottom-left top-right diagonal.
    # Obtained by first rotating 90 degress clockwise and then reflecting along the vertical axis
    diag2_refl = [vert_refl[i] for i in cw_rot_90]

    return [identity,cw_rot_90,cw_rot_180,cw_rot_270,vert_refl,hor_refl,diag1_refl,diag2_refl]


def check_winner(board,needed_to_win):
    # checks if there are 'needed_to_win' many consecutive symbols on any row, column or diagonal.
    n = int(math.sqrt(len(board)))
    
    # rows
    for i in range(n):
        line = [i*n + j for j in range(n)]
        s = ''.join([board[i] for i in line])  # the string obtained by looking at symbols in positions indexed by 'line'
        if 'X'*needed_to_win in s:
            return 'X'
        elif 'O'*needed_to_win in s:
            return 'O'

    # columns
    for i in range(n):
        line = [j*n + i for j in range(n)]
        s = ''.join([board[i] for i in line])  # the string obtained by looking at symbols in positions indexed by 'line'
        if 'X'*needed_to_win in s:
            return 'X'
        elif 'O'*needed_to_win in s:
            return 'O'
    
    # Diagonals: from bottom right to top left.
    # The base of the diagonal 'p' moves downwards along the right-most column starting from top right box, which has index n-1.
    # We move downwards 2n-2 times.
    # Moving down corresponds to adding n.
    # The last position for p is therefore n-1 + n * (2n-2).
    # For each p we take n-1 steps from p towards up-left.
    # Moving up-left corresponds to subtracting n+1.
    # Some of the indices are outside of the bounds [0,n**2-1] but we simply take those that are inside this interval
    for p in range(n-1,n + n*(2*n-2),n):
        line = [p - j*(n+1) for j in range(n) if 0 <= p - j*(n+1) <= n**2 - 1]
        s = ''.join([board[i] for i in line])  # the string obtained by looking at symbols in positions indexed by line
        if 'X'*needed_to_win in s:
            return 'X'
        elif 'O'*needed_to_win in s:
            return 'O'
                   
    # Diagonals: from bottom left to top right.
    # The base of the diagonal 'p' moves downwards along the left-most column starting from top left box, which has index 0.
    # We move downwards 2n-2 times.
    # Moving down corresponds to adding n.
    # The last position for p is therefore n * (2n-2).
    # For each p we take n-1 steps from p towards up-right.
    # Moving up-right corresponds to subtracting n-1.
    # Some of the indices are outside of the bounds [0,n**2-1] but we simply take those that are inside this interval
    for p in range(0,n * (2*n - 2) + 1,n):
        line = [p - j*(n-1) for j in range(n) if 0 <= p - j*(n-1) <= n**2 - 1]
        s = ''.join([board[i] for i in line])  # the string obtained by looking at symbols in positions indexed by 'line'
        if 'X'*needed_to_win in s:
            return 'X'
        elif 'O'*needed_to_win in s:
            return 'O'

    # check for ties
    if board.count('e') == 0:
        return 'T'
    
    # nobody wins
    return None


def place_at(board,i,m):
    # Places symbol 'm' at position 'i'
    return board[:i] + m + board[i+1:]


def winner_of_node(board,player_of_this_node,game_tree,needed_to_win,symmetries_of_square):
    # We compute the winner of this node of the game tree, corresponding to 'board'.
    
    # Check if this board or any of its permutations has already been computed
    for s in symmetries_of_square:
        board_permuted_by_s = "".join([board[s[i]] for i in range(len(board))])
        if board_permuted_by_s in game_tree.keys():
            return game_tree[board_permuted_by_s]

    
    winner = check_winner(board,needed_to_win) # check if this node is a leaf, i.e. it has a winner
    if winner != None:
        game_tree[board] = winner
        return winner
    
    # Next, we will look at which of the empty square we need to consider.
    # For example, if the board is
    # X |   | O
    #   |   | 
    # O |   | X
    # then the empty squares are in positions 1,3,4,5,7 but we only need to consider positions 1,3,4.
    # This is because, for example, we don't need to consider placing anything in position 5 
    # since that is, up to symmetry, the same as placing something in position 1 as these two positions are related by a reflection 
    # along the down-left up-right diagonal which keeps to board fixed.
    # This reduces the number children of this node we need to consider.

    symmetries_of_board = [] # the set of symmetries of the square that keep the board fixed
    for s in symmetries_of_square:
        for i in range(len(board)):
            if board[i] != board[s[i]]:
                break
        else:
            symmetries_of_board.append(s)

    empty_squares = [i for i in range(len(board)) if board[i] == 'e']
    empty_squares_uts = [] # empty squares up to symmetry
    
    # We compute the list empty_squares_uts
    for i in empty_squares:
        symmetrically_unique = True
        for j in empty_squares_uts:
            for s in symmetries_of_board:
                if i == s[j]:
                    symmetrically_unique = False
                    break
            if not symmetrically_unique:
                break
        else:
            empty_squares_uts.append(i)    

    next_boards_uts = [place_at(board,i,player_of_this_node) for i in empty_squares_uts] # all possible moves current player can make here, up to symmetry
  
    other_player = 'X' if player_of_this_node == 'O' else 'O'
  
    outcomes = [winner_of_node(b,other_player,game_tree,needed_to_win,symmetries_of_square) for b in next_boards_uts] # compute the outcomes of the relevant children of this node

    if outcomes.count(player_of_this_node) >= 1: 
        # if current player wins at least one of the next nodes it wins this node
        game_tree[board] = player_of_this_node
        return player_of_this_node
    elif outcomes.count('T') >= 1:  
        # current player doesn't win any of the next nodes but at least one is tie: this board is (at least) a tie
        game_tree[board] = 'T'
        return 'T'
    else:                           
        # no wins or ties for current player at this node: other player wins this node
        game_tree[board] = other_player
        return other_player


def next_move_for_computer(current_board,game_tree,permutations,computer_symbol):
    # Compute the next optimal move for the computer.
    # This function returns the next board, instead of just the position of the symbol.

    # We look at all empty squares which gives us the possible next moves.
    # For each board b that is obtained by placing a symbol in an empty square, 
    # we compute all possible permutations of b and see which one of them is in the computed game tree.
    # In this way we form pairs (b,b_perm) where b is one of the next boards and b_perm is one of its permutations that is in the computed game tree.
    # A lemma that needs to be proven here is that for any b there is at least one symmetric counterpart b_perm in the computed game tree,
    # i.e. in game_tree.keys() 
    # If for some pair (b,b_perm) we find that b_perm gives a winning path for the computer, we know that so does b and hence we can play that one.

    empty_squares = [i for i in range(len(current_board)) if current_board[i] == 'e']
    next_boards = [place_at(current_board,i,computer_symbol) for i in empty_squares]
    next_boards_and_their_permutations = [] # the pairs (b,b_perm) 

    for b in next_boards:
        for s in permutations:
            b_permuted_by_s = ''.join([b[s[i]] for i in range(len(b))])
            if b_permuted_by_s in game_tree.keys():
                next_boards_and_their_permutations.append((b,b_permuted_by_s))
    
    # Check if there are winning moves
    for b,b_perm in next_boards_and_their_permutations:
        if game_tree[b_perm] == computer_symbol:
            print("Computer is on a winning path")
            return b
    
    # No winning moves: check if any of them gives a tie
    for b,b_perm in next_boards_and_their_permutations:
        if game_tree[b_perm] == 'T':
            print("Computer will get at least a tie")
            return b    
        
    # No ties either: computer chooses the first possible move
    # Note: the computer could try to do some heuristic decision here instead
    print("Player has a way to win for sure")
    return next_boards[0]


def print_board(board):
    n = int(math.sqrt(len(board)))

    # column numbers
    print('  ',end='')
    for i in range(n):
        print(i,end=' ')
    print("\n0",end=' ') # first row number

    for i in range(len(board)):
        if i > 0 and i % n == 0:
            print(f"\n{i // n}",end=' ') # row numbers 
        if board[i] == 'e':
            print('_',end= ' ')
        else:
            print(board[i],end= ' ')
        
    print('\n')    


def ask_player_move(board):
    board_side_length = int(math.sqrt(len(board)))

    while True:
        move = input("Player move: ")
        if not (move.isdigit() and len(move) == 2): # does the string 'move' consist of just two digits?
            print("Try again")
        else:
            row = int(move[0])
            col = int(move[1])
            if not( 0 <= row <= board_side_length-1 and 0 <= col <= board_side_length-1):
                print("Try again")
                continue
            
            # input is of then correct form, we check if the there is an empty square
            index = board_side_length * row + col
            if board[index] != 'e':
                print("Not empty, try again")
                continue
            else:
                return index


def play_game(board,game_tree,all_symmetries,needed_to_win,player_symbol):
    computer_symbol = 'O' if player_symbol == 'X' else 'X'
    next_turn = 'player' if player_symbol == 'X' else 'computer'
    
    print_board(board)

    while True:
        if next_turn == 'player':
            player_move = ask_player_move(board)
            board = place_at(board,player_move,player_symbol)
        else:
            board = next_move_for_computer(board,game_tree,all_symmetries,computer_symbol)

        print_board(board)

        winner = check_winner(board,needed_to_win)
        if winner == player_symbol:
            print("You Win!")
            break
        elif winner == computer_symbol:
            print("Computer Wins!")
            break
        elif winner == 'T':
            print("It's a tie")
            break
            
        next_turn = 'player' if next_turn == 'computer' else 'computer'


def ask_board_settings():
    while True:
        s = input("Board side length: ")
        if not (s.isdigit() and len(s) > 0 and s[0] != '0'):
            print("Please give the side lenght as a positive integer")
            continue

        board_side_length = int(s)
        break

    while True:
        s = input("How many to win: ")
        if not (s.isdigit() and len(s) > 0 and s[0] != '0' and 1 <= int(s) <= board_side_length):
            print(f"Please give an integer between 1 and {board_side_length}")
            continue

        needed_to_win = int(s)
        break

    return board_side_length,needed_to_win


def ask_player_symbol():
    while True:
        s = input("Play as X/O (X goes first): ")
        if s.upper() not in ['X','O']:
            print("Type either 'X' or 'O'")
            continue
        
        return s.upper()


if __name__ == '__main__':
    change_settings = True
    while True:
        if change_settings:
            board_side_length, needed_to_win = ask_board_settings()

            print("Computing game tree...")
            board = 'e'*board_side_length**2
            game_tree = {}
            start = time.time()
            all_symmetries = symmetries_of_square(board_side_length)
            winner_of_node(board,'X',game_tree,needed_to_win,all_symmetries) # Compute the entire game tree, up to symmetry. First move is played by 'X'
            end = time.time()
            print(f"Time: {end-start:.3f}s\nNodes in game tree: {len(game_tree.keys())}\n")

        player_symbol = ask_player_symbol()
        play_game(board,game_tree,all_symmetries,needed_to_win,player_symbol)
        
        while True:
            answer = input("1: New game (same board)\n2: New game (change board)\n3: Quit\n? ")
            if answer not in ['1','2','3']:
                print("Try again")
                continue
            else:
                break
        
        answer = int(answer)
        
        match answer:
            case 1:
                board = 'e'*board_side_length**2
                change_settings = False
            case 2:
                change_settings = True
            case 3:
                break

     