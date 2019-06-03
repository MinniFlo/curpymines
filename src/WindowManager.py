from MineWindow import MineWindow
import time
from SuperWin import SuperWin


class WindowManager:

    def __init__(self, game_setuper, context):
        self.game_setuper = game_setuper
        self.context = context
        self.m_win = game_setuper.m_win
        self.s_win = game_setuper.s_win
        self.p_win = game_setuper.p_win
        self.o_win = game_setuper.o_win
        self.d_win = game_setuper.d_win
        self.v_win = game_setuper.v_win
        self.mine_win = MineWindow(self.m_win, self.context, self)
        self.win_stack = []
        self.active_win = None
        self.active_win_obj = None
        self.input_map = {(119, 107, 259): SuperWin.up_input, (97, 104, 260): SuperWin.left_input,
                          (100, 108, 261): SuperWin.right_input, (115, 106, 258): SuperWin.down_input,
                          (32, 10): SuperWin.click_input, (101, 102, 104): SuperWin.flag_input,
                          (114, 111): SuperWin.reset_input, (27, 113, 112): SuperWin.exit_input}
        self.run_game = True
        
    def game_setup(self):
        self.init_stack()
        self.context.logic.build()
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
            if cur_key in tup:
                self.input_map[tup](self.active_win_obj)
                break

    def restart(self):
        self.m_win.clear()
        self.s_win.clear()
        self.game_setuper.update_game()
        self.mine_win = MineWindow(self.m_win, self.context, self)
        self.game_setup()

    def push_win_stack(self, win, win_obj):
        old_win, _ = self.win_stack[0]
        if old_win != self.m_win:
            old_win.clear()
            old_win.refresh()
        self.mine_win.render()
        self.m_win.refresh()

        self.win_stack.insert(0, (win, win_obj))
        self.refresh_win_vars()

    def pop_win_stack(self):
        pop_win, _ = self.win_stack.pop(0)
        self.refresh_win_vars()

        pop_win.erase()
        pop_win.refresh()
        self.mine_win.render()
        self.m_win.refresh()

    def init_stack(self):
        self.win_stack.clear()
        self.win_stack.insert(0, (self.m_win, self.mine_win))
        self.refresh_win_vars()

    def refresh_win_vars(self):
        self.active_win, self.active_win_obj = self.win_stack[0]
