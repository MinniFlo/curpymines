import curses


class Colors:

    def __init__(self):
        curses.use_default_colors()
        # dark red
        curses.init_color(10, 600, 200, 300)
        # pink
        curses.init_color(11, 1000, 600, 750)
        # gray
        curses.init_color(12, 350, 350, 350)
        # orange
        curses.init_color(13, 900, 600, 400)
        # dark violet
        curses.init_color(14, 700, 0, 700)


        # number colors
        curses.init_pair(0, curses.COLOR_WHITE, -1)
        curses.init_pair(1, curses.COLOR_BLUE, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_RED, -1)
        curses.init_pair(4, curses.COLOR_CYAN, -1)
        curses.init_pair(5, curses.COLOR_MAGENTA, -1)
        curses.init_pair(6, 13, -1)
        curses.init_pair(7, 14, -1)
        curses.init_pair(8, 12, -1)

        # error colors
        curses.init_pair(9, -1, 10)
        curses.init_pair(10, 10, -1)

        # flag color
        curses.init_pair(11, 11, -1)

        # not relevant fields (low lighted)
        curses.init_pair(12, 12, -1)


