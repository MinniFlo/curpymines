import random

from GameLogic.Field import Field


class GameGrid:

    def __init__(self, y_size, x_size):
        self.y_size = y_size
        self.x_size = x_size
        self.grid = []
        self.boarder = set()

        self.build_grid()

    def build_grid(self):
        for y in range(self.y_size):
            self.grid.append([])
            self._fill_grid_columns_and_boarder_set(y)

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

