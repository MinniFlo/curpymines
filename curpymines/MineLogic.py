import random

from curpymines.Fields import Field


class MinefieldLogic:

    def __init__(self, max_y, max_x):
        self.max_y = max_y
        self.max_x = max_x
        self.field_amount = self.max_y * self.max_x
        self.max_mine = int(self.field_amount * 0.15)
        self.field_list = [i for i in range(self.field_amount)]
        self.field_matrix = []
        self.next_fields = set([])

    # The function witch fills the field_matrix with field-objects
    def build(self):

        for y in range(self.max_y):
            x_column = []
            self.field_matrix.append(x_column)
            for x in range(self.max_x):
                field = Field(y, x)
                x_column.append(field)

    def distribute_mines(self, st_y, st_x):
        mine_list = self.mine_list(st_y, st_x)
        for y in self.field_matrix:
            for x in y:
                pos_y, pos_x = x.get_foordinate()
                if mine_list and pos_y * self.max_x + pos_x == mine_list[0]:
                    x.set_mine(True)
                    mine_list.pop(0)

        for y in self.field_matrix:
            for x in y:
                if x.get_mine():
                    x.set_number(9)
                else:
                    cur_y, cur_x = x.get_foordinate()
                    mine_count = self.count_mines(cur_y, cur_x)
                    x.set_number(mine_count)

    # The function witch sets the position of the mines
    def mine_list(self, st_y, st_x):
        calc_list = set(self.field_list)
        no_mines = self.no_mines(st_y, st_x)
        help_mine_list = calc_list - no_mines
        help_mine_list = list(help_mine_list)
        mine_list = []
        for i in range(self.max_mine):
            rand = random.choice(help_mine_list)
            mine_list.append(rand)
            help_mine_list.remove(rand)
        mine_list.sort()
        return mine_list

    # The function witch calculates the rim of the field and the 9 fields where the start is
    def no_mines(self, st_y, st_x):
        rim_list = []
        for i in self.field_list:
            if i % self.max_x == 0 or (i + 1) % self.max_x == 0 or i < self.max_x or i > self.max_x * (self.max_y-1):
                rim_list.append(i)
        start = st_y * self.max_x + st_x
        start_fields = [start, start - 1, start + 1,
                        start + self.max_x, start + self.max_x + 1, start + self.max_x - 1,
                        start - self.max_x, start - self.max_x - 1, start - self.max_x + 1]
        rim_list = set(rim_list)
        start_fields = set(start_fields)
        no_mines = rim_list | start_fields
        return no_mines

    # Is called on click of a field
    def click_field(self, y, x):
        if not self.field_matrix[y][x].get_open():
            if self.field_matrix[y][x].get_mine():
                return False  # Todo!!1!11!
            self.check_field(y, x)
            self.check_next_fields()
        else:
            self.quality_of_life_click(y, x)

    # Checks the fields around the field that is called in click_field
    def check_field(self, y, x):
        cur_field = self.field_matrix[y][x]
        if cur_field.get_number() != 0:
            cur_field.set_open(True)
        else:
            adjacent_list = self.adjacent_fields(y, x)
            cur_field.set_open(True)
            for i in adjacent_list:
                i_field = self.tuple_in_matrix(i)
                if not i_field.get_open():
                    self.next_fields.add(i_field)

    def quality_of_life_click(self, y, x):
        if 0 < self.field_matrix[y][x].get_number() < 9:
            if self.count_flags(y, x) == self.field_matrix[y][x].get_number():
                adj_list = self.adjacent_fields(y, x)
                subs_list = set([])
                for i in adj_list:
                    i_field = self.tuple_in_matrix(i)
                    if i_field.get_flag() or i_field.get_open:
                        subs_list.add(i)
                adj_list = adj_list - subs_list
                for i in adj_list:
                    cur_y, cur_x = i
                    if self.field_matrix[cur_y][cur_x].get_mine:
                        return False  # Todo!!11!11!
                    else:
                        self.check_field(cur_y, cur_x)
                        self.check_next_fields()

    def check_next_fields(self):
        while self.next_fields:
            open_fields = set([])
            for i in self.next_fields:
                if i.get_open():
                    open_fields.add(i)
            self.next_fields = self.next_fields - open_fields
            if self.next_fields:
                i_field = self.next_fields.pop()
                y_i, x_i = i_field.get_foordinate()
                self.check_field(y_i, x_i)

    # The function returns a list of all tuples of fields that surround a specified field
    def adjacent_fields(self, y, x):
        adjacent_list = {(y, x+1), (y, x-1), (y+1, x), (y+1, x+1), (y+1, x-1), (y-1, x), (y-1, x+1), (y-1, x-1)}
        return set([x for x in adjacent_list if self.in_range(x)])

    # Maps a tuple of y and x to a field object from field_matrix
    def tuple_in_matrix(self, tupple):
        y, x = tupple
        return self.field_matrix[y][x]

    # Counts the mines around on field
    def count_mines(self, y, x):
        adj_list = self.adjacent_fields(y, x)
        mine_count = 0
        for i in adj_list:
            i_field = self.tuple_in_matrix(i)
            if i_field.get_mine():
                mine_count += 1
        return mine_count

    def count_flags(self, y, x):
        adj_list = self.adjacent_fields(y, x)
        flag_count = 0
        for i in adj_list:
            i_field = self.tuple_in_matrix(i)
            if i_field.get_flag():
                flag_count += 1
        return flag_count

    # logic that checks if field ist in the window
    def in_range(self, tupple):
        y, x = tupple
        return 0 <= y <= (self.max_y-1) and 0 <= x <= (self.max_x-1)


def main():
    st_y = 1
    st_x = 1
    logic = MinefieldLogic(6, 6)
    logic.build()

    print('\nopen:')
    for y in logic.field_matrix:
        print()
        for x in y:
            y_val, x_val = x.foordinate
            field = logic.field_matrix[y_val][x_val]
            if field.get_mine():
                print('+', end='\t')
            else:
                print(str(field.get_number()), end='\t')

    print('\n\nclosed:')
    for y in logic.field_matrix:
        print()
        for x in y:
            y_val, x_val = x.foordinate
            field = logic.field_matrix[y_val][x_val]
            if not field.get_open():
                print('?', end='\t')
            else:
                print(str(field.get_number()), end='\t')

    print("with mines:")
    logic.distribute_mines(st_y, st_x)
    logic.click_field(st_y, st_x)

    print('\nopen:')
    for y in logic.field_matrix:
        print()
        for x in y:
            y_val, x_val = x.foordinate
            field = logic.field_matrix[y_val][x_val]
            if field.get_mine():
                print('+', end='\t')
            else:
                print(str(field.get_number()), end='\t')

    print('\n\nclosed:')
    for y in logic.field_matrix:
        print()
        for x in y:
            y_val, x_val = x.foordinate
            field = logic.field_matrix[y_val][x_val]
            if not field.get_open():
                print('?', end='\t')
            else:
                print(str(field.get_number()), end='\t')


if __name__ == '__main__':
    main()
