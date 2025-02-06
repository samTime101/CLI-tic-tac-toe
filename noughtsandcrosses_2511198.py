"""
MODULE DOCSTRING: PYLINT CONVENTION
imports: random , os , json
"""

import random
import os.path
import json
random.seed()


def draw_board(board):

    '''
    function:draw_board
    parameter:board
    prints board
    return:None
    '''

    for i in board:
        print(f"{'-'*11}".center(50))
        print(f"| {' | '.join(i)} |".center(50))
    print(f"{'-'*11}".center(50))

def welcome(board):

    '''
    function:welcome
    parameter:board
    prints welcome message
    return:None
    '''

    print('Welcome to the "Unbeatable Noughts and Crosses" game.')
    print("The board layout is show below:")
    draw_board(board)
    print("When prompted, enter the number corresponding to the square you want.")


def initialise_board(board):

    '''
    function:initialise_board
    parameter:board
    sets board to empty
    returns board
    PYLINT CONVENTION : using enumerate
    '''


    for i, row in enumerate(board):
        for j, _ in enumerate(row):
            board[i][j] = " "
    return board


def get_player_move(board):

    '''
    function:get_player_move
    parameters:board
    gets player move
    returns:row and col
    PYLINT CONVENTION: EXPLICIT ERROR HANDLING
    '''

    while True:
        try:
            print("                    1 2 3")
            print("                    4 5 6")
            print("Choose your square: 7 8 9 :", end="")
            user_input = int(input())
            if user_input < 1 or user_input > 9:
                raise ValueError("enter between 1 to 9")
            row  = (user_input -1 )//3
            col = (user_input-1)%3
            if board[row][col] == ' ':
                return row,col
            print("Cell already occupied")
        except ValueError as error :
            print(error)
            continue

# Feb 6 , Added Min Max algo

def minimax(board, depth, is_maximizing):
    """
    min max : ALGORITHM REFERENCE :
    https://www.datacamp.com/tutorial/minimax-algorithm-for-ai-in-python  PSEUDOCODE
    RECURSIVE ALGORITHM ,
    RETURNS BEST SCORE AFTER TRYING WINNING MOVE
    """
    # COMPUTER WON
    if check_for_win(board, 'O'):
        return 10
    if check_for_win(board, 'X'):
        return -10
    if check_for_draw(board):
        return 0
    if is_maximizing:
        best_score = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    # for first 0 and greater than 0
                    best_score = max(score, best_score)
        return best_score
    best_score = float('inf')
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                score = minimax(board, depth + 1, True)
                board[i][j] = ' '
                # just less than inf
                best_score = min(score, best_score)
    return best_score

def choose_computer_move(board):
    """
    Algorithm : best score is set to lowest value
    Calls minmax function and receives score
    if score from func is greater than the lowest value ,
    then it points to i, j and makes that move
    """
    best_score = float('-inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                score = minimax(board, 0, False)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    if best_move is None:
        raise ValueError("No valid moves available")
    return best_move



def check_for_win(board, mark):

    '''
    function:check_for_win
    parameters:board,mark
        if all the three consecutive cells are filled it returns True
        else False
    returns:True or False
    '''
    winning_conditions = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]

    for condition in winning_conditions:
        condition_met = True
        for (row, col) in condition:
            if board[row][col] != mark:
                condition_met = False
                break
        if condition_met:
            return True

    return False

def check_for_draw(board):

    '''
    function:check_for_draw
    parameter:board
    returns:True if all cells are filled otherwise False
    '''
    for row in board:
        if ' ' in row:
            return False
    return True



def play_game(board):
    '''
    function:play_game
    parameter:board
    play_game function
    '''
    initialise_board(board)
    draw_board(board)
    cur_player='X'
    while True:
        if cur_player == "X":
            row,col = get_player_move(board)
            board[row][col] = "X"
        else:
            try:
                row,col = choose_computer_move(board)
                board[row][col] = "O"
            except ValueError as error:
                print(error)
                return -100
        draw_board(board)

        if check_for_win(board,cur_player):
            if cur_player == "X":
                print("Player X Won")
                return 1
            print("Computer Won")
            return -1
        if check_for_draw(board):
            print("Draw No one Won ")
            return 0
        if cur_player == "X":
            cur_player = "O"
        else:
            cur_player = "X"

def menu():

    '''
    function:menu
    paramenter:None
    returns choice
    '''
    print("Enter one of the following options:\n"
    "\t1 - play game\n"
    "\t2 - save your score in the leaderboard\n"
    "\t3 - Load and display the loaderboard\n"
    "\tq - End program")
    choice = input("\n1,2,3 or q? ")
    return choice

def load_scores():
    '''
    function:load_scores
    parameter:none
    reuturns json data from leaderboar.txt file
    '''
    if os.path.exists('leaderboard.txt'):
        with open('leaderboard.txt', 'r' , encoding='utf-8') as file:
            leaders = json.load(file)
    else:
        leaders = {}
    return leaders

def save_score(score):

    '''
    function:save_score
    parameter:score
    takes in user name and saves it in leaderboar.txt file
    returns:None
    '''
    name = input("Enter your name: ")
    leaders = load_scores()
    leaders[name] = score
    with open('leaderboard.txt', 'w',encoding='utf-8') as file:
        json.dump(leaders, file)
    # return


def display_leaderboard(leaders):

    '''
    function:display_leaderboard
    parameter:leaders
    prints the leaderboard
    '''
    sorted_leaders = sorted(leaders.values(),reverse=True)
    printed_names = []
    print("\nNAME: SCORE")
    for score in sorted_leaders:
        for name  in leaders.keys():
            if leaders[name] == score and name not in printed_names:
                print(f"{name}: {score}")
                printed_names.append(name)
                break
