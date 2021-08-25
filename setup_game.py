from genericpath import exists
from os import *
from graphics import *
from time import sleep
from utils import *


class Setup_game:
    def __init__(self, black, white, size):
        self.black = black
        self.white = white
        self.sqsize = size
        self.pic_dir = "pieces"
        self.win = GraphWin(
            "Schackbrädet", 8 * self.sqsize + self.sqsize * 2, 8 * self.sqsize
        )
        self.pieces_info = pieces()

    def check(self, current_player: str) -> bool:
        other_player = self.get_other_player(current_player)
        i_king, j_king = self.pieces_info["kung"][current_player][1]["pos"]

        for piece in self.pieces_info:
            for piece_index in self.pieces_info[piece][other_player]:
                if king_is_check(
                    self, piece, piece_index, other_player, i_king, j_king
                ):
                    return True
        return False

    def check_possibilities(
        self,
        piece: str,
        piece_index: int,
        current_player: str,
        only_attack: bool,
    ):
        i, j = self.pieces_info[piece][current_player][piece_index]["pos"]
        possible_moves = []
        rules = self.pieces_info[piece]["rules"]
        dir = 1
        other_player = "black"
        rekursive = rules["rekursive"]
        if current_player == "black":
            dir = -1
            other_player = "white"

        if piece == "bonde":
            # checks if bonde can attack
            possible_moves = bonde_attack(self, other_player, i, j, dir)
            if only_attack:
                return possible_moves
            if self.pieces_info[piece][current_player][piece_index]["moved"]:
                rekursive = 1

        # checking other possibilites

        add_move_list = rules["standard_move"]
        for i_add, j_add in add_move_list:
            for steps in range(rekursive):
                steps = steps + 1
                temp_i = i + i_add * steps * dir
                temp_j = j + j_add * steps
                temp_move = (temp_i, temp_j)
                bre, temp_move = check_one_posibility(
                    self,
                    piece,
                    current_player,
                    piece_index,
                    temp_i,
                    temp_j,
                    other_player,
                )
                if temp_move != None:
                    possible_moves.append(temp_move)
                if bre == "break":
                    break

        return possible_moves  # kolla så att detta inte gör så att man står i schack
        # returns a list of tuples of i,j possible moves

    def potential_movement_check(
        self, piece: str, piece_index: int, current_player: str, possible_moves: list
    ) -> list:  # returns True if movement leads to check on my self
        other_player = self.get_other_player(current_player)
        m = 0
        new_possible_moves = possible_moves.copy()
        for i, j in possible_moves:
            i_orig, j_orig = self.pieces_info[piece][current_player][piece_index]["pos"]
            self.pieces_info[piece][current_player][piece_index]["pos"] = (i, j)

            # temporary remove piece if it kills anyone
            [object, remove_piece, remove_piece_index] = self.remove_piece(
                other_player, i, j, False
            )
            if piece != "kung":
                if self.check(current_player):
                    new_possible_moves.pop(m)
                    m -= 1
                    print("tar bort ett alternativ pga det ställer dig i schack")

            # restore piece
            if object != None:
                self.restore_piece(
                    remove_piece, other_player, remove_piece_index, object
                )

            self.pieces_info[piece][current_player][piece_index]["pos"] = (
                i_orig,
                j_orig,
            )
            m += 1
        return new_possible_moves

    def remove_piece(
        self, current_player: str, i: int, j: int, graphical: bool
    ) -> dict:
        remove_piece, remove_piece_index = self.exist_piece_here(current_player, i, j)
        if remove_piece != None:
            if graphical:
                graphic_image = self.pieces_info[remove_piece][current_player][
                    remove_piece_index
                ]["pic"]
                graphic_image.undraw()
            object = self.pieces_info[remove_piece][current_player][remove_piece_index]
            del self.pieces_info[remove_piece][current_player][remove_piece_index]
            return [object, remove_piece, remove_piece_index]
        return None, None, None

    def restore_piece(
        self, piece: str, current_player: str, piece_index: int, object: dict
    ):
        self.pieces_info[piece][current_player][piece_index] = object

    def check_spot(self, i: int, j: int, possible_moves: list) -> bool:
        for i_temp, j_temp in possible_moves:
            if i_temp == i:
                if j_temp == j:
                    return True
        return False

    def exist_piece_here(self, check_player: str, i: int, j: int):

        if check_player == "both":
            check_players = ["white", "black"]
        else:
            check_players = [check_player]
        for check_player in check_players:
            for piece in self.pieces_info:
                piece_dict = self.pieces_info[piece][check_player]
                for piece_index in piece_dict:
                    i_temp, j_temp = piece_dict[piece_index]["pos"]
                    if i_temp == i:
                        if j_temp == j:
                            return piece, piece_index
        return None, None

    def undraw_possible_moves(self, list_circles: list):
        for circle in list_circles:
            circle.undraw()

    def move_piece(
        self, piece: str, current_player: str, piece_index: int, i: int, j: int
    ):
        i_pre, j_pre = self.pieces_info[piece][current_player][piece_index]["pos"]
        self.pieces_info[piece][current_player][piece_index]["pos"] = (i, j)

        graphic_piece = self.pieces_info[piece][current_player][piece_index]["pic"]
        delta_i = i - i_pre
        delta_j = j - j_pre
        i_px = int(convert_to_px(delta_i, self.sqsize) + self.sqsize / 2)
        j_px = int(convert_to_px(delta_j, self.sqsize) + self.sqsize / 2)
        graphic_piece.move(i_px, j_px)
        if piece == "bonde":
            self.pieces_info[piece][current_player][piece_index]["moved"] = True

    def draw_possible_moves(self, possible_moves: list):
        list_circles = []
        radius = self.sqsize / 8
        for i, j in possible_moves:
            x = convert_to_px(i, self.sqsize)
            y = convert_to_px(j, self.sqsize)
            circle = Circle(Point(x, y), radius)
            circle.setFill("blue")
            circle.draw(self.win)
            list_circles.append(circle)
        return list_circles

    def draw_board(self):
        for x in range(8):
            for y in range(8):
                square = Rectangle(
                    Point(x * self.sqsize, y * self.sqsize),
                    Point(x * self.sqsize + self.sqsize, y * self.sqsize + self.sqsize),
                )
                if (x % 2 == 0 and y % 2 == 0) or (x % 2 > 0 and y % 2 > 0):
                    square.setFill(self.white)
                else:
                    square.setFill(self.black)
                square.draw(self.win)

    def draw_pieces(self):
        for piece in listdir(self.pic_dir):
            color, name = piece.split("_")
            name = name[:-4]
            piece_dict = self.pieces_info[name][color]
            for piece_index in piece_dict:
                i, j = piece_dict[piece_index]["pos"]
                self._draw_piece(piece, i, j, name, color, piece_index)

    def _draw_piece(
        self, img: str, i: int, j: int, name: str, color: str, piece_index: int
    ):
        ipx = convert_to_px(i, self.sqsize)
        jpx = convert_to_px(j, self.sqsize)
        myImage = Image(Point(ipx, jpx), self.pic_dir + "/" + img)
        myImage.draw(self.win)
        self.pieces_info[name][color][piece_index]["pic"] = myImage

    def get_other_player(self, current_player):
        if current_player == "black":
            return "white"
        return "black"

    def get_mouse_position(self):
        while True:
            mouse = self.win.getMouse()
            x, y = str(mouse)[6:-1].split(",")
            x = float(x)
            y = float(y)
            i, j = convert_to_i_j(x, y, self.sqsize)
            return i, j
