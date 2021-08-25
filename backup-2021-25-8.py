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
    while move_spot == False:
        i, j = chessboard.get_mouse_position()
        temp_piece, temp_piece_index = chessboard.exist_piece_here(current_player, i, j)
        if temp_piece != None:
            piece, piece_index = temp_piece, temp_piece_index
            if list_circles != []:
                chessboard.undraw_possible_moves(list_circles)
            possible_moves = chessboard.check_possibilities(
                piece, piece_index, current_player, i, j
            )
            list_circles = chessboard.draw_possible_moves(possible_moves)

        if piece != None:
            if chessboard.check_spot(i, j, possible_moves):
                print("move_spot == True")
                move_spot = True

    print(move_spot, "move_spot")
    # sleep(1)
    chessboard.undraw_possible_moves(list_circles)
    chessboard.move_piece(piece, current_player, piece_index, i, j)


def switch_players(current_player):
    if current_player == "white":
        return "black"
    return "white"


def main():
    current_player = "white"
    print("setting up game")
    _setup_game()
    while True:
        round(current_player)
        current_player = switch_players(current_player)


main()
