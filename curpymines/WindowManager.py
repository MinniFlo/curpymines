from curpymines.MineWindow import MineWindow
from curpymines.StatusWindow import StatusWindow
import curses


class WindowManager:

    def __init__(self):
        self.m_win = curses.newwin(1, 1)
        self.mine_win = MineWindow(self.m_win)
        self.s_win = curses.newwin(2, 2)
        self.status_window = StatusWindow(self.s_win)

