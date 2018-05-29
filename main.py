
import curses
import os
from curpymines import WindowManager


def main(stdscr):
    window_manager = WindowManager.WindowManager()
    window_manager.setup()
    window_manager.render_all()
    # window_manager.render_threads()


def shorter_esc_delay():
    os.environ.setdefault('ESCDELAY', '25')


if __name__ == '__main__':
    shorter_esc_delay()
    curses.wrapper(main)
