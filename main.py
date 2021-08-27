from tkinter import Checkbutton
from setup_game import *

boardSize = 800
chessboard = Setup_game("green", "yellow", boardSize / 8)
global game_running
game_running = True


def _setup_game():
    chessboard.draw_board()
    chessboard.draw_pieces()
    chessboard.setup_buttons()
    chessboard.turn_off_buttons()


def round(current_player):
    print("choose a piece to move")
    move_spot = False
    list_circles = []
    piece_selected = False
    rochade = False
    while move_spot == False:
        x, y = chessboard.get_mouse_position()
        i, j = convert_to_i_j(chessboard, x, y)
        temp_piece, temp_piece_index = chessboard.exist_piece_here(current_player, i, j)
        if temp_piece != None:
            piece_selected = True
            piece, piece_index = temp_piece, temp_piece_index
            if list_circles != []:
                chessboard.undraw_possible_moves(list_circles)
            possible_moves = chessboard.check_possibilities(
                piece, piece_index, current_player, False
            )
            possible_moves = chessboard.potential_movement_check(
                piece, piece_index, current_player, possible_moves
            )

            list_circles = chessboard.draw_possible_moves(possible_moves)

        if piece_selected:
            if chessboard.check_spot(i, j, possible_moves):
                move_spot = True
        if chessboard.check_which_button_clicked(
            x, y, current_player
        ):  # can only do rochade on the others turn, change the other her to current and fix bug
            move_spot = True
            rochade = True
    if list_circles != []:
        chessboard.undraw_possible_moves(list_circles)
    if rochade == False:
        chessboard.move_piece(piece, current_player, piece_index, i, j)
        return [piece, piece_index, i, j]
    else:
        return [rochade, None, None, None]  # rochade == True


def end_of_round(piece, current_player, piece_index, i, j):
    other_player = chessboard.get_other_player(current_player)
    chessboard.turn_off_buttons()
    chessboard.turn_on_buttons()
    if piece != True:
        _ = chessboard.remove_piece(other_player, i, j, True)
    if chessboard.check(other_player):
        print("schack")

    global game_running
    if chessboard.check_mate(other_player):
        print(current_player, "wins!!")
        game_running = False
    elif chessboard.equal(other_player):
        print("lika!")
        game_running = False
    else:
        print("game is still running")
        print(game_running, "game_running")

    return other_player


def main():
    current_player = "white"
    print("setting up game")
    _setup_game()
    while game_running:
        [piece, piece_index, i, j] = round(current_player)
        current_player = end_of_round(piece, current_player, piece_index, i, j)
    print("game is not running", game_running)


if __name__ == "__main__":
    main()
