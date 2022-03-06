import random

starting_board = """
     1 | 2 | 3
     ---------
     4 | 5 | 6
     ---------
     7 | 8 | 9
"""

valid_input = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
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

empty = "   "
player_x = " X "
player_o = " O "
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
taken_spaces = []
player_spaces = []
comp_spaces = []


def print_board():
    print(f"""
    {game_positions['pos_1']}|{game_positions['pos_2']}|{game_positions['pos_3']}
     ---------
    {game_positions['pos_4']}|{game_positions['pos_5']}|{game_positions['pos_6']}
     ---------
    {game_positions['pos_7']}|{game_positions['pos_8']}|{game_positions['pos_9']}
    """)


def place_move(move, player_side):
    game_positions[f'pos_{move}'] = player_side
    taken_spaces.append(move)
    player_spaces.append(move)


def player_about_to_win():
    for number_set in winning_numbers:
        player_taken = 0
        comp_taken = 0
        for number in number_set:
            if number in player_spaces:
                player_taken += 1
            elif number in comp_spaces:
                comp_taken += 1
        if player_taken == 2 and comp_taken == 0:
            return True
    return False


def block_player_win():
    player_could_win = []
    for number_set in winning_numbers:
        player_taken = 0
        for number in number_set:
            if number in player_spaces:
                player_taken += 1
            if player_taken == 2:
                player_could_win.append(number_set)
    set_to_play = random.choice(player_could_win)
    for number in set_to_play:
        if number not in player_spaces:
            return number


def choose_best_move():
    if player_about_to_win():
        best_move = block_player_win()
        return best_move
    one_more_move = []
    two_more_moves = []
    for number_set in winning_numbers:
        open_spaces = 0
        taken = 0
        for number in number_set:
            if number in comp_spaces:
                open_spaces += 1
            elif number in player_spaces:
                taken += 1
        if open_spaces == 2 and taken == 0:
            one_more_move.append(number_set)
        elif open_spaces == 1 and taken == 0:
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
        comp_move = str(random.randint(1, 9))
        if comp_move not in taken_spaces:
            return comp_move


def computer_move(computer_side):
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
    for number_set in winning_numbers:
        for number in range(len(number_set)):
            if number_set[number] not in side_moves:
                break
            elif number == 2 and number_set[number] in side_moves:
                return True
    return False


def player_move(player):
    move_valid = False
    while not move_valid:
        next_move = input("Enter the number of the space you'd like to go in: ")
        if next_move not in taken_spaces and next_move in valid_input:
            move_valid = True
            place_move(next_move, player)
        else:
            print("That input is either invalid, or that space is already taken.")


def board_full():
    if len(taken_spaces) == 9:
        print("It's a tie! No one won. Restart the game to try again.")
        return True


def play_game(player, computer):
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


def choose_side():
    side_chosen = False
    player_side = input("Type 'x' or 'o' to choose a side - Player X always goes first: ")
    while not side_chosen:
        if player_side.strip().lower() == "x" or player_side.strip().lower() == "o":
            return player_side
        else:
            player_side = input("That's not a valid input. Please type the letter 'x' or the letter 'o' to begin: ")


def begin_game():
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


begin_game()
