#!/bin/python
import curses
import os
import argparse

from GameSetup import GameSetup


def main(stdscr):
    parser = argparse.ArgumentParser('does stuff')
    parser.add_argument('-y', '--y-axis', type=int, help='size of y_axis', choices=list(range(2, 205)))
    parser.add_argument('-x', '--x-axis', type=int, help='size of x_axis', choices=list(range(10, 478)))
    parser.add_argument('-f', '--full_screen', action='store_true', help='uses full higth/width of terminal')
    parser.add_argument('-d', '--difficulty', type=int, help='set difficulty', choices=list(range(1, 6)))
    args = parser.parse_args()
    setuper = GameSetup(stdscr, args)
    setuper.args_stuff()
    window_manager = setuper.create_manager()
    window_manager.setup()
    window_manager.render_all()


def shorter_esc_delay():
    os.environ.setdefault('ESCDELAY', '25')


if __name__ == '__main__':
    shorter_esc_delay()
    curses.wrapper(main)
