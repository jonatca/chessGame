from os import *
from graphics import *
from utils import *
from button import *
from time import perf_counter as pc
from typing import List, Set, Dict, Tuple, Optional, Callable


class Setup_game:
    def __init__(self, dark_col, light_col, size, white_name, black_name):
        self.black = dark_col
        self.white = light_col
        self.white_name = white_name
        self.black_name = black_name
        self.sqsize = size
        self.set_initial_values()
        self.win = GraphWin(
            "Schackbrädet",
            self.num_squares * self.sqsize + self.sqsize * self.extra_side_space * 2,
            self.num_squares * self.sqsize,
        )
        self.win.setBackground("lightblue")

    def set_initial_values(self):
        self.num_squares = 8
        self.extra_side_space = 3.859  # gives isch 16/9 res
        self.pic_dir = "pieces"
        self.possible_moves = []
        self.black_kingside_button_on = True
        self.white_kingside_button_on = True
        self.black_queenside_button_on = True
        self.white_queenside_button_on = True
        self.start_button_on = False
        self.pause_button_on = True
        self.time_is_up = False
        self.settings_button_clicked = False
        self.pause_time = {self.white_name: 0, self.black_name: 0}
        self.button_size = (self.sqsize * 2.4, self.sqsize / 2)  # width,hieght
        self.pieces_info = pieces(self.white_name, self.black_name)

    def get_time_is_up(self) -> bool:
        return self.time_is_up

    def get_start_button_on(self) -> bool:
        return self.start_button_on

    def get_pause_button_on(self) -> bool:
        return self.pause_button_on

    def queening_the_pawn(self, current_player: str, i: int, j: int):
        i_goal = 8
        if current_player == self.black_name:
            i_goal = 1
        if i == i_goal:
            self.remove_piece(current_player, i, j, True)
            img_name = current_player + "_dam.png"
            new_piece_index = len(self.pieces_info["dam"][current_player]) + 1
            self.pieces_info["dam"][current_player][new_piece_index] = {
                "pos": (i, j),
                "moved": True,
            }
            self._draw_piece(img_name, i, j, "dam", current_player, new_piece_index)

    def turn_on_buttons(self):
        [
            button_on,
            player,
            _,
            _,
            side_fun_can_do,
            button,
            side,
        ] = get_button_info(self)
        bol = []
        for m in range(len(button)):
            bol_temp = True
            if not button_on[m]:
                if side_fun_can_do[m] == None:
                    bol_temp = False
                elif side_fun_can_do[m](player[m], side[m]):
                    button[m].activate()
                else:
                    bol_temp = False
            elif side_fun_can_do[m] == None:
                button[m].activate()

            bol.append(bol_temp)
        set_button_bol(self, bol)

    def turn_off_buttons(self):
        [
            button_on,
            player,
            _,
            _,
            side_fun_can_do,
            button,
            side,
        ] = get_button_info(self)
        bol = []
        for m in range(len(button)):
            bol_temp = False
            if button_on[m]:
                if side_fun_can_do[m] == None:
                    bol_temp = True
                elif not side_fun_can_do[m](player[m], side[m]):
                    button[m].deactivate()
                else:
                    bol_temp = True
            elif side_fun_can_do[m] == None:
                button[m].deactivate()

            bol.append(bol_temp)

        set_button_bol(self, bol)

    def start_game(self, _, not_used):
        print("starts game")
        self.settings_button_clicked = True
        self.pause_button_on = True
        self.start_button_on = False
        self.pause_button.activate()
        self.start_button.deactivate()

    def pause_game(self, current_player: str, _):
        print("pauses game")
        self.start_button.activate()
        self.pause_button.deactivate()
        self.settings_button_clicked = True
        self.pause_button_on = False
        self.start_button_on = True
        start = pc()
        x, y = self.get_mouse_position()
        while self.check_which_button_clicked(x, y)[1] != "start":
            x, y = self.get_mouse_position()
            print("pausing")
        end = pc()
        self.pause_time[current_player] += end - start

    def check_which_button_clicked(
        self, x: float, y: float, current_player: str = None
    ) -> Tuple:
        [
            button_on,
            player,
            button_center,
            side_fun_do,
            _,
            _,
            side,
        ] = get_button_info(self)
        for m in range(len(button_on)):
            if current_player == player[m] or player[m] in ["start", "pause"]:
                if button_on[m]:
                    min_x, min_y, max_x, max_y = get_button_boundaries(
                        self, button_center[m]
                    )
                    if is_inside(x, y, min_x, min_y, max_x, max_y):
                        side_fun_do[m](current_player, side[m])
                        return True, player[m]
        return False, False

    def setup_buttons(self):
        self.set_button_centers()
        self._setup_buttons()

    def set_button_centers(self):
        self.black_kingside_button_center = (
            self.sqsize * (self.num_squares + self.extra_side_space * 3 / 2),
            (self.sqsize * (self.num_squares * 4 / 16)),
        )
        self.white_kingside_button_center = (
            self.sqsize * (self.extra_side_space / 2),
            (self.sqsize * (self.num_squares * 4 / 16)),
        )
        self.black_queenside_button_center = (
            self.sqsize * (self.num_squares + self.extra_side_space * 3 / 2),
            (self.sqsize * (self.num_squares * 6 / 16)),
        )
        self.white_queenside_button_center = (
            self.sqsize * (self.extra_side_space / 2),
            (self.sqsize * (self.num_squares * 6 / 16)),
        )
        self.start_button_center = (
            self.sqsize * (self.extra_side_space / 2),
            (self.sqsize * (self.num_squares * 8 / 16)),
        )
        self.pause_button_center = (
            self.sqsize * (self.extra_side_space / 2),
            (self.sqsize * (self.num_squares * 10 / 16)),
        )

    def _setup_buttons(self):
        button_center = [
            self.black_kingside_button_center,
            self.white_kingside_button_center,
            self.black_queenside_button_center,
            self.white_queenside_button_center,
            self.start_button_center,
            self.pause_button_center,
        ]
        message = [
            "Rokad kungsidan",
            "Rokad kungsidan",
            "Rokad damsidan",
            "Rokad damsidan",
            "Start",
            "Paus",
        ]
        button_name = []
        for m in range(len(button_center)):
            button_name.append(
                Button(
                    self.win,
                    Point(
                        button_center[m][0],
                        button_center[m][1],
                    ),
                    self.button_size[0],
                    self.button_size[1],
                    message[m],
                )
            )
            button_name[m].activate()
        [
            self.black_kingside_button,
            self.white_kingside_button,
            self.black_queenside_button,
            self.white_queenside_button,
            self.start_button,
            self.pause_button,
        ] = button_name

    def can_do_rochade(self, player: str, side) -> bool:
        i = 1
        j_list = [2, 3]
        if player == self.black_name:
            i = 8
        torn_index = 1
        if side == "dam":
            j_list = [5, 6, 7]
            torn_index = 2
        if torn_index in self.pieces_info["torn"][player]:
            torn_moved = self.pieces_info["torn"][player][torn_index]["moved"]
            kung_moved = self.pieces_info["kung"][player][1]["moved"]

            if not torn_moved:
                if not kung_moved:
                    for temp_j in j_list:
                        if bol_exist_piece_here(self, player, i, temp_j):
                            return False
                    return True
        return False

    def do_rochade(self, player: str, side: str):
        i = 1
        j_list = [2, 3]
        torn_index = 1
        if player == self.black_name:
            i = 8
        if side == "dam":
            j_list = [6, 5]
            torn_index = 2

        self.move_piece("kung", player, 1, i, j_list[0])
        self.move_piece("torn", player, torn_index, i, j_list[1])

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

    def has_possible_moves(self, player: str) -> bool:
        for piece in self.pieces_info:
            for piece_index in self.pieces_info[piece][player]:

                possible_moves = self.get_possible_moves(
                    piece, piece_index, player, False
                )
                if possible_moves != []:
                    return True
        return False

    def check_mate(self, other_player: str) -> bool:
        if self.check(other_player):
            if not self.has_possible_moves(other_player):
                return True
        return False

    def equal(self, other_player: str):
        if not self.has_possible_moves(other_player):
            return True
        return False

    def get_possible_moves(
        self,
        piece: str,
        piece_index: int,
        current_player: str,
        only_attack: bool,
    ) -> List:
        possible_moves_with_check = self.check_possibilities(
            piece, piece_index, current_player, only_attack
        )

        possible_moves = self.potential_movement_check(
            piece, piece_index, current_player, possible_moves_with_check
        )
        return possible_moves

    def check_possibilities(
        self,
        piece: str,
        piece_index: int,
        current_player: str,
        only_attack: bool,
    ) -> List:
        i, j = self.pieces_info[piece][current_player][piece_index]["pos"]
        possible_moves = []
        rules = self.pieces_info[piece]["rules"]
        dir = 1
        other_player = self.black_name
        rekursive = rules["rekursive"]
        if current_player == self.black_name:
            dir = -1
            other_player = self.white_name

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
        return possible_moves
        # returns a list of tuples of i,j possible moves

    def potential_movement_check(
        self, piece: str, piece_index: int, current_player: str, possible_moves: list
    ) -> List:
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
            # if piece != "kung":  # ta bort denna
            if self.check(current_player):
                new_possible_moves.pop(m)
                m -= 1

            # restore piece
            if object != None:
                restore_piece(
                    self, remove_piece, other_player, remove_piece_index, object
                )

            self.pieces_info[piece][current_player][piece_index]["pos"] = (
                i_orig,
                j_orig,
            )
            m += 1
        return new_possible_moves

    def remove_piece(
        self, current_player: str, i: int, j: int, graphical: bool
    ) -> List:  # [object, str, int]:
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

    def exist_piece_here(self, check_player: str, i: int, j: int) -> Tuple[str, int]:

        if check_player == "both":
            check_players = [self.white_name, self.black_name]
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

    def undraw_possible_moves(self, list_circles: list):  # util
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
        self.pieces_info[piece][current_player][piece_index]["moved"] = True

    def draw_possible_moves(self, possible_moves: list) -> List:
        list_circles = []
        radius = self.sqsize / 8
        for i, j in possible_moves:
            x = convert_to_px(i + self.extra_side_space, self.sqsize)
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
                    Point((x + self.extra_side_space) * self.sqsize, y * self.sqsize),
                    Point(
                        (x + self.extra_side_space) * self.sqsize + self.sqsize,
                        y * self.sqsize + self.sqsize,
                    ),
                )
                if (x % 2 == 0 and y % 2 == 0) or (x % 2 > 0 and y % 2 > 0):
                    square.setFill(self.white)
                else:
                    square.setFill(self.black)
                square.draw(self.win)

    def draw_pieces(self):
        for img_name in listdir(self.pic_dir):
            color, piece = img_name.split("_")
            if color == "black":
                color = self.black_name
            else:
                color = self.white_name

            piece = piece[:-4]
            piece_dict = self.pieces_info[piece][color]
            for piece_index in piece_dict:
                i, j = piece_dict[piece_index]["pos"]
                # i, j = convert_to_pos(self.white_position, i, j)
                self._draw_piece(img_name, i, j, piece, color, piece_index)

    def _draw_piece(
        self, img: str, i: int, j: int, piece: str, color: str, piece_index: int
    ) -> str:
        ipx = convert_to_px(i + self.extra_side_space, self.sqsize)
        jpx = convert_to_px(j, self.sqsize)
        myImage = Image(Point(ipx, jpx), self.pic_dir + "/" + img)
        myImage.draw(self.win)
        self.pieces_info[piece][color][piece_index]["pic"] = myImage

    def get_other_player(self, current_player) -> str:
        if current_player == self.black_name:
            return self.white_name
        return self.black_name

    def get_mouse_position(
        self,
        pc: Callable = None,
        tot_elapsed_time: List = None,
        current_player: str = None,
    ) -> Tuple[int, int]:
        mouse = self.win.getMouseWithTime(pc, tot_elapsed_time, current_player, self)
        x, y = str(mouse)[6:-1].split(",")
        x = float(x)
        y = float(y)
        return x, y

    def set_start_time(self, white_start_time: float, black_start_time: float):
        self.white_start_time = white_start_time * 60
        self.black_start_time = black_start_time * 60

    # def get_start_time(self) -> Tuple[int, int]:
    #     return self.white_start_time, self.black_start_time

    def output_time_left(self, stop: int, tot_elapsed_time: list, current_player: str):
        index = 0
        if current_player == self.black_name:
            index = 1
        elapsed_time = stop - tot_elapsed_time[index]  # remove other players time
        if index == 1:
            tot_elapsed_time = calc_time_past(0, elapsed_time, tot_elapsed_time)
            time_left = (
                self.white_start_time
                - tot_elapsed_time[0]
                + self.pause_time[current_player]
            )
        if index == 0:
            tot_elapsed_time = calc_time_past(1, elapsed_time, tot_elapsed_time)
            time_left = (
                self.black_start_time
                - tot_elapsed_time[1]
                + self.pause_time[current_player]
            )
        time_formatted = get_time_formated(time_left)
        if time_left <= 0:
            self.time_is_up = True
            time_formatted = 0
        self.update_timer(time_formatted, current_player)

    def update_timer(self, time_formatted: str, current_player: str):
        # update text with new time_formatted
        index = 2
        if current_player == self.black_name:
            index = 3

        self.time_text[index].setText(time_formatted)

    def setup_text(self, white: str, black: str):
        self.time_text = []
        j = [1, 1, 2, 2]
        i = [
            self.extra_side_space / 2,
            self.num_squares + self.extra_side_space * 3 / 2,
            self.extra_side_space / 2,
            self.num_squares + self.extra_side_space * 3 / 2,
        ]

        output_message = [
            white,
            black,
            get_time_formated(self.white_start_time),
            get_time_formated(self.black_start_time),
        ]
        for m in range(len(j)):
            time_text = Text(
                Point(
                    self.sqsize * i[m],
                    (self.sqsize * (self.num_squares * j[m] / 16)),
                ),
                output_message[m],
            )  # eftersom jag printar nedifrån vänster och upp
            time_text.draw(self.win)
            self.time_text.append(time_text)

    def undraw_circles(self, list_circles: List):
        if list_circles != []:
            self.undraw_possible_moves(list_circles)

    def set_winners_text(self, output_message: str):

        # winning_player = self.get_other_player(losing_player)

        i_list = [
            self.extra_side_space / 2,
            self.num_squares + 3 / 2 * self.extra_side_space,
        ]
        color = [self.white_name, self.black_name]
        for m in range(len(output_message)):
            if color[m] != None:
                temp_text = Text(
                    Point(
                        self.sqsize * i_list[m],
                        self.sqsize * (self.num_squares * 13 / 16),
                    ),
                    output_message[color[m]],
                )  # eftersom jag printar nedifrån vänster och upp
                temp_text.setSize(19)
                temp_text.setTextColor("black")
                temp_text.draw(self.win)

    def set_check_text(self, player: str):
        index = 0
        if player == self.black_name:
            index = 1

        i_list = [
            self.extra_side_space / 2,
            self.num_squares + 3 / 2 * self.extra_side_space,
        ]

        self.check_text = Text(
            Point(
                self.sqsize * i_list[index],
                self.sqsize * (self.num_squares * 13 / 16),
            ),
            "Check",
        )  # eftersom jag printar nedifrån vänster och upp
        self.check_text.setSize(19)
        self.check_text.setTextColor("black")
        self.check_text.draw(self.win)

    def undraw_check_text(self):
        try:
            self.check_text.undraw()
        except AttributeError:
            pass

    def check_if_game_over(
        self, current_player: str, other_player: str
    ) -> Tuple[bool, str]:
        game_running = True
        output_message = None
        if self.get_time_is_up():
            output_message = {
                other_player: f"Time is up\nGood job {other_player}\nYou win!",
                current_player: f"Time is up\nNice try {current_player}\nYou lost",
            }
            game_running = False
        elif self.check_mate(other_player):
            output_message = {
                current_player: f"Check mate,\nGood job {current_player}\nYou win!",
                other_player: f"Check mate\nNice try {other_player}\nYou lost",
            }
            game_running = False
        elif self.equal(other_player):
            output_message = {
                current_player: f"Equal,\nGood job {current_player}",
                other_player: f"Equal\nGood job {other_player}",
            }
            game_running = False
        return game_running, output_message
