import argparse
import curses

from WindowManager import WindowManager


class GameSetup:

    def __init__(self, scr, parser):
        self.scr = scr
        self.y_size = 15
        self.x_size = 59
        self.parser = parser
        self.parser.add_argument('--y-axis', '-y', type=int, help='size of y_axis')
        self.parser.add_argument('--x-axis', '-x', type=int, help='size of x_axis')
        self.parser.add_argument('--full_screen', '-f', action='store_true', help='uses full higth/width of terminal')
        self.args = self.parser.parse_args()

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

    def create_manager(self):
        return WindowManager(self.y_size, self.x_size)
