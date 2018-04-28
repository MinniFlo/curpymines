from curpymines.MineWindow import MineWindow
import curses


class WindowManager:

    def __init__(self):
        m_win = curses.newwin(1, 1)
        self.mine_win = MineWindow(m_win)

