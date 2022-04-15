import random
import time

from src.Fields import Field


class GameLogic:

    def __init__(self, max_y, max_x, difficulty, max_mine_digit):
        self.max_y = max_y
        self.max_x = max_x
        self.x_fields = self.max_x // 2 + 1
        self.field_amount = self.x_fields * max_y
        self.mine_percent = difficulty
        self.max_mine = int((self.field_amount - 9) * self.mine_percent)
        self.rim_list = set([])
        self.field_matrix = []
        self.previous_matrix = []
        self.next_fields = set([])
        self.render_list = set([])
        self.win_list = set()
        self.first = True
        self.loose = False
        self.win = False
        self.cheat = False
        self.pause = False
        self.flag_count = self.max_mine
        self.start_time = 0
        self.sum_time = 0
        self.current_time_str = ""
        self.cheat_count = 0
        self.max_mine_digit = max_mine_digit

    # The function witch fills the field_matrix with field-objects
    # setup >>>>>
    def setup(self):
        self.loose = False
        self._create_game_grit()

    def _create_game_grit(self):
        for y in range(self.max_y):
            self.field_matrix.append([])
            self._fill_matrix_columns_and_rim_set(y)

    def _fill_matrix_columns_and_rim_set(self, y):
        for x in range(self.x_fields):
            offset_x = x * 2
            self._fill_field_matrix(y, offset_x)
            self._fill_rim_list(y, offset_x)

    def _fill_field_matrix(self, y, x):
        field = Field(y, x)
        self.field_matrix[y].append(field)

    def _fill_rim_list(self, y, x):
        if self._tuple_is_boarder(y, x):
            self.rim_list.add((y, x))

    def _tuple_is_boarder(self, y, x):
        return y == 0 or y == (self.max_y - 1) or x == 0 or x == (self.max_x - 1)
    # <<<<< setup

    def distribute_mines(self, st_y, st_x):
        self.start_time = time.time()
        mine_list = self.mine_list(st_y, st_x)
        # sets mines
        for y in self.field_matrix:
            for x in y:
                cur_tuple = x.get_foordinate()
                if mine_list and cur_tuple in mine_list:
                    x.set_mine(True)
        # sets numbers
        for y in self.field_matrix:
            for x in y:
                if x.get_mine():
                    x.set_number(9)
                else:
                    cur_y, cur_x = x.get_foordinate()
                    mine_count = self.count_mines(cur_y, cur_x)
                    x.set_number(mine_count)
        self.first = False

    # The function witch sets the position of the mines
    def mine_list(self, st_y, st_x):
        calc_list = set([])
        for y in self.field_matrix:
            for x in y:
                cur_tuple = x.get_foordinate()
                calc_list.add(cur_tuple)
        no_mines = self.no_mines(st_y, st_x)
        help_mine_list = calc_list - no_mines
        help_mine_list = list(help_mine_list)
        mine_list = set([])
        for i in range(self.max_mine):
            rand = random.choice(help_mine_list)
            mine_list.add(rand)
            help_mine_list.remove(rand)
        return mine_list

    # The function witch calculates the rim of the field and the 9 fields where the start is
    def no_mines(self, st_y, st_x):
        start_fields = {(st_y, st_x), (st_y + 1, st_x), (st_y - 1, st_x), (st_y, st_x + 2), (st_y, st_x - 2),
                        (st_y + 1, st_x + 2), (st_y + 1, st_x - 2), (st_y - 1, st_x + 2), (st_y - 1, st_x - 2)}
        no_mines = self.rim_list | start_fields
        return no_mines

    # Is called on click of a field
    def click_field(self, y, x):
        x_index = x // 2
        if not self.field_matrix[y][x_index].get_flag():
            if not self.field_matrix[y][x_index].get_mine():
                self.check_field(y, x)
                self.check_next_fields()
            else:
                self.loose = True

    # Checks the fields around the field that is called in click_field and opens the field
    def check_field(self, y, x):
        x_index = x // 2
        cur_field = self.field_matrix[y][x_index]
        if cur_field.get_number() != 0:
            cur_field.set_open(True)
            self.render_list.add(cur_field)
            self.win_list.add(cur_field)
        else:
            adjacent_list = self.neighbors(y, x)
            cur_field.set_open(True)
            self.render_list.add(cur_field)
            self.win_list.add(cur_field)
            for i in adjacent_list:
                i_field = self.tuple_in_matrix(i)
                if not i_field.get_open():
                    self.next_fields.add(i_field)

    def check_next_fields(self):
        while self.next_fields:
            none_matching_fields = set([])
            for i in self.next_fields:
                if i.get_open() or i.get_foordinate() in self.rim_list:
                    none_matching_fields.add(i)
            self.next_fields = self.next_fields - none_matching_fields
            if self.next_fields:
                i_field = self.next_fields.pop()
                y_i, x_i = i_field.get_foordinate()
                self.check_field(y_i, x_i)

    def quality_of_life_click(self, y, x):
        x_index = x // 2
        cur_field = self.field_matrix[y][x_index]
        if cur_field.get_number() != 0:
            if self.count_flags(y, x) == cur_field.get_number():
                work_list = self.neighbors(y, x)
                for i in set(work_list):
                    i_field = self.tuple_in_matrix(i)
                    if i_field.get_flag() or i_field.get_open():
                        work_list.remove(i)
                for i in work_list:
                    cur_y, cur_x = i
                    j_field = self.tuple_in_matrix(i)
                    if not j_field.get_mine():
                        self.check_field(cur_y, cur_x)
                        self.check_next_fields()
                    else:
                        self.loose = True

    # The function returns a list of all tuples of fields that surround a specified field
    def neighbors(self, y, x):
        adjacent_list = {(y, x+2), (y, x-2), (y+1, x), (y+1, x+2), (y+1, x-2), (y-1, x), (y-1, x+2), (y-1, x-2)}
        return {x for x in adjacent_list if self.in_range(x)}

    # Maps a tuple of y and x to a field object from field_matrix
    def tuple_in_matrix(self, tup):
        y, x = tup
        x = x // 2
        return self.field_matrix[y][x]

    # Counts the mines around on field
    def count_mines(self, y, x):
        adj_list = self.neighbors(y, x)
        mine_count = 0
        for i in adj_list:
            i_field = self.tuple_in_matrix(i)
            if i_field.get_mine():
                mine_count += 1
        return mine_count

    def count_flags(self, y, x):
        adj_list = self.neighbors(y, x)
        flags = 0
        for i in adj_list:
            i_field = self.tuple_in_matrix(i)
            if i_field.get_flag():
                flags += 1
        return flags

    def flag_field(self, y, x):
        cur_field = self.field_matrix[y][x]
        if not cur_field.get_open():
            if not cur_field.get_flag():
                cur_field.set_flag(True)
                self.flag_count -= 1
            else:
                cur_field.set_flag(False)
                self.flag_count += 1
            self.render_list.add(cur_field)

    def format_flag_num(self):
        return "{}".format(str(self.flag_count).rjust(self.max_mine_digit, "0"))

    def check_win(self):
        if (self.field_amount - len(self.rim_list) - self.max_mine) == len(self.win_list):
            self.win = True

    # logic that checks if field ist in the window
    def in_range(self, tupple):
        y, x = tupple
        return 1 <= y <= (self.max_y-2) and 2 <= x <= (self.max_x-3)

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
        if self.cheat_count < 100:
            return "{}".format(str(self.cheat_count).rjust(2, "0"))
        return "> 9000"


