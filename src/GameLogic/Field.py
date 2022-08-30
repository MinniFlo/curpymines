

class Field:

    def __init__(self, y, x):
        self.y_pos = y
        self.x_pos = x
        self.render_x_pos = x * 2
        self.mine = False
        self.open = False
        self.flag = False
        # is used to highlight Fields, that are relevant for further solving
        self.relevant = False
        self.number = 0
        self.current_symbol = '*'
        self.current_color_id = 12

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

    def get_relevant(self):
        return self.relevant

    def set_open(self, is_open):
        self.open = is_open
        if is_open:
            self.current_color_id = self.number
            if self.number == 0:
                self.current_symbol = ' '
            else:
                self.current_symbol = str(self.number)

    def set_number(self, num):
        self.number = num

    def set_mine(self, is_mine):
        self.mine = is_mine

    def set_flag(self, is_flagged):
        self.flag = is_flagged
        if is_flagged:
            self.current_symbol = '?'
            self.current_color_id = 11
            self.relevant = True
        else:
            self.current_symbol = '*'
            self.current_color_id = 0

    def set_relevant(self, is_relevant):
        if self.flag:
            return
        self.relevant = is_relevant
        if is_relevant and not self.open:
            self.current_color_id = 0
        elif is_relevant and self.open:
            self.current_color_id = self.number
        else:
            self.current_color_id = 12

    def get_current_symbol(self):
        return self.current_symbol

    def get_current_color_id(self):
        return self.current_color_id





