import argparse
import curses

from WindowManager import WindowManager


class GameSetup:

    def __init__(self, scr, args):
        self.scr = scr
        self.difficulty = 0.17
        self.y_size = 15
        self.x_size = 59
        self.args = args
        self.difficulty_map = {1: 0.11, 2: 0.14, 3: 0.17, 4: 0.20, 5: 0.23}

    def args_stuff(self):
        if self.args.y_axis is not None:
            self.y_size = self.args.y_axis
        if self.args.x_axis is not None:
            self.x_size = self.args.x_axis
        if self.args.full_screen:
            self.y_size, self.x_size = self.scr.getmaxyx()
            self.y_size -= 1
            if self.x_size % 2 == 0:
                self.x_size -= 1
        if self.args.difficulty is not None:
            self.difficulty = self.difficulty_map[self.args.difficulty]

    def create_manager(self):
        return WindowManager(self.y_size, self.x_size, self.difficulty)
