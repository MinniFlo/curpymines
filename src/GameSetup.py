import curses
import sys
import os

from WindowManager import WindowManager
from MineLogic import MinefieldLogic
from Context import Context


class GameSetup:

    def __init__(self, scr, args):
        self.scr = scr
        self.args = args
        self.y_size = 15
        self.x_size = 59
        self.y_pos, self.x_pos = 0, 0
        self.difficulty = 3
        self.difficulty_map = {1: 0.11, 2: 0.14, 3: 0.17, 4: 0.20, 5: 0.23}
        self.max_mine_digit = 2
        self.small = False
        self.fullscreen = False
        self.m_win = curses.newwin(self.y_size, self.x_size, self.y_pos, self.x_pos)
        self.s_win = curses.newwin(2, self.x_size, self.y_size, self.x_pos)
        self.p_win = curses.newwin(6, 13, self.y_pos, self.x_pos)
        self.o_win = curses.newwin(4, 16, self.y_pos, self.x_pos)
        self.d_win = curses.newwin(8, 13, self.y_pos, self.x_pos)
        self.v_win = curses.newwin(6, 14, (self.y_size // 2) - 4, (self.x_size // 2) - 6)
        self.logic = MinefieldLogic(self.y_size, self.x_size, self.difficulty_map[self.difficulty], self.max_mine_digit)
        self.context = Context(self.logic, (self.y_size, self.x_size), self.difficulty, self.difficulty_map,
                               self.fullscreen, self.small)

    def args_stuff(self):
        full_y, full_x = self.scr.getmaxyx()

        # sets the fullscreen
        if self.args.full_screen:
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
        if self.args.xaxis is not None:
            self.x_size = self.args.xaxis * 2 + 3
            if self.x_size > full_x:
                curses.endwin()
                os.system('echo terminal ist to small for the given x-value!')
                sys.exit()


        # sets the new y value
        if self.args.yaxis is not None:
            self.y_size = self.args.yaxis + 2
            if self.y_size + 1 > full_y:
                curses.endwin()
                os.system('echo terminal ist to small for the given y-value!')
                sys.exit()
            if self.x_size < 37:
                self.y_size = self.args.yaxis + 3
                if self.y_size + 1 > full_y:
                    curses.endwin()
                    os.system('echo terminal ist to small for the given y-value!')
                    sys.exit()

        # sets the difficulty
        if self.args.difficulty is not None:
            self.difficulty = self.args.difficulty

        # sets the flag for the alternative status window render
        if self.x_size < 37:
            self.small = True
            self.y_size -= 1

        # sets the padding for the "mines left: ..." in the status window
        self.max_mine_digit = len(str(int((((self.x_size // 2 + 1) * self.y_size) - 9) *
                                          self.difficulty_map[self.difficulty])))

        self.create_new_game()
        self.update_context()

    def update_context(self):
        self.context.update(self.logic, (self.y_size, self.x_size), self.difficulty, self.difficulty_map,
                            self.fullscreen, self.small)

    def create_manager(self):
        return WindowManager(self, self.context)

    def create_wins(self):
        self.m_win = curses.newwin(self.y_size, self.x_size, self.y_pos, self.x_pos)
        self.s_win = curses.newwin(2, self.x_size, self.y_size, self.x_pos)
        self.p_win = curses.newwin(6, 13, self.y_pos, self.x_pos)
        self.o_win = curses.newwin(4, 16, self.y_pos, self.x_pos)
        self.d_win = curses.newwin(8, 15, self.y_pos, self.x_pos)
        self.v_win = curses.newwin(6, 14, (self.y_size // 2) - 4, (self.x_size // 2) - 6)

    def create_new_game(self):
        self.create_wins()
        self.logic = MinefieldLogic(self.y_size, self.x_size, self.difficulty_map[self.difficulty], self.max_mine_digit)
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