import curses


class Colors:

    def __init__(self):
        curses.use_default_colors()

        curses.init_color(10, 600, 200, 300)
        curses.init_color(12, 350, 350, 350)
        curses.init_color(13, 1000, 600, 750)


        # number colors
        curses.init_pair(1, curses.COLOR_BLUE, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_RED, -1)
        curses.init_pair(4, curses.COLOR_CYAN, -1)
        curses.init_pair(5, curses.COLOR_MAGENTA, -1)
        curses.init_pair(6, 13, -1)

        # other
        curses.init_pair(7, curses.COLOR_WHITE, -1)
        curses.init_pair(8, curses.COLOR_WHITE, -1)

        # error colors
        curses.init_pair(9, curses.COLOR_BLACK, 10)
        curses.init_pair(10, 10, -1)

        # not relevant fields
        curses.init_pair(12, 12, -1)


