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
        if not self.game_grid.grid[y][x].get_flag():
            if not self.game_grid.grid[y][x].get_mine():
                self.check_field(y, x)
                self.check_next_fields()
            else:
                self.loose = True

    # Checks the fields around the field that is called in click_field and opens the field
    def check_field(self, y, x):
        cur_field = self.game_grid.grid[y][x]
        cur_field.set_open(True)
        self.render_list.add(cur_field)
        self.open_fields.add((y, x))
        if cur_field.get_number() == 0:
            adjacent_list = self.game_grid.neighbors_of_coordinates(y, x)
            for i in adjacent_list:
                i_field = self.game_grid.get_field_with_coordinates(i)
                if not i_field.get_open():
                    self.next_fields.add(i_field)

    def check_next_fields(self):
        while self.next_fields:
            none_matching_fields = set([])
            for i in self.next_fields:
                if i.get_open() or i.get_coordinates() in self.game_grid.boarder:
                    none_matching_fields.add(i)
            self.next_fields = self.next_fields - none_matching_fields
            if self.next_fields:
                i_field = self.next_fields.pop()
                y_i, x_i = i_field.get_coordinates()
                self.check_field(y_i, x_i)

    def quality_of_life_click(self, y, x):
        cur_field = self.game_grid.grid[y][x]
        if cur_field.get_number() != 0:
            if self.count_flags(y, x) == cur_field.get_number():
                work_list = self.game_grid.neighbors_of_coordinates(y, x)
                for i in set(work_list):
                    i_field = self.game_grid.get_field_with_coordinates(i)
                    if i_field.get_flag() or i_field.get_open():
                        work_list.remove(i)
                for i in work_list:
                    cur_y, cur_x = i
                    j_field = self.game_grid.get_field_with_coordinates(i)
                    if not j_field.get_mine():
                        self.check_field(cur_y, cur_x)
                        self.check_next_fields()
                    else:
                        self.loose = True

    def add_field_to_render_list(self, coordinates):
        field = self.game_grid.get_field_with_coordinates(coordinates)
        self.render_list.add(field)

    # The function returns a list of all tuples of fields that surround a specified field
    # def neighbors(self, y, x):
    #     adjacent_list = {(y, x+1), (y, x-1), (y+1, x), (y+1, x+1), (y+1, x-1), (y-1, x), (y-1, x+1), (y-1, x-1)}
    #     return {x for x in adjacent_list if x not in self.rim_list}
    # 
    # 
    # def get_field_with_coordinates(self, coordinates):
    #     y, x = coordinates
    #     return self.game_grid.grid[y][x]

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
