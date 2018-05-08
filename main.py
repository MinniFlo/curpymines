
import curses

from curpymines import MineWindow
from curpymines import WindowManager


def main(stdscr):
    # mine_field = MineWindow.MineWindow(stdscr)
    # mine_field.while_running()
    window_manager = WindowManager.WindowManager()
    window_manager.setup()
    window_manager.render_all()


if __name__ == '__main__':
    curses.wrapper(main)
