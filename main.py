import random

# We start the game showing the user the board with numbers 1-9 in each of the spaces.
# When the user wants to place a move, the user must type one of the numbers for the space where they'd like to move.
starting_board = """
     1 | 2 | 3
     ---------
     4 | 5 | 6
     ---------
     7 | 8 | 9
"""

# A list of valid move inputs to check against in case the user inputs a non-valid input.
valid_input = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

# This is a list of every combination of winning tic-tac-toe numbers on a 3x3 board. This list will be checked against
# when deciding if the user/computer won. This will also be checked against for the computer to decide which move is
# best for them to take next.
winning_numbers = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
    ["1", "4", "7"],
    ["2", "5", "8"],
    ["3", "6", "9"],
    ["1", "5", "9"],
    ["3", "5", "7"],
]

# The following are the string inputs which are used to display the board. The board starts with all empty spaces.
# As a move is placed, it is replaced by either player x or player o.
empty = "   "
player_x = " X "
player_o = " O "

# A dictionary of all nine board positions, and they're accompanying values. They start as empty, and will be replaced
# as the game progresses.
game_positions = {
    "pos_1": empty,
    "pos_2": empty,
    "pos_3": empty,
    "pos_4": empty,
    "pos_5": empty,
    "pos_6": empty,
    "pos_7": empty,
    "pos_8": empty,
    "pos_9": empty,
}

# These lists are used to keep track of spaces taken so far by both the user and the computer.
taken_spaces = []
player_spaces = []
comp_spaces = []


def choose_side():
    """Asks the player to choose if they'd like to be x or o. If the player's input is invalid, it continues to prompt
    the player for a valid choice."""
    side_chosen = False
    player_side = input("Type 'x' or 'o' to choose a side - Player X always goes first: ")
    while not side_chosen:
        if player_side.strip().lower() == "x" or player_side.strip().lower() == "o":
            return player_side
        else:
            player_side = input("That's not a valid input. Please type the letter 'x' or the letter 'o' to begin: ")


def begin_game():
    """This starts the game. It asks for the player to press 'y' to begin, and then asks the player to choose a side.
    Once the player chooses x or o, the starting reference board with numbers 1-9 is shown, and the
    main game loop begins. Note that if the player chooses to be x, the player will place a move before the main game
    loop begins."""
    player_start = input("Press 'y' to begin: ")
    if player_start.strip().lower() == 'y':
        player_side = choose_side().strip().lower()
        if player_side == "x":
            player = " X "
            computer = " O "
            print(starting_board)
            user_move = input("You play the first move. Enter the number of the space you'd like to go in: ")
            place_move(user_move, player)
            play_game(player, computer)
        elif player_side == "o":
            player = " O "
            computer = " X "
            print(starting_board)
            play_game(player, computer)
    else:
        print("That's not the letter 'y'! Be sure to press the letter 'y' to begin.")
        begin_game()


def play_game(player, computer):
    """This is the main game loop. It starts with the computer's move, then prints the board following the computer's
    move. It then checks if the computer won with that move, and if not, it checks if the board is full.

    If both of those are untrue, it proceeds to the player's turn, then prints the board following the player's move.
    It then checks if the player is the winner following the player's move, and if not, it checks if the board is full.

    If any of the game-ending conditions are satisfied, the loop is broken and the appropriate game-ending message is
    displayed."""
    game_over = False
    while not game_over:
        computer_move(computer)
        print_board()
        if check_winner(comp_spaces):
            print("The computer is the winner, better luck next time!")
            break
        elif board_full():
            break
        else:
            player_move(player)
            print_board()
            if check_winner(player_spaces):
                print("You won! Thanks for playing.")
                break
            elif board_full():
                game_over = True


def print_board():
    """Prints the board as it currently stands. This is printed after every move to show the current state of the
    game."""
    print(f"""
    {game_positions['pos_1']}|{game_positions['pos_2']}|{game_positions['pos_3']}
     ---------
    {game_positions['pos_4']}|{game_positions['pos_5']}|{game_positions['pos_6']}
     ---------
    {game_positions['pos_7']}|{game_positions['pos_8']}|{game_positions['pos_9']}
    """)


def place_move(move, player_side):
    """Takes the player's chosen move, and their chosen side (ie: x or o), and then replaces the empty position on the
    board with their marker."""
    game_positions[f'pos_{move}'] = player_side
    taken_spaces.append(move)
    player_spaces.append(move)


def comp_about_to_win():
    """Checks if the computer is one move away from winning. If so, the function returns True."""
    for number_set in winning_numbers:
        player_taken = 0
        comp_taken = 0
        for number in range(len(number_set)):
            if number_set[number] in player_spaces:
                player_taken += 1
            elif number_set[number] in comp_spaces:
                comp_taken += 1
            if number == 2:
                if player_taken == 0 and comp_taken == 2:
                    return True
    return False


def player_about_to_win():
    """Checks if the player is one move away from winning. If so, the function returns True."""
    for number_set in winning_numbers:
        player_taken = 0
        comp_taken = 0
        for number in range(len(number_set)):
            if number_set[number] in player_spaces:
                player_taken += 1
            elif number_set[number] in comp_spaces:
                comp_taken += 1
            if number == 2:
                if player_taken == 2 and comp_taken == 0:
                    return True
    return False


def block_player_win():
    """If the player is one move away from winning, this function will return the number of the
    space on the board where the winning move would be."""
    player_could_win = []
    for number_set in winning_numbers:
        player_taken = 0
        comp_taken = 0
        for number in range(len(number_set)):
            if number_set[number] in player_spaces:
                player_taken += 1
            elif number_set[number] in comp_spaces:
                comp_taken += 1
            if number == 2:
                if player_taken == 2 and comp_taken == 0:
                    player_could_win.append(number_set)
    set_to_play = random.choice(player_could_win)
    for number in set_to_play:
        if number not in player_spaces:
            return number


def choose_best_move():
    """First checks if computer is one move away from winning. If so, the function will pass so that the computer can
    determine the best move to take. If not, it checks if the player is one move away from winning, and if they
    are, the player's winning move will be returned as the best move for the computer to take.

    If both of those are untrue, it then makes a list of all moves that are best for the computer to take, starting
    with those where there is one move left to take. If there are any such moves, it'll take the winning move.
    Otherwise, it proceeds to find move sets where the computer would win in two more moves, and then would take a
    move from the remaining moves in that move set.

    If none of those are true, the computer simply chooses a random unchosen space on the board to move as the best
    move."""
    if comp_about_to_win():
        pass
    elif player_about_to_win():
        best_move = block_player_win()
        return best_move
    one_more_move = []
    two_more_moves = []
    for number_set in winning_numbers:
        comp_taken = 0
        player_taken = 0
        for number in number_set:
            if number in comp_spaces:
                comp_taken += 1
            elif number in player_spaces:
                player_taken += 1
        if comp_taken == 2 and player_taken == 0:
            one_more_move.append(number_set)
        elif comp_taken == 1 and player_taken == 0:
            two_more_moves.append(number_set)
    if len(one_more_move) >= 1:
        best_move_set = random.choice(one_more_move)
        for number in best_move_set:
            if number not in comp_spaces:
                return number
    elif len(two_more_moves) >= 1:
        best_move_set = random.choice(two_more_moves)
        potential_moves = []
        for number in best_move_set:
            if number not in comp_spaces:
                potential_moves.append(number)
        best_move = random.choice(potential_moves)
        return best_move
    else:
        move_found = False
        while not move_found:
            comp_move = str(random.randint(1, 9))
            if comp_move not in taken_spaces:
                return comp_move


def computer_move(computer_side):
    """The computer chooses the best move, and then places the move on the board. This also appends the lists of spaces
    taken with the move that was decided upon. This function also checks that if this is the computer's first move, it
    simply chooses a random unchosen space on the board, and places its move there."""
    move_found = False
    while not move_found:
        if len(comp_spaces) == 0:
            comp_move = str(random.randint(1, 9))
            if comp_move not in taken_spaces:
                move_found = True
                game_positions[f'pos_{comp_move}'] = computer_side
                taken_spaces.append(comp_move)
                comp_spaces.append(comp_move)
        else:
            comp_move = choose_best_move()
            move_found = True
            game_positions[f'pos_{comp_move}'] = computer_side
            taken_spaces.append(comp_move)
            comp_spaces.append(comp_move)


def check_winner(side_moves):
    """Takes the list of either player x or player o's moves, and checks it against the list of winning combinations.
    If all numbers of a particular winning move set are found to be in the list of the inputted side's moves, the
    function returns True."""
    for number_set in winning_numbers:
        for number in range(len(number_set)):
            if number_set[number] not in side_moves:
                break
            elif number == 2 and number_set[number] in side_moves:
                return True
    return False


def player_move(player):
    """Asks for a space where the player would like to go, and then calls the place_move function. If the player's input
    is invalid, the player will be asked again to place a valid move."""
    move_valid = False
    while not move_valid:
        next_move = input("Enter the number of the space you'd like to go in: ")
        if next_move not in taken_spaces and next_move in valid_input:
            move_valid = True
            place_move(next_move, player)
        else:
            print("That input is either invalid, or that space is already taken.")


def board_full():
    """Checks if all spaces on the board have been taken. If so, the function returns True."""
    if len(taken_spaces) == 9:
        print("It's a tie! No one won. Restart the game to try again.")
        return True


# This calls the function to start the game.
begin_game()
