import random
import time

from GameLogic.GameGrid import GameGrid


class GameLogic:

    def __init__(self, y_size, x_size, difficulty):
        self.difficulty_map = {1: 0.14, 2: 0.17, 3: 0.20, 4: 0.23, 5: 0.26}
        percentage_of_mines = self.difficulty_map[difficulty]

        self.game_grid = GameGrid(y_size, x_size, percentage_of_mines)

        self.mine_count_digit_len = len("{}".format(self.game_grid.mine_count))
        self.remaining_mines = self.game_grid.mine_count

        self.next_fields = set()
        self.render_list = set()
        self.open_fields = set()

        # gamestate
        self.first = True
        self.loose = False
        self.win = False
        self.cheat = False
        self.pause = False

        # status Windowstuff
        self.start_time = 0
        self.sum_time = 0
        self.current_time_str = ""
        self.cheat_count = 0

    # Is called on click of a field
    def click_field(self, y, x):
        field = self.game_grid.get_field_with_coordinates((y, x))
        if not field.get_flag():
            if not field.get_mine():
                self.check_field(field)
                self.check_next_fields()
            else:
                self.loose = True

    # Checks the fields around the field that is called in click_field and opens the field
    def check_field(self, field):
        y, x = field.get_coordinates()
        field.set_open(True)
        self.render_list.add(field)
        self.open_fields.add((y, x))
        if field.get_number() == 0:
            neighbors = self.game_grid.neighbors_of_coordinates(y, x)
            for tup in neighbors:
                tup_field = self.game_grid.get_field_with_coordinates(tup)
                if not tup_field.get_open():
                    self.next_fields.add(tup_field)

    def check_next_fields(self):
        while self.next_fields:
            none_matching_fields = set([])
            for i in self.next_fields:
                if i.get_open() or i.get_coordinates() in self.game_grid.boarder:
                    none_matching_fields.add(i)
            self.next_fields = self.next_fields - none_matching_fields
            if self.next_fields:
                i_field = self.next_fields.pop()
                self.check_field(i_field)

    def quality_of_life_click(self, y, x):
        cur_field = self.game_grid.grid[y][x]
        if cur_field.get_number() != 0:
            if self.count_flags(y, x) == cur_field.get_number():
                neighbors = self.game_grid.neighbors_of_coordinates(y, x)
                for t in neighbors:
                    t_field = self.game_grid.get_field_with_coordinates(t)
                    if t_field.get_flag() or t_field.get_open():
                        continue
                    if not t_field.get_mine():
                        self.check_field(t_field)
                        self.check_next_fields()
                    else:
                        self.loose = True

    def add_field_to_render_list(self, coordinates):
        field = self.game_grid.get_field_with_coordinates(coordinates)
        self.render_list.add(field)

    def count_flags(self, y, x):
        adj_list = self.game_grid.neighbors_of_coordinates(y, x)
        flags = 0
        for i in adj_list:
            i_field = self.game_grid.get_field_with_coordinates(i)
            if i_field.get_flag():
                flags += 1
        return flags

    def flag_field(self, y, x):
        cur_field = self.game_grid.grid[y][x]
        if not cur_field.get_open():
            if not cur_field.get_flag():
                cur_field.set_flag(True)
                self.remaining_mines -= 1
            else:
                cur_field.set_flag(False)
                self.remaining_mines += 1
            self.render_list.add(cur_field)

    def format_flag_num(self):
        return "{}".format(str(self.remaining_mines).rjust(self.mine_count_digit_len, "0"))

    def check_win(self):
        if (self.game_grid.field_amount - self.game_grid.mine_count) == len(self.open_fields):
            self.win = True

    def start_clock(self):
        self.start_time = time.time()

    def calc_time(self):
        cur_time = time.time()
        sum_time = int(cur_time - self.start_time)
        self.sum_time = sum_time
        minutes = sum_time // 60
        seconds = sum_time % 60
        minutes = "{}".format(str(minutes).rjust(2, "0"))
        seconds = "{}".format(str(seconds).rjust(2, "0"))
        self.current_time_str = "{}:{}".format(minutes, seconds)
        return self.current_time_str

    def format_cheat_num(self):
        if self.cheat_count < 10:
            return "{}".format(str(self.cheat_count).rjust(2, "0"))
        elif self.cheat_count >= 1000:
            return "too much"
        return "{} <.<\"".format(str(self.cheat_count).rjust(2, "0"))
