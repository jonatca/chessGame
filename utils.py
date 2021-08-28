from graphics import *
import datetime


def convert_to_px(i: int, sqsize: int) -> int:
    return i * sqsize - sqsize / 2


def convert_to_i_j(chessboard, x: float, y: float) -> int:
    j = int(y / chessboard.sqsize + 1)
    i = int(x / chessboard.sqsize + 1 - chessboard.extra_side_space)
    return i, j


def convert_to_pos(white_position, i, j):
    if white_position == "down":
        pass
    return 9 - j, 9 - i


def pieces(white_name, black_name):
    torn_movement = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # (i,j), i=x=right
    lopare_movement = [(1, 1), (-1, -1), (1, -1), (-1, 1)]

    pieces_info = {
        "bonde": {
            white_name: {
                1: {"pos": (2, 1), "moved": False},
                2: {"pos": (2, 2), "moved": False},
                3: {"pos": (2, 3), "moved": False},
                4: {"pos": (2, 4), "moved": False},
                5: {"pos": (2, 5), "moved": False},
                6: {"pos": (2, 6), "moved": False},
                7: {"pos": (2, 7), "moved": False},
                8: {"pos": (2, 8), "moved": False},
            },
            black_name: {
                1: {"pos": (7, 1), "moved": False},
                2: {"pos": (7, 2), "moved": False},
                3: {"pos": (7, 3), "moved": False},
                4: {"pos": (7, 4), "moved": False},
                5: {"pos": (7, 5), "moved": False},
                6: {"pos": (7, 6), "moved": False},
                7: {"pos": (7, 7), "moved": False},
                8: {"pos": (7, 8), "moved": False},
            },
            "rules": {
                "standard_move": [(1, 0)],  # i,j
                "attack_move": [(1, 1), (1, -1)],
                "rekursive": 2,  # change this to 1 if moved == True
            },
        },
        "torn": {
            white_name: {
                1: {"pos": (1, 1), "moved": False},
                2: {"pos": (1, 8), "moved": False},
            },
            black_name: {
                1: {"pos": (8, 1), "moved": False},
                2: {"pos": (8, 8), "moved": False},
            },
            "rules": {
                "standard_move": torn_movement,
                "rekursive": 8,
            },
        },
        "hast": {
            white_name: {
                1: {"pos": (1, 2), "moved": False},
                2: {"pos": (1, 7), "moved": False},
            },
            black_name: {
                1: {"pos": (8, 2), "moved": False},
                2: {"pos": (8, 7), "moved": False},
            },
            "rules": {
                "standard_move": [
                    (2, 1),
                    (2, -1),
                    (1, 2),
                    (-1, 2),
                    (-2, 1),
                    (-2, -1),
                    (1, -2),
                    (-1, -2),
                ],  # i,j
                "rekursive": 1,
            },
        },
        "lopare": {
            white_name: {
                1: {"pos": (1, 3), "moved": False},
                2: {"pos": (1, 6), "moved": False},
            },
            black_name: {
                1: {"pos": (8, 3), "moved": False},
                2: {"pos": (8, 6), "moved": False},
            },
            "rules": {
                "standard_move": lopare_movement,
                "rekursive": 8,
            },
        },
        "kung": {
            white_name: {1: {"pos": (1, 4), "moved": False}},
            black_name: {1: {"pos": (8, 4), "moved": False}},
            "rules": {
                "standard_move": lopare_movement + torn_movement,
                "rekursive": 1,
            },
        },
        "dam": {
            white_name: {1: {"pos": (1, 5), "moved": False}},
            black_name: {1: {"pos": (8, 5), "moved": False}},
            "rules": {
                "standard_move": lopare_movement + torn_movement,
                "rekursive": 8,
            },
        },
    }
    return pieces_info


def bonde_attack(Setup_game, other_player: str, i: int, j: int, dir: int) -> list:
    possible_moves = []
    attack_position = [(i + dir, j + 1), (i + dir, j - 1)]
    for m in range(len(attack_position)):
        temp_piece, temp_piece_index = Setup_game.exist_piece_here(
            other_player, attack_position[m][0], attack_position[m][1]
        )
        if temp_piece != None:
            possible_moves.append((attack_position[m][0], attack_position[m][1]))
    return possible_moves


def outside_board(i: int, j: int):
    return i < 1 or i > 8 or j < 1 or j > 8


def king_is_check(
    Setup_game,
    piece: str,
    piece_index: int,
    current_player: str,
    i_king: int,
    j_king: int,
):
    Setup_game.possible_moves = Setup_game.check_possibilities(
        piece, piece_index, current_player, True
    )
    # lägg till functionen potential_movement_check
    for i, j in Setup_game.possible_moves:
        if i_king == i:
            if j_king == j:
                return True
    return False


def bol_exist_piece_here(Setup_game, check_player: str, i: int, j: int):
    piece, piece_index = Setup_game.exist_piece_here(check_player, i, j)
    if piece == None:
        return False
    return True


def check_one_posibility(
    Setup_game,
    piece: str,
    current_player: str,
    piece_index: int,
    temp_i: int,
    temp_j: int,
    other_player: str,
):
    temp_move = (temp_i, temp_j)
    if outside_board(temp_i, temp_j):
        return "break", None

    elif bol_exist_piece_here(Setup_game, current_player, temp_i, temp_j):
        return "break", None

    if bol_exist_piece_here(Setup_game, other_player, temp_i, temp_j):
        if piece == "bonde":
            return "break", None
        else:
            return "break", temp_move
    else:
        return None, temp_move


def calc_time_past(index, elapsed_time, tot_elapsed_time) -> list:
    last_time = tot_elapsed_time[index]
    delta_time = elapsed_time - last_time
    tot_elapsed_time[index] += delta_time
    return tot_elapsed_time


def get_time_formated(num_secounds):
    formatted_time = str(datetime.timedelta(seconds=num_secounds))
    # print(len(formatted_time), "längd")
    if len(formatted_time) == 14:
        formatted_time = formatted_time[:-5]
    return formatted_time
