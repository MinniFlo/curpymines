from SuperWin import SuperWin
import curses


class PauseWin(SuperWin):

    def __init__(self, win, manager):
        self.win = win
        self.manager = manager
        self.logic = self.manager.logic
        self.menu_map = {0: self.resume, 1: self.restart, 2: self.options, 3: self.exit}
        self.menu_str_list = ["resume", "restart", "options", "exit"]
        self.menu_index = 0


    def render(self):
        for i in range(4):
            if self.menu_index == i:
                self.win.addstr(i+1, 2, self.menu_str_list[i], curses.A_REVERSE)
            else:
                self.win.addstr(i+1, 2, self.menu_str_list[i])
        self.win.box()

    def resume(self):
        self.manager.pop_win_stack()

    def restart(self):
        self.manager.restart()

    def options(self):
        pass

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