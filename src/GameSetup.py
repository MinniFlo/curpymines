import argparse
import curses
import sys
import os

from WindowManager import WindowManager


class GameSetup:

    def __init__(self, scr, args):
        self.scr = scr
        self.args = args
        self.y_size = 15
        self.x_size = 59
        self.difficulty = 0.17
        self.difficulty_map = {1: 0.11, 2: 0.14, 3: 0.17, 4: 0.20, 5: 0.23}
        self.max_mine_digit = 2
        self.small = False


    def args_stuff(self):
        full_y, full_x = self.scr.getmaxyx()

        # sets the fullscreen
        if self.args.full_screen:
            self.y_size = full_y - 1
            if full_x % 2 != 0:
                self.x_size = full_x
            else:
                self.x_size = full_x - 1
            if full_y < 6 or full_x < 21:
                os.system('echo test')
                sys.exit()

        # sets the new x value
        if self.args.x_axis is not None:
            self.x_size = self.args.x_axis * 2 + 3
            if self.x_size > full_x:
                os.system('echo test')
                sys.exit()

        # sets the new y value
        if self.args.y_axis is not None:
            self.y_size = self.args.y_axis + 2
            if self.y_size + 1 > full_y:
                os.system('echo test')
                sys.exit()
            if self.x_size < 37:
                self.y_size = self.args.y_axis + 3
                if self.y_size + 1 > full_y:
                    os.system('echo test')
                    sys.exit()

        # sets the difficulty
        if self.args.difficulty is not None:
            self.difficulty = self.difficulty_map[self.args.difficulty]

        # sets the flag for the alternative status window render
        if self.x_size < 37:
            self.small = True
            self.y_size -= 1

        # sets the padding for the "mines left: ..." in the status window
        self.max_mine_digit = len(str(int(((self.x_size // 2 + 1) * self.y_size - 9) * self.difficulty)))


    def create_manager(self):
        return WindowManager(self.y_size, self.x_size, self.difficulty, self.max_mine_digit, self.small)
