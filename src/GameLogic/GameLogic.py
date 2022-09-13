import time

from GameLogic.GameGrid import GameGrid
from GameLogic.StatusData import StatusData


class GameLogic:

    def __init__(self, y_size, x_size, difficulty):
        self.difficulty_map = {1: 0.14, 2: 0.17, 3: 0.20, 4: 0.23, 5: 0.26}
        percentage_of_mines = self.difficulty_map[difficulty]

        self.game_grid = GameGrid(y_size, x_size, percentage_of_mines)
        self.statusData = StatusData(self.game_grid.mine_count)

        self.fields_to_open = set()
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
            self._check_field_for_mine_and_open_it(field)

    def click_open_field(self, y, x):
        field = self.game_grid.get_field_with_coordinates((y, x))
        if field.get_number() != 0:
            if self._flag_count(y, x) == field.get_number():
                self._open_closed_neighbors(x, y)

    def _open_closed_neighbors(self, x, y):
        neighbors = self.game_grid.neighbors_of_coordinates(y, x)
        for t in neighbors:
            field = self.game_grid.get_field_with_coordinates(t)
            if not field.get_open() and not field.get_flag():
                self._check_field_for_mine_and_open_it(field)

    def _check_field_for_mine_and_open_it(self, field):
        if not field.get_mine():
            self._open_field_and_check_neighbors(field)
            self._process_fields_to_open()
        else:
            self.loose = True

    def _flag_count(self, y, x):
        neighbors = self.game_grid.neighbors_of_coordinates(y, x)
        flags = 0
        for t in neighbors:
            field = self.game_grid.get_field_with_coordinates(t)
            if field.get_flag():
                flags += 1
        return flags
 
    def _open_field_and_check_neighbors(self, field):
        y, x = field.get_coordinates()
        field.set_open(True)
        self.open_fields.add((y, x))
        neighbors = self._add_field_and_neighbors_to_render_list(field)
        if field.get_number() == 0:
            self._add_closed_neighbors_to_fields_to_open(neighbors)

    def _add_closed_neighbors_to_fields_to_open(self, neighbors):
        for tup in neighbors:
            field = self.game_grid.get_field_with_coordinates(tup)
            if not field.get_open():
                self.fields_to_open.add(field)

    def _process_fields_to_open(self):
        while self.fields_to_open:
            i_field = self.fields_to_open.pop()
            self._open_field_and_check_neighbors(i_field)

    def add_field_to_render_list(self, coordinates):
        field = self.game_grid.get_field_with_coordinates(coordinates)
        self.render_list.add(field)

    def flag_field(self, y, x):
        field = self.game_grid.get_field_with_coordinates((y, x))
        if not field.get_open():
            if not field.get_flag():
                field.set_flag(True)
                self.statusData.remaining_mines -= 1
            else:
                field.set_flag(False)
                self.statusData.remaining_mines += 1
            self._add_field_and_neighbors_to_render_list(field)

    def _add_field_and_neighbors_to_render_list(self, field):
        self.render_list.add(field)
        y, x = field.get_coordinates()
        neighbors = self.game_grid.neighbors_of_coordinates(y, x)
        for tup in neighbors:
            tup_field = self.game_grid.get_field_with_coordinates(tup)
            self.render_list.add(tup_field)
        return neighbors

    def check_win(self):
        if (self.game_grid.field_count - self.game_grid.mine_count) == len(self.open_fields):
            self.win = True

    def update_last_game_state(self):
        self.game_grid.update_last_grid()
        # self.last_render_list = self.render_list

    def reset_to_last_game_state(self):
        self.game_grid.reset_to_last_grid()
        #  self.render_list = self.last_render_list
