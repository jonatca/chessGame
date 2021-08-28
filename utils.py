from graphics import *
import datetime
from typing import List, Set, Dict, Tuple, Optional, Callable


def convert_to_px(i: int, sqsize: int) -> int:
    return i * sqsize - sqsize / 2


def convert_to_i_j(chessboard, x: float, y: float) -> Tuple[int, int]:
    j = int(y / chessboard.sqsize + 1)
    i = int(x / chessboard.sqsize + 1 - chessboard.extra_side_space)
    return i, j


def pieces(white_name: str, black_name: str):
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
) -> bool:
    Setup_game.possible_moves = Setup_game.check_possibilities(
        piece, piece_index, current_player, True
    )
    for i, j in Setup_game.possible_moves:
        if i_king == i:
            if j_king == j:
                return True
    return False


def bol_exist_piece_here(Setup_game, check_player: str, i: int, j: int) -> bool:
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
) -> Tuple[str, Tuple[int, int]]:
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


def calc_time_past(index: int, elapsed_time: int, tot_elapsed_time: List) -> List:

    last_time = tot_elapsed_time[index]
    delta_time = elapsed_time - last_time
    tot_elapsed_time[index] += delta_time
    return tot_elapsed_time


def get_time_formated(num_secounds: int) -> str:
    formatted_time = str(datetime.timedelta(seconds=num_secounds))
    # print(len(formatted_time), "längd")
    if len(formatted_time) == 14:
        formatted_time = formatted_time[:-5]
    return formatted_time


def is_inside(x: int, y: int, min_x: int, min_y: int, max_x: int, max_y: int) -> bool:
    if x >= min_x:
        if x <= max_x:
            if y >= min_y:
                if y <= max_y:
                    return True
    return False


def set_button_bol(chessboard, bol: bool):
    [
        chessboard.black_kingside_button_on,
        chessboard.white_kingside_button_on,
        chessboard.black_queenside_button_on,
        chessboard.white_queenside_button_on,
        chessboard.start_button_on,
        chessboard.pause_button_on,
    ] = bol


def get_button_info(
    chessboard,
) -> List:
    # List[bool],
    # List[str],
    # List[Tuple[int]],
    # List[Callable],
    # List[Callable],
    # List[object],
    # List[str],

    button_on = [
        chessboard.black_kingside_button_on,
        chessboard.white_kingside_button_on,
        chessboard.black_queenside_button_on,
        chessboard.white_queenside_button_on,
        chessboard.start_button_on,
        chessboard.pause_button_on,
    ]
    player = [
        chessboard.black_name,
        chessboard.white_name,
        chessboard.black_name,
        chessboard.white_name,
        "start",
        "pause",
    ]
    button_center = [
        chessboard.black_kingside_button_center,
        chessboard.white_kingside_button_center,
        chessboard.black_queenside_button_center,
        chessboard.white_queenside_button_center,
        chessboard.start_button_center,
        chessboard.pause_button_center,
    ]
    side_fun_do = [
        chessboard.do_rochade,
        chessboard.do_rochade,
        chessboard.do_rochade,
        chessboard.do_rochade,
        chessboard.start_game,
        chessboard.pause_game,
    ]
    side_fun_can_do = [
        chessboard.can_do_rochade,
        chessboard.can_do_rochade,
        chessboard.can_do_rochade,
        chessboard.can_do_rochade,
        None,
        None,
    ]
    button = [
        chessboard.black_kingside_button,
        chessboard.white_kingside_button,
        chessboard.black_queenside_button,
        chessboard.white_queenside_button,
        chessboard.start_button,
        chessboard.pause_button,
    ]
    side = ["kung", "kung", "dam", "dam", None, None]
    return [
        button_on,
        player,
        button_center,
        side_fun_do,
        side_fun_can_do,
        button,
        side,
    ]


def get_button_boundaries(chessboard, button_center: tuple) -> List:  # [int]:
    min_x = button_center[0] - chessboard.button_size[0] / 2
    min_y = button_center[1] - chessboard.button_size[1] / 2
    max_x = button_center[0] + chessboard.button_size[0] / 2
    max_y = button_center[1] + chessboard.button_size[1] / 2
    return [min_x, min_y, max_x, max_y]


def restore_piece(
    chessboard, piece: str, current_player: str, piece_index: int, object: dict
):
    chessboard.pieces_info[piece][current_player][piece_index] = object


def check_spot(i: int, j: int, possible_moves: list) -> bool:
    for i_temp, j_temp in possible_moves:
        if i_temp == i:
            if j_temp == j:
                return True
    return False
