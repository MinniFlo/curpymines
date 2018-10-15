import curses


class Colors:

    def __init__(self):
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLUE, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_RED, -1)
        curses.init_pair(4, curses.COLOR_CYAN, -1)
        curses.init_pair(5, curses.COLOR_MAGENTA, -1)
        curses.init_pair(6, curses.COLOR_YELLOW, -1)
        curses.init_pair(7, curses.COLOR_WHITE, -1)
        curses.init_pair(8, curses.COLOR_WHITE, -1)
        curses.init_pair(9, -1, curses.COLOR_RED)
        curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(11, curses.COLOR_YELLOW, curses.COLOR_RED)

