from input_dialog import InputDialog
from setup_game import *
from time import perf_counter as pc
from time import sleep


def get_start_values():  # set this input parameters
    global white_name, game_running, tot_elapsed_time, current_player
    global dark_col, light_col, board_size, suggested_start_time
    game_running = True
    tot_elapsed_time = [0, 0]
    board_size = 650
    suggested_start_time = 30
    dark_col = "darkgreen"
    light_col = "lightgreen"


def set_up_game():
    global white_name, black_name, chessboard, dark_col, light_col
    global board_size, suggested_start_time, input_dialog

    white_start_time, black_start_time = input_dialog.get_times()
    white_name, black_name = input_dialog.get_names()

    chessboard = Setup_game(
        dark_col,
        light_col,
        board_size / 8,
        white_name,
        black_name,
    )
    chessboard.draw_board()
    chessboard.draw_pieces()
    chessboard.setup_buttons()
    chessboard.turn_off_buttons()
    chessboard.set_start_time(white_start_time, black_start_time)
    chessboard.setup_text(white_name, black_name)


def one_round():
    global chessboard, piece, piece_index, i, j, current_player, tot_elapsed_time
    move_spot = False
    list_circles = []
    piece_selected = False
    rochade = False
    while move_spot == False:
        x, y = chessboard.get_mouse_position(pc, tot_elapsed_time, current_player)
        i, j = convert_to_i_j(chessboard, x, y)  # converts to 8x8 grid (i,j)
        temp_piece, temp_piece_index = chessboard.exist_piece_here(
            current_player, i, j
        )  # checks if piece has been selected
        chessboard.undraw_circles(list_circles)  # undraws circles if they exists
        if temp_piece != None:
            piece_selected = True
            possible_moves = chessboard.get_possible_moves(
                temp_piece, temp_piece_index, current_player, False
            )
            list_circles = chessboard.draw_possible_moves(possible_moves)
            piece, piece_index = temp_piece, temp_piece_index

        if piece_selected:
            if chessboard.check_spot(
                i, j, possible_moves
            ):  # True if player can move to spot
                move_spot = True

        if chessboard.check_which_button_clicked(x, y, current_player)[
            0
        ]:  # return True if any button is clicked
            move_spot = True
            rochade = True
            if chessboard.settings_button_clicked:
                move_spot = False
                rochade = False

    if rochade == False:
        chessboard.move_piece(piece, current_player, piece_index, i, j)
    else:
        piece = rochade  # piece = True, moves piece in check_which_button_clicked


def end_of_round():
    global chessboard, piece, piece_index, i, j, current_player
    global tot_elapsed_time, output_message, game_running
    other_player = chessboard.get_other_player(current_player)
    chessboard.turn_off_buttons()  # turn off buttons if they should be turned off
    chessboard.turn_on_buttons()
    chessboard.undraw_check_text()  # undraw check text if check text was displayed before

    if piece != True:
        chessboard.remove_piece(other_player, i, j, True)
        if piece == "bonde":
            chessboard.queening_the_pawn(
                current_player, piece_index, i, j
            )  # checks if pawn is on other side of board

    game_running, output_message = chessboard.check_if_game_over(
        current_player, other_player
    )
    if chessboard.check(other_player):
        chessboard.set_check_text(other_player)
    current_player = other_player


def main():
    global white_name, black_name, game_running, tot_elapsed_time
    global current_player, output_message, input_dialog
    get_start_values()
    input_dialog = InputDialog(suggested_start_time)
    if input_dialog.interact() == "Start":
        print("setting up game")
        set_up_game()
        current_player = white_name
        try:
            while game_running:
                one_round()
                end_of_round()

            chessboard.set_winners_text(output_message)
            sleep(1000)
        except GraphicsError:
            print("hejdå")


if __name__ == "__main__":
    main()
