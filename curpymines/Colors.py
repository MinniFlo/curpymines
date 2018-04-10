import curses


class Colors:

    def __init__(self):
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
        self.one_color = curses.color_pair(1)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.two_color = curses.color_pair(2)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        self.three_color = curses.color_pair(3)
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
        self.four_color = curses.color_pair(4)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        self.five_color = curses.color_pair(5)
        curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        self.six_color = curses.color_pair(6)
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.seven_color = curses.color_pair(7)
        curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.eight_color = curses.color_pair(8)
        curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_RED)
        self.mine_color = curses.color_pair(9)