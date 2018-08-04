#!/bin/python
import curses
import os
import argparse

from GameSetup import GameSetup


def main(stdscr):
    parser = argparse.ArgumentParser('does stuff')
    setuper = GameSetup(stdscr, parser)
    setuper.args_stuff()
    window_manager = setuper.create_manager()
    window_manager.setup()
    window_manager.render_all()
    # window_manager.render_threads()


def shorter_esc_delay():
    os.environ.setdefault('ESCDELAY', '25')


if __name__ == '__main__':
    shorter_esc_delay()
    curses.wrapper(main)
