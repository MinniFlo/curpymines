#!/bin/python
import curses
import os

from WindowManager import WindowManager


def main(stdscr):
    window_manager = WindowManager(stdscr)
    window_manager.setup()
    window_manager.render_all()
    # window_manager.render_threads()


def shorter_esc_delay():
    os.environ.setdefault('ESCDELAY', '25')


if __name__ == '__main__':
    shorter_esc_delay()
    curses.wrapper(main)
