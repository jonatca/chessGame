from input_dialog import InputDialog
from tkinter import Checkbutton
from setup_game import *
from time import perf_counter as pc
from time import sleep

# set this input parameters
boardSize = 650

input_dialog = InputDialog()


def setup_the_game():
    global white_name, black_name, chessboard
    white_start_time, black_start_time = input_dialog.get_times()
    white_name, black_name = input_dialog.get_names()

    chessboard = Setup_game(
        "darkgreen",
        "lightgreen",
        boardSize / 8,
        white_name,
        black_name,
    )
    chessboard.draw_board()
    chessboard.draw_pieces()
    chessboard.setup_buttons()
    chessboard.turn_off_buttons()
    chessboard.set_start_time(white_start_time, black_start_time)
    chessboard.setup_text(white_name, black_name)


def one_round(current_player, pc, tot_elapsed_time):
    global chessboard
    print("choose a piece to move")
    move_spot = False
    list_circles = []
    piece_selected = False
    rochade = False
    piece = 0
    while move_spot == False:
        x, y = chessboard.get_mouse_position(pc, tot_elapsed_time, current_player)
        i, j = convert_to_i_j(chessboard, x, y)
        print(i, j)
        temp_piece, temp_piece_index = chessboard.exist_piece_here(current_player, i, j)
        if temp_piece != None:
            if list_circles != []:
                chessboard.undraw_possible_moves(list_circles)
            piece_selected = True
            possible_moves = chessboard.check_possibilities(
                temp_piece, temp_piece_index, current_player, False
            )

            possible_moves = chessboard.potential_movement_check(
                temp_piece, temp_piece_index, current_player, possible_moves
            )

            list_circles = chessboard.draw_possible_moves(possible_moves)
            piece, piece_index = temp_piece, temp_piece_index
        else:
            if list_circles != []:
                chessboard.undraw_possible_moves(list_circles)

        if piece_selected:
            if chessboard.check_spot(i, j, possible_moves):
                move_spot = True
        if chessboard.check_which_button_clicked(x, y, current_player)[0]:
            move_spot = True
            rochade = True
            if chessboard.settings_button_clicked:
                move_spot = False
                rochade = False

    if rochade == False:
        chessboard.move_piece(piece, current_player, piece_index, i, j)
        return [piece, piece_index, i, j]
    else:
        return [rochade, None, None, None]  # rochade == True


def end_of_round(piece, current_player, piece_index, i, j):
    global chessboard, output_message
    other_player = chessboard.get_other_player(current_player)
    chessboard.turn_off_buttons()
    chessboard.turn_on_buttons()
    chessboard.undraw_check_text()

    if piece != True:
        _ = chessboard.remove_piece(other_player, i, j, True)
        if piece == "bonde":
            chessboard.queening_the_pawn(current_player, piece_index, i, j)

    game_running = True
    if chessboard.get_time_is_up():
        output_message = {
            other_player: f"Time is up\nGood job {other_player}\nYou win!",
            current_player: f"Time is up\nNice try {current_player}\nYou lost",
        }
        game_running = False
    if chessboard.check_mate(other_player):
        output_message = {
            current_player: f"Check mate,\nGood job {current_player}\nYou win!",
            other_player: f"Check mate\nNice try {other_player}\nYou lost",
        }
        game_running = False
    elif chessboard.equal(other_player):
        print("equal!")
        output_message = {
            current_player: "Equal,\nGood job {current_player}",
            other_player: "Equal\nGood job {other_player}",
        }
        game_running = False
    elif chessboard.check(other_player):
        print("schack")
        chessboard.set_check_text(other_player)

    return other_player, game_running


def get_start_values():
    global white_name, game_running, tot_elapsed_time
    game_running = True
    tot_elapsed_time = [0, 0]
    current_player = white_name
    return current_player


def main():
    global white_name, black_name, game_running, tot_elapsed_time

    if input_dialog.interact() == "Start":
        print("setting up game")
        setup_the_game()
        current_player = get_start_values()
        while game_running:
            [piece, piece_index, i, j] = one_round(current_player, pc, tot_elapsed_time)
            current_player, game_running = end_of_round(
                piece, current_player, piece_index, i, j
            )
            print("tot_elapsed_time", tot_elapsed_time)
        chessboard.set_winners_text(output_message, white_name, black_name)
        sleep(1000)


if __name__ == "__main__":
    main()
