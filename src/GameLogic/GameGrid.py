import random

from GameLogic.Field import Field


class GameGrid:

    def __init__(self, y_size, x_size, percentage_of_mines):
        self.y_size = y_size
        self.x_size = x_size
        self.grid = []
        self.boarder = set()

        self.build_grid()

        self.field_amount = (y_size * x_size) - len(self.boarder)
        self.mine_count = int((self.field_amount - 9) * percentage_of_mines)

        self.last_grid = []

    def build_grid(self):
        for y in range(self.y_size):
            self.grid.append([])
            self._fill_grid_columns_and_boarder_set(y)
            
    def set_mines_data(self, start_y, start_x):
        self._set_mines(start_y, start_x)
        self._set_numbers()
            
    def neighbors_of_coordinates(self, y, x):
        adjacent_coordinates = {(y, x+1), (y, x-1), (y+1, x), (y+1, x+1), (y+1, x-1), (y-1, x), (y-1, x+1), (y-1, x-1)}
        return {t for t in adjacent_coordinates if t not in self.boarder}

    def get_field_with_coordinates(self, coordinates):
        y, x = coordinates
        return self.grid[y][x]

    def update_last_grid(self):
        self.last_grid = self.grid

    def reset_to_last_grid(self):
        self.grid = self.last_grid

    def _fill_grid_columns_and_boarder_set(self, y):
        for x in range(self.x_size):
            self._fill_grid_with_fields(y, x)
            self._fill_boarder_with_tuples(y, x)

    def _fill_grid_with_fields(self, y, x):
        field = Field(y, x)
        self.grid[y].append(field)

    def _fill_boarder_with_tuples(self, y, x):
        if self._tuple_is_in_boarder(y, x):
            self.boarder.add((y, x))

    def _tuple_is_in_boarder(self, y, x):
        return y == 0 or y == (self.y_size - 1) or x == 0 or x == (self.x_size - 1)

    def _set_mines(self, start_y, start_x):
        mine_list = self._get_mine_positions_list(start_y, start_x)
        self._set_mine_value_in_corresponding_fields(mine_list)

    def _set_numbers(self):
        for row in self.grid:
            for field in row:
                field_coordinates = field.get_coordinates()
                if field_coordinates in self.boarder or field.get_mine():
                    continue
                else:
                    self._set_field_number(field)

    def _set_field_number(self, field):
        mine_count = self._count_mines_around_field(field)
        field.set_number(mine_count)

    def _count_mines_around_field(self, field):
        y, x = field.get_coordinates()
        neighbors = self.neighbors_of_coordinates(y, x)
        mine_count = self._mine_count_in_neighbors(neighbors)
        return mine_count

    def _mine_count_in_neighbors(self, neighbors):
        mine_count = 0
        for position in neighbors:
            field = self.get_field_with_coordinates(position)
            if field.get_mine():
                mine_count += 1
        return mine_count

    def _set_mine_value_in_corresponding_fields(self, mine_list):
        for rows in self.grid:
            for field in rows:
                if field.get_coordinates() in mine_list:
                    field.set_mine(True)
                    field.set_number(9)

    # The function witch sets the position of the mines
    def _get_mine_positions_list(self, start_y, start_x):
        possible_mine_positions = self._get_possible_mine_positions(start_y, start_x)
        mine_position = self._get_random_mine_positions(possible_mine_positions)
        return mine_position

    def _get_possible_mine_positions(self, start_y, start_x):
        grid_fields = self._get_grid_coordinates_without_boarder()
        start_fields = self._get_start_space_coordinates(start_y, start_x)
        return list(grid_fields - start_fields)

    def _get_grid_coordinates_without_boarder(self):
        all_fields = set([])
        for row in self.grid:
            for field in row:
                all_fields.add(field.get_coordinates())
        return all_fields - self.boarder

    @staticmethod
    def _get_start_space_coordinates(st_y, st_x):
        start_fields = {(st_y, st_x), (st_y + 1, st_x), (st_y - 1, st_x), (st_y, st_x + 1), (st_y, st_x - 1),
                        (st_y + 1, st_x + 1), (st_y + 1, st_x - 1), (st_y - 1, st_x + 1), (st_y - 1, st_x - 1)}
        return start_fields

    def _get_random_mine_positions(self, possible_mine_positions):
        mine_positions = set([])
        for _ in range(self.mine_count):
            self._randomly_choose_mines(possible_mine_positions, mine_positions)
        return mine_positions

    @staticmethod
    def _randomly_choose_mines(possible_mine_positions, mine_positions):
        choice = random.choice(possible_mine_positions)
        mine_positions.add(choice)
        possible_mine_positions.remove(choice)
