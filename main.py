
import curses

from curpymines import MineWindow


def main(stdscr):

    mine_field = MineWindow.MineWindow(stdscr)
    mine_field.while_running()


if __name__ == '__main__':
    curses.wrapper(main)
