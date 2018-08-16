from SuperWin import SuperWin
import curses


class VerificationsWin(SuperWin):

    def __init__(self, win, manager):
        self.win = win
        self.manager = manager
        self.menu_map = {0: self.yes, 1: self.no}
        self.menu_str_list = ["yes", "ney"]
        self.menu_index = 0
        self.line_str = "{}{}".format(chr(9500).ljust(13, chr(9472)), chr(9508))

    def render(self):
        self.win.addstr(1, 3, "restart")
        self.win.addstr(2, 3, "the game")

        if self.menu_index == 0:
            self.win.addstr(4, 3, self.menu_str_list[0], curses.A_REVERSE)
            self.win.addstr(4, 8, self.menu_str_list[1])
        else:
            self.win.addstr(4, 3, self.menu_str_list[0])
            self.win.addstr(4, 8, self.menu_str_list[1], curses.A_REVERSE)

        self.win.box()
        self.win.addstr(3, 0, self.line_str)

    def yes(self):
        self.manager.restart()

    def no(self):
        self.manager.pop_win_stack()

    def left_input(self):
        self.menu_index = (self.menu_index - 1) % 2

    def right_input(self):
        self.menu_index = (self.menu_index + 1) % 2

    def click_input(self):
        self.menu_map[self.menu_index]()

    def exit_input(self):
        self.no()

    def down_input(self):
        pass

    def flag_input(self):
        pass

    def reset_input(self):
        pass

    def up_input(self):
        pass
