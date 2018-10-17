from SuperWin import SuperWin
from OptionWin import OptionWin
import curses
import time


class PauseWin(SuperWin):

    def __init__(self, win, manager, context):
        self.win = win
        self.manager = manager
        self.context = context
        self.logic = self.context.logic
        self.menu_map = {0: self.resume, 1: self.restart, 2: self.options, 3: self.exit}
        self.menu_str_list = ["resume".ljust(7, ' ').center(9, ' '), "restart".center(9, ' '), "options".center(9, ' '),
                              "exit".ljust(7, ' ').center(9, ' ')]
        self.menu_index = 0
        self.option_win = OptionWin(self.manager.o_win, self.manager, self.context)

    def render(self):
        for i in range(4):
            if self.menu_index == i:
                self.win.addstr(i + 1, 2, self.menu_str_list[i], curses.A_REVERSE)
            else:
                self.win.addstr(i + 1, 2, self.menu_str_list[i])

        self.win.border(curses.ACS_VLINE, curses.ACS_VLINE, curses.ACS_HLINE, curses.ACS_HLINE,
                        curses.ACS_ULCORNER, curses.ACS_TTEE, curses.ACS_LTEE, curses.ACS_LRCORNER)

    def resume(self):
        self.manager.pop_win_stack()
        self.logic.start_time = time.time()
        self.logic.start_time -= self.logic.sum_time
        self.logic.sum_time = 0
        self.logic.pause = False

    def restart(self):
        self.manager.restart()

    def options(self):
        self.manager.push_win_stack(self.manager.o_win, self.option_win)

    def exit(self):
        self.manager.run_game = False

    def up_input(self):
        self.menu_index = (self.menu_index - 1) % 4

    def down_input(self):
        self.menu_index = (self.menu_index + 1) % 4

    def click_input(self):
        self.menu_map[self.menu_index]()

    def exit_input(self):
        self.resume()

    def flag_input(self):
        pass

    def reset_input(self):
        pass

    def left_input(self):
        pass

    def right_input(self):
        pass