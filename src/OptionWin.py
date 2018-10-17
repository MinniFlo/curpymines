from SuperWin import SuperWin
from DifficultyWin import DifficultyWin
import curses


class OptionWin(SuperWin):

    def __init__(self, win, manager, context):
        self.win = win
        self.manager = manager
        self.context = context
        self.menu_map = {0: self.difficulty, 1: self.back}
        self.menu_str_list = ["difficulty".center(12, ' '), "back".ljust(10, ' ').center(12, ' ')]
        self.menu_index = 0
        self.difficulty_win = DifficultyWin(manager.d_win, manager, self.context)

    def render(self):
        for i in range(2):
            if i == self.menu_index:
                self.win.addstr(i + 1, 2, self.menu_str_list[i], curses.A_REVERSE)
            else:
                self.win.addstr(i + 1, 2, self.menu_str_list[i])

            self.win.border(curses.ACS_VLINE, curses.ACS_VLINE, curses.ACS_HLINE, curses.ACS_HLINE,
                            curses.ACS_ULCORNER, curses.ACS_TTEE, curses.ACS_LTEE, curses.ACS_LRCORNER)

    def difficulty(self):
        self.manager.push_win_stack(self.manager.d_win, self.difficulty_win)

    def back(self):
        self.manager.pop_win_stack()

    def up_input(self):
        self.menu_index = (self.menu_index - 1) % 2

    def down_input(self):
        self.menu_index = (self.menu_index + 1) % 2

    def click_input(self):
        self.menu_map[self.menu_index]()

    def exit_input(self):
        self.back()


    def flag_input(self):
        pass

    def reset_input(self):
        pass

    def left_input(self):
        pass

    def right_input(self):
        pass

