from SuperWin import SuperWin
import curses
from VerificationsWin import VerificationsWin


class SizeWin(SuperWin):

    def __init__(self, win, manager, context):
        self.win = win
        self.manager = manager
        self.context = context
        self.y_Val = None
        self.x_Val = None
        self.logic = self.context.logic
        self.menu_str_list = []
        self.menu_index = 0
        self.verifications_win = VerificationsWin(manager.v_win, manager)

    def render(self):
        self.back()

    def back(self):
        self.manager.pop_win_stack()

    def up_input(self):
        pass

    def left_input(self):
        pass

    def right_input(self):
        pass

    def down_input(self):
        pass

    def click_input(self):
        pass

    def flag_input(self):
        pass

    def reset_input(self):
        pass

    def exit_input(self):
        self.back()