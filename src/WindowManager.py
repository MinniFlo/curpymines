from MineWindow import MineWindow
from MineLogic import MinefieldLogic
from PauseWin import PauseWin
import time
import curses
from SuperWin import SuperWin


class WindowManager:

    def __init__(self, y_size, x_size, difficulty, max_mine_digit, small):
        self.y_size = y_size
        self.x_size = x_size
        self.y_pos = 0
        self.x_pos = 0
        self.difficulty = difficulty
        self.max_mine_digit = max_mine_digit
        self.small = small
        self.m_win = curses.newwin(self.y_size, self.x_size, self.y_pos, self.x_pos)
        self.s_win = curses.newwin(2, self.x_size, self.y_size , self.x_pos)
        self.p_win = curses.newwin(6, 13, self.y_pos, self.y_pos)
        self.logic = MinefieldLogic(self.y_size, self.x_size, difficulty, max_mine_digit)
        self.mine_win = MineWindow(self.m_win, self, self.small)
        self.pause_win = PauseWin(self.p_win, self)
        self.win_stack = []
        self.active_win = None
        self.active_win_obj = None
        self.input_map = {(119, 107, 259): SuperWin.up_input, (97, 104, 260): SuperWin.left_input,
                          (100, 108, 261): SuperWin.right_input, (115, 106, 258): SuperWin.down_input,
                          (32, 10): SuperWin.click_input, (101, 102): SuperWin.flag_input,
                          (114, 111): SuperWin.reset_input, (27, 113, 112): SuperWin.exit_input}
        self.run_game = True


    def setup(self):
        curses.noecho()
        curses.curs_set(0)
        self.m_win.nodelay(True)
        self.m_win.keypad(True)
        self.p_win.keypad(True)
        self.game_setup()

    def game_setup(self):
        self.init_stack()
        self.logic.build()
        self.mine_win.draw()



    def render_all(self):
        self.mine_win.status.render()
        while self.run_game:
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

    def restart(self):
        self.m_win.clear()
        self.s_win.clear()
        self.logic = MinefieldLogic(self.y_size, self.x_size, self.difficulty, self.max_mine_digit)
        self.mine_win = MineWindow(self.m_win, self, self.small)
        self.game_setup()

    def push_win_stack(self, win, win_obj):
        self.win_stack.insert(0, (win, win_obj))
        self.refresh_win_vars()

    def pop_win_stack(self):
        self.win_stack.pop(0)
        self.refresh_win_vars()

    def init_stack(self):
        self.win_stack.clear()
        self.push_win_stack(self.m_win, self.mine_win)
        self.refresh_win_vars()

    def refresh_win_vars(self):
        self.active_win, self.active_win_obj = self.win_stack[0]
