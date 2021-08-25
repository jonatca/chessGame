from tkinter import Checkbutton
from setup_game import *

boardSize = 800
chessboard = Setup_game("green", "yellow", boardSize / 8)


def _setup_game():
    chessboard.draw_board()
    chessboard.draw_pieces()


def round(current_player):
    print("choose a piece to move")
    move_spot = False
    list_circles = []
    piece_selected = False
    while move_spot == False:
        i, j = chessboard.get_mouse_position()
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
            )  # returns True if movement leads to check on my self

            list_circles = chessboard.draw_possible_moves(possible_moves)

        if piece_selected:
            if chessboard.check_spot(i, j, possible_moves):
                move_spot = True

    chessboard.undraw_possible_moves(list_circles)

    chessboard.move_piece(piece, current_player, piece_index, i, j)
    return [piece, piece_index, i, j]


def end_of_round(piece, current_player, piece_index, i, j):
    other_player = chessboard.get_other_player(current_player)

    _ = chessboard.remove_piece(other_player, i, j, True)
    if chessboard.check(other_player):
        print("schack")
    else:
        print("inte schack")
    #    if chessboard.check_mate(other_player):
    #     print("game over ", current_player, "wins")
    # else:
    #       print("check")


def main():
    current_player = "white"
    print("setting up game")
    _setup_game()
    while True:
        [piece, piece_index, i, j] = round(current_player)
        end_of_round(piece, current_player, piece_index, i, j)
        current_player = chessboard.get_other_player(current_player)


main()
