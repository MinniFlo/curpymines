import argparse
import curses

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
        # sets the fullscreen
        if self.args.full_screen:
            self.y_size, self.x_size = self.scr.getmaxyx()
            self.y_size -= 1
            if self.x_size % 2 == 0:
                self.x_size -= 1

        # sets the new x value
        if self.args.x_axis is not None:
            self.x_size = self.args.x_axis * 2 + 3

        # sets the new y value
        if self.args.y_axis is not None:
            self.y_size = self.args.y_axis + 2
            if self.x_size < 37:
                self.y_size = self.args.y_axis + 3

        # sets the difficulty
        if self.args.difficulty is not None:
            self.difficulty = self.difficulty_map[self.args.difficulty]

        # sets the flag for the alternative status window render
        if self.x_size < 37:
            self.small = True
            self.y_size -= 1

        # sets the padding for the "mines left: ..." in the status window
        self.max_mine_digit = len(str(int(((self.x_size // 2 + 1)* self.y_size - 9) * self.difficulty)))

    def create_manager(self):
        return WindowManager(self.y_size, self.x_size, self.difficulty, self.max_mine_digit, self.small)
