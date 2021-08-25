from graphics import *


def convert_to_px(i: int, sqsize: int) -> int:  # ok
    return i * sqsize - sqsize / 2


def convert_to_i_j(x: float, y: float, sqsize: int):  # ok
    j = int(y / sqsize) + 1
    i = int(x / sqsize) + 1
    return i, j


def pieces():
    torn_movement = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    lopare_movement = [(1, 1), (-1, -1), (1, -1), (-1, 1)]

    pieces_info = {
        "bonde": {
            "white": {
                1: {"pos": (2, 1), "moved": False},
                2: {"pos": (2, 2), "moved": False},
                3: {"pos": (2, 3), "moved": False},
                4: {"pos": (2, 4), "moved": False},
                5: {"pos": (2, 5), "moved": False},
                6: {"pos": (2, 6), "moved": False},
                7: {"pos": (2, 7), "moved": False},
                8: {"pos": (2, 8), "moved": False},
            },
            "black": {
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
                "rekursive": 2,  # change this to 1 when moved == True
            },
        },
        "torn": {
            "white": {1: {"pos": (1, 1)}, 2: {"pos": (1, 8)}},
            "black": {1: {"pos": (8, 1)}, 2: {"pos": (8, 8)}},
            "rules": {
                "standard_move": torn_movement,  # i,j
                "rekursive": 8,
            },
        },
        "hast": {
            "white": {1: {"pos": (1, 2)}, 2: {"pos": (1, 7)}},
            "black": {1: {"pos": (8, 2)}, 2: {"pos": (8, 7)}},
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
            "white": {1: {"pos": (1, 3)}, 2: {"pos": (1, 6)}},
            "black": {1: {"pos": (8, 3)}, 2: {"pos": (8, 6)}},
            "rules": {
                "standard_move": lopare_movement,  # i,j
                "rekursive": 8,
            },
        },
        "kung": {
            "white": {1: {"pos": (1, 5)}},
            "black": {1: {"pos": (8, 5)}},
            "rules": {
                "standard_move": lopare_movement + torn_movement,  # i,j
                "rekursive": 1,
            },
        },
        "dam": {
            "white": {1: {"pos": (1, 4)}},
            "black": {1: {"pos": (8, 4)}},
            "rules": {
                "standard_move": lopare_movement + torn_movement,  # i,j
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


def outside_board(i, j):
    return i < 1 or i > 8 or j < 1 or j > 8


def king_is_check(Setup_game, piece, piece_index, current_player, i_king, j_king):
    possible_moves = Setup_game.check_possibilities(
        piece, piece_index, current_player, True
    )
    #lägg till functionen potential_movement_check
    for i, j in possible_moves:
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
    Setup_game, piece, current_player, piece_index, temp_i, temp_j, other_player
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
