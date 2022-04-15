

class Field:

    def __init__(self, y, x):
        self.y_pos = y
        self.x_pos = x
        self.render_x_pos = x * 2
        self.mine = False
        self.open = False
        self.flag = False
        self.number = 0

    def get_mine(self):
        return self.mine

    def get_open(self):
        return self.open

    def get_number(self):
        return self.number

    def get_coordinates(self):
        return self.y_pos, self.x_pos

    def get_render_coordinates(self):
        return self.y_pos, self.render_x_pos

    def get_flag(self):
        return self.flag

    def set_open(self, state_open):
        self.open = state_open

    def set_number(self, num):
        self.number = num

    def set_mine(self, is_mine):
        self.mine = is_mine

    def set_flag(self, is_marked):
        self.flag = is_marked




