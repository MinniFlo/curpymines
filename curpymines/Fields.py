from curpymines.Colors import Colors


class Field:

    def __init__(self, y, x):
        self.foordinate = (y, x)
        self.mine = False
        self.open = False
        self.flag = False
        self.number = 0
        self.color = Colors()
        self.color_pair = None

    def get_mine(self):
        return self.mine

    def get_open(self):
        return self.open

    def get_number(self):
        return self.number

    def get_foordinate(self):
        return self.foordinate

    def get_flag(self):
        return self.flag

    def get_color(self):
        return self.color_pair

    def set_open(self, state_open):
        self.open = state_open

    def set_number(self, num):
        self.number = num
        self.set_color(num)

    def set_mine(self, is_mine):
        self.mine = is_mine

    def set_flag(self, is_marked):
        self.flag = is_marked

    def set_color(self, num):
        if num == 0:
            pass
        elif num == 1:
            self.color_pair = self.color.one_color
        elif num == 2:
            self.color_pair = self.color.two_color
        elif num == 3:
            self.color_pair = self.color.three_color
        elif num == 4:
            self.color_pair = self.color.four_color
        elif num == 5:
            self.color_pair = self.color.five_color
        elif num == 6:
            self.color_pair = self.color.six_color
        elif num == 7:
            self.color_pair = self.color.seven_color
        elif num == 8:
            self.color_pair = self.color.eight_color
        elif num == 9:
            self.color_pair = self.color.mine_color
        else:
            self.color_pair = self.color.seven_color

