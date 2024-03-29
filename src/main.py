#!/bin/python
import curses
import os
import argparse
from functools import partial
from GameSetup import GameSetup


def main(args, stdscr):
    setuper = GameSetup(stdscr, args)
    setuper.process_args()
    setuper.curses_setup()
    window_manager = setuper.create_manager()
    window_manager.game_setup()
    window_manager.render_all()


def shorter_esc_delay():
    os.environ.setdefault('ESCDELAY', '25')


if __name__ == '__main__':
    shorter_esc_delay()

    parser = argparse.ArgumentParser(prog='tool',
                                     formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50))
    parser.add_argument("-y", "--height", type=int, help="size of y_axis", metavar="[7-204]",
                        choices=range(7, 205))
    parser.add_argument("-x", "--width", type=int, help="size of x_axis", metavar="[10-477]", choices=range(10, 478))
    parser.add_argument("-f", "--full_screen", action="store_true", help="uses full height/width of terminal")
    parser.add_argument("-d", "--difficulty", type=int, help="set difficulty", metavar="[1-5]", choices=range(1, 6))
    args = parser.parse_args()

    curses.wrapper(partial(main, args))
