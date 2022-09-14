import time
from grid_n_fields import Grid, FieldContext as FC
from GameLogic.StatusData import StatusData


class GameLogic:

    def __init__(self, y_size, x_size, difficulty):
        self.difficulty_map = {1: 0.14, 2: 0.17, 3: 0.20, 4: 0.23, 5: 0.26}
        percentage_of_mines = self.difficulty_map[difficulty]

        self.game_grid = Grid(y_size, x_size, percentage_of_mines)
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

    def first_click(self, coordinates):
        self.statusData.start_time = time.time()
        self.game_grid.set_mine_data(coordinates)
        self.click_closed_field(coordinates)
        self.first = False

    # Is called on click of a field
    def click_closed_field(self, coordinates):
        with FC(self.game_grid, coordinates) as field:
            if not field.is_flag:
                self._check_field_for_mine_and_open_it(field)

    def click_open_field(self, coordinates):
        with FC(self.game_grid, coordinates) as field:
            if field.number != 0:
                if self._flag_count(coordinates) == field.number:
                    self._open_closed_neighbors(coordinates)

    def _open_closed_neighbors(self, coordinates):
        neighbors = self.game_grid.neighbors_of_coordinates(coordinates)
        for t in neighbors:
            with FC(self.game_grid, t) as field:
                if not field.is_open and not field.is_flag:
                    self._check_field_for_mine_and_open_it(field)

    def _check_field_for_mine_and_open_it(self, field):
        if not field.is_mine:
            self._open_field_and_check_neighbors(field)
            self._process_fields_to_open()
        else:
            self.loose = True

    def _flag_count(self, coordinates):
        neighbors = self.game_grid.neighbors_of_coordinates(coordinates)
        flags = 0
        for t in neighbors:
            with FC(self.game_grid, t) as field:
                if field.is_flag:
                    flags += 1
        return flags
 
    def _open_field_and_check_neighbors(self, field):
        coordinates = field.coordinates
        field.is_open = True
        self.open_fields.add(coordinates)
        neighbors = self._add_field_and_neighbors_to_render_list(coordinates)
        if field.number == 0:
            self._add_closed_neighbors_to_fields_to_open(neighbors)

    def _add_closed_neighbors_to_fields_to_open(self, neighbors):
        for t in neighbors:
            with FC(self.game_grid, t) as field:
                if not field.is_open:
                    self.fields_to_open.add(t)

    def _process_fields_to_open(self):
        while self.fields_to_open:
            coordinates = self.fields_to_open.pop()
            with FC(self.game_grid, coordinates) as field:
                self._open_field_and_check_neighbors(field)

    def flag_field(self, coordinates):
        with FC(self.game_grid, coordinates) as field:
            if not field.is_open:
                if not field.is_flag:
                    field.is_flag = True
                    self.statusData.remaining_mines -= 1
                else:
                    field.is_flag = False
                    self.statusData.remaining_mines += 1
                self._add_field_and_neighbors_to_render_list(coordinates)

    def _add_field_and_neighbors_to_render_list(self, coordinates):
        self.render_list.add(coordinates)
        neighbors = self.game_grid.neighbors_of_coordinates(coordinates)
        self.render_list = self.render_list | neighbors
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
