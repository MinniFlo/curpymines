import time

from GameLogic.GameGrid import GameGrid
from GameLogic.StatusData import StatusData


class GameLogic:

    def __init__(self, y_size, x_size, difficulty):
        self.difficulty_map = {1: 0.14, 2: 0.17, 3: 0.20, 4: 0.23, 5: 0.26}
        percentage_of_mines = self.difficulty_map[difficulty]

        self.game_grid = GameGrid(y_size, x_size, percentage_of_mines)
        self.statusData = StatusData(self.game_grid.mine_count)

        self.next_fields = set()
        self.render_list = set()
        # self.last_render_list = set()
        self.open_fields = set()

        # game state
        self.first = True
        self.loose = False
        self.win = False
        self.cheat = False
        self.pause = False

    def first_click(self, y, x):
        self.statusData.start_time = time.time()
        self.game_grid.set_mines_data(y, x)
        self.click_closed_field(y, x)
        self.first = False

    # Is called on click of a field
    def click_closed_field(self, y, x):
        field = self.game_grid.get_field_with_coordinates((y, x))
        if not field.get_flag():
            if not field.get_mine():
                self.check_field(field)
                self.check_next_fields()
            else:
                self.loose = True

    def click_open_field(self, y, x):
        cur_field = self.game_grid.grid[y][x]
        if cur_field.get_number() != 0:
            if self._flag_count(y, x) == cur_field.get_number():
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

    def _flag_count(self, y, x):
        adj_list = self.game_grid.neighbors_of_coordinates(y, x)
        flags = 0
        for i in adj_list:
            i_field = self.game_grid.get_field_with_coordinates(i)
            if i_field.get_flag():
                flags += 1
        return flags

    # Checks the fields around the field that is called in click_field and opens the field
    def check_field(self, field):
        y, x = field.get_coordinates()
        field.set_open(True)
        self.open_fields.add((y, x))
        self.render_list.add(field)
        neighbors = self.game_grid.neighbors_of_coordinates(y, x)
        if field.get_number() == 0:
            for tup in neighbors:
                tup_field = self.game_grid.get_field_with_coordinates(tup)
                if not tup_field.get_open():
                    self.next_fields.add(tup_field)
        else:
            for tup in neighbors:
                tup_field = self.game_grid.get_field_with_coordinates(tup)
                self.render_list.add(tup_field)

    def check_next_fields(self):
        while self.next_fields:
            i_field = self.next_fields.pop()
            self.check_field(i_field)

    def add_field_to_render_list(self, coordinates):
        field = self.game_grid.get_field_with_coordinates(coordinates)
        self.render_list.add(field)

    def flag_field(self, y, x):
        cur_field = self.game_grid.grid[y][x]
        if not cur_field.get_open():
            if not cur_field.get_flag():
                cur_field.set_flag(True)
                self.statusData.remaining_mines -= 1
            else:
                cur_field.set_flag(False)
                self.statusData.remaining_mines += 1
            self.render_list.add(cur_field)
        # put all neighbor fields in the render_list for the highlight-color-feature
        neighbors = self.game_grid.neighbors_of_coordinates(y, x)
        for tup in neighbors:
            tup_field = self.game_grid.get_field_with_coordinates(tup)
            self.render_list.add(tup_field)

    def check_win(self):
        if (self.game_grid.field_amount - self.game_grid.mine_count) == len(self.open_fields):
            self.win = True

    def update_last_game_state(self):
        self.game_grid.update_last_grid()
        # self.last_render_list = self.render_list

    def reset_to_last_game_state(self):
        self.game_grid.reset_to_last_grid()
        #  self.render_list = self.last_render_list
