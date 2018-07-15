from curpymines.MineWindow import MineWindow
from curpymines.StatusWindow import StatusWindow
from curpymines.MineLogic import MinefieldLogic
import time
import curses
from curpymines.SuperWin import SuperWin


class WindowManager:

    def __init__(self):
        self.y_size = 15
        self.x_size = 59
        self.y_pos = 0
        self.x_pos = 0
        self.m_win = curses.newwin(self.y_size, self.x_size, self.y_pos, self.x_pos)
        self.s_win = curses.newwin(2, self.x_size, self.y_size, self.x_pos, )
        self.logic = MinefieldLogic(self.y_size, self.x_size)
        self.mine_win = MineWindow(self.m_win, self.logic)
        self.status_win = StatusWindow(self.s_win, self.logic)
        self.win_stack = []
        self.active_win = None
        self.active_win_obj = None
        self.input_map = {(119, 107, 259): SuperWin.up_input, (97, 104, 260): SuperWin.left_input,
                          (100, 108, 261): SuperWin.right_input, (115, 106, 258): SuperWin.down_input,
                          (32, 10): SuperWin.click_input, (101, 102): SuperWin.flag_input,
                          (114, 111): SuperWin.reset_input, (27, 113): SuperWin.exit_input}

    def setup(self):
        curses.noecho()
        curses.curs_set(0)
        self.m_win.nodelay(True)
        self.init_stack()
        self.m_win.keypad(True)
        self.logic.build()
        self.mine_win.draw()

    def render_all(self):
        while self.mine_win.run:
            self.status_win.render()
            self.user_input()
            self.active_win_obj.render()

    def user_input(self):
        cur_key = self.active_win.getch()
        if cur_key == -1:
            time.sleep(0.01)
        for tup in self.input_map.keys():
            for key in tup:
                if cur_key == key:
                    self.input_map[tup](self.active_win_obj)
                    break
            else:
                continue
            break

    def push_win_stack(self, win, win_obj):
        self.win_stack.insert(0, (win, win_obj))

    def pop_win_stack(self):
        self.win_stack.pop(0)

    def refresh_stack(self):
        self.active_win, self.active_win_obj = self.win_stack[0]

    def init_stack(self):
        self.push_win_stack(self.m_win, self.mine_win)
        self.refresh_stack()
