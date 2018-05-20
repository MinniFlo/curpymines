from curpymines.MineWindow import MineWindow
from curpymines.StatusWindow import StatusWindow
from curpymines.MineLogic import MinefieldLogic
import _thread
import curses


class WindowManager:

    def __init__(self):
        self.y_size = 15
        self.x_size = 59
        self.y_pos = 0
        self.x_pos = 0
        self.m_win = curses.newwin(self.y_size, self.x_size, self.y_pos, self.x_pos)
        self.s_win = curses.newwin(2, self.x_size, self.y_size, self.x_pos)
        self.logic = MinefieldLogic(self.y_size, self.x_size)
        self.mine_win = MineWindow(self.m_win, self.logic)
        self.status_window = StatusWindow(self.s_win, self.logic)

    '''
    def ms_win_setup(self, y, x, y_pos, x_pos):
        self.m_win = curses.newwin(y, x, y_pos, x_pos)
        self.s_win = curses.newwin(2, x, y_pos + y + 1, x_pos)
    '''
    def setup(self):
        curses.noecho()
        self.logic.build()
        self.mine_win.draw()
        self.m_win.keypad(True)

    def render_all(self):
        while self.mine_win.run:
            self.status_window.render()
            self.mine_win.user_input()
            self.mine_win.render()
