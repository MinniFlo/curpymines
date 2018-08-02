import argparse

from WindowManager import WindowManager


class GameSetup:

    def __init__(self, scr):
        self.scr = scr
        self.y_size = 15
        self.x_size = 59
        self.parser = argparse.ArgumentParser('does stuff')
        self.parser.add_argument('--y_axis', '-y', type=int, help='size of y_axis')
        self.parser.add_argument('--x_axis', '-x', type=int, help='size of x_axis')
        self.args = self.parser.parse_args()

    def args_stuff(self):
        if self.args.y_axis is not None:
            self.y_size = self.args.y_axis
        if self.args.x_axis is not None:
            self.x_size = self.args.x_axis

    def create_manager(self):
        return WindowManager(self.scr, self.y_size, self.x_size)
