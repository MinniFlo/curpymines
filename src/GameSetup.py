import curses
import sys
import os

from WindowManager import WindowManager
from GameLogic.GameLogic import GameLogic
from Context import Context


class GameSetup:

    def __init__(self, scr, args):
        self.scr = scr
        self.args = args
        self.y_size = 15
        self.x_size = 59
        self.y_value = None
        self.x_value = None
        self.y_pos, self.x_pos = 0, 0
        self.difficulty = 3
        self.small = False
        self.fullscreen = False
        self.m_win = curses.newwin(self.y_size, self.x_size, self.y_pos, self.x_pos)
        self.s_win = curses.newwin(2, self.x_size, self.y_size, self.x_pos)
        self.p_win = curses.newwin(6, 13, self.y_pos, self.x_pos)
        self.o_win = curses.newwin(5, 16, self.y_pos, self.x_pos)
        self.d_win = curses.newwin(8, 13, self.y_pos, self.x_pos)
        self.v_win = curses.newwin(6, 14, (self.y_size // 2) - 4, (self.x_size // 2) - 6)
        self.so_win = curses.newwin(6, 6, self.y_pos, self.x_pos)
        self.logic = GameLogic(self.y_size, self._calculate_x_size_for_logic(), self.difficulty)
        self.context = Context(self.logic, (self.y_value, self.x_value), self.difficulty,
                               self.fullscreen, self.small, (self.y_size, self.x_size))

    def game_setup(self, fullscreen=None, y_value=None, x_value=None, difficulty=None, restart=False):

        # set fullscreen flag
        if fullscreen is None:
            fullscreen = self.fullscreen

        # get available space of terminal window
        full_y, full_x = self.scr.getmaxyx()

        # sets the fullscreen
        if fullscreen and not restart:
            self.y_size = full_y - 1
            if full_x % 2 != 0:
                self.x_size = full_x
            else:
                self.x_size = full_x - 1
            self.fullscreen = True
            if full_y < 6 or full_x < 21:
                curses.endwin()
                os.system('echo terminal is to small')
                sys.exit()

        # sets the new x value
        if x_value is not None:
            self.x_value = x_value
            self.x_size = x_value * 2 + 3
            if self.x_size > full_x:
                curses.endwin()
                os.system('echo terminal ist to small for the given x-value!')
                sys.exit()

        # sets the new y value
        if y_value is not None:
            self.y_value = y_value
            # number of minefield rows plus 2 border rows
            self.y_size = y_value + 2
            # the y_size must also not be equal the full window size,
            # because there has to be space for the status menu
            # todo: wtf -------------------------
            if self.y_size >= full_y:
                curses.endwin()
                os.system('echo terminal ist to small for the given y-value!')
                sys.exit()
            # if the terminal is to small to display the status window
            if self.x_size < 37:
                # todo: why 2 and not 1
                self.y_size += 2
                if self.y_size >= full_y:
                    curses.endwin()
                    os.system('echo terminal ist to small for the given y-value!')
                    sys.exit()
            # todo: wtf -------------------------

        # sets the difficulty
        if difficulty is not None:
            self.difficulty = difficulty

        # sets the flag for the alternative status window render
        if self.x_size < 37 and not restart:
            self.small = True

        self.create_new_game()

    # todo: do not work with args but with the data of the context
    def process_args(self):
        self.game_setup(fullscreen=self.args.full_screen, y_value=self.args.height, x_value=self.args.width,
                        difficulty=self.args.difficulty, restart=False)

    def update_game(self):
        self.game_setup(fullscreen=self.context.fullscreen, difficulty=self.context.difficulty, restart=True)

    def update_context(self):
        self.context.update(self.logic, (self.y_size, self.x_size), self.difficulty,
                            self.fullscreen, self.small, (self.y_value, self.x_value))

    def create_manager(self):
        return WindowManager(self, self.context)

    def create_wins(self):
        self.m_win = curses.newwin(self.y_size, self.x_size, self.y_pos, self.x_pos)
        self.s_win = curses.newwin(2, self.x_size, self.y_size, self.x_pos)
        self.p_win = curses.newwin(6, 13, self.y_pos, self.x_pos)
        self.o_win = curses.newwin(5, 16, self.y_pos, self.x_pos)
        self.d_win = curses.newwin(8, 15, self.y_pos, self.x_pos)
        self.v_win = curses.newwin(6, 14, (self.y_size // 2) - 4, (self.x_size // 2) - 6)
        self.so_win = curses.newwin(6, 6, self.y_pos, self.x_pos)

    def create_new_game(self):
        self.create_wins()
        self.logic = GameLogic(self.y_size, self._calculate_x_size_for_logic(), self.difficulty)
        self.update_context()

    def curses_setup(self):
        curses.noecho()
        curses.curs_set(0)
        self.m_win.nodelay(True)
        self.m_win.keypad(True)
        self.p_win.keypad(True)
        self.o_win.keypad(True)
        self.d_win.keypad(True)
        self.v_win.keypad(True)
        self.so_win.keypad(True)

    def _calculate_x_size_for_logic(self):
        return self.x_size // 2 + 1
