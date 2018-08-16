from SuperWin import SuperWin
import curses


class DifficultyWin(SuperWin):

    def __init__(self, win, manager):
        self.win = win
        self.manager = manager
        self.menu_str_list = ["very easy".center(11, ' '), "easy".ljust(9, ' ').center(11, ' '),
                              "normal".ljust(9, ' ').center(11, ' '), "hard".ljust(9, ' ').center(11, ' '),
                              "insane".ljust(9, ' ').center(11, ' '), "back".ljust(9, ' ').center(11, ' ')]
        self.menu_index = 0

    def render(self):
        for i in range(6):
            if i == self.menu_index:
                self.win.addstr(i + 1, 2, self.menu_str_list[i], curses.A_REVERSE)
            else:
                self.win.addstr(i + 1, 2, self.menu_str_list[i])

            self.win.border(curses.ACS_VLINE, curses.ACS_VLINE, curses.ACS_HLINE, curses.ACS_HLINE,
                            curses.ACS_ULCORNER, curses.ACS_TTEE, curses.ACS_LTEE, curses.ACS_LRCORNER)

    def difficulty_change(self):
        return self.manager.game_setuper.difficulty_map[self.menu_index + 1]

    def back(self):
        self.manager.pop_win_stack()

    def up_input(self):
        self.menu_index = (self.menu_index - 1) % 6

    def down_input(self):
        self.menu_index = (self.menu_index + 1) % 6

    def click_input(self):
        if self.menu_index <= 4:
            self.manager.game_setuper.difficulty = self.difficulty_change()
        else:
            self.back()

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
