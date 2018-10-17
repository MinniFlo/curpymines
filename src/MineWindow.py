from Colors import Colors
import curses
from SuperWin import SuperWin
from StatusWindow import StatusWindow
from PauseWin import PauseWin


class MineWindow(SuperWin):

    def __init__(self, scr, context, manager):
        self.scr = scr
        self.manager = manager
        self.context = context
        self.logic = self.context.logic
        self.status = StatusWindow(self.manager.s_win, self.context)
        self.pause_win = PauseWin(self.manager.p_win, self.manager, self.context)
        self.max_y, self.max_x = self.scr.getmaxyx()
        self.curs_y, self.curs_x = (self.max_y // 2 - 1, 2)
        self.color = Colors()
        self.x_index = self.curs_x // 2
        self.closed_field = '*'
        self.flag_field = '?'
        self.explode_field = 'x'

    def draw(self):
        for y in range(self.max_y):
            for x in range(int(self.max_x/2)):
                self.scr.addstr(y, x*2, self.closed_field)
        self.curs_x = self.x_start()
        self.scr.box()
        self.scr.addstr(self.curs_y, self.curs_x, self.closed_field, curses.A_REVERSE)
        self.logic.render_list.add(self.logic.field_matrix[self.curs_y][self.x_index])

    def render_mine_win(self):
        if self.logic.loose:
            self.end_game()
        else:
            for cur_field in self.logic.render_list:
                cur_y, cur_x = cur_field.get_foordinate()
                if not (cur_y, cur_x) == (self.curs_y, self.curs_x):
                    style = curses.A_NORMAL
                else:
                    style = curses.A_REVERSE
                if cur_field.get_open():
                    if cur_field.get_number() == 0:
                        self.scr.addstr(cur_y, cur_x, ' ', style)
                    else:
                        self.scr.addstr(cur_y, cur_x, str(cur_field.get_number()),
                                        curses.color_pair(cur_field.get_number()) | style)
                else:
                    if cur_field.get_flag():
                        self.scr.addstr(cur_y, cur_x, self.flag_field, curses.color_pair(6) | style)
                    else:
                        self.scr.addstr(cur_y, cur_x, self.closed_field, style)
            self.scr.box()
            self.logic.render_list.clear()
            self.logic.check_win()

            if self.logic.win:
                if not self.logic.cheat:
                    self.scr.addstr(0, int(self.max_x/2 - 4), ' win ^.^ ')
                else:
                    self.scr.addstr(0, int(self.max_x/2 - 6), ' cheater >.> ')

    def end_game(self):
        for y in self.logic.field_matrix:
            for x in y:
                cur_y, cur_x = x.get_foordinate()
                if (cur_y, cur_x) in self.logic.rim_list:
                    continue
                if x.get_number() == 0:
                    self.scr.addstr(cur_y, cur_x, ' ')
                elif x.get_flag():
                    if x.get_mine():
                        self.scr.addstr(cur_y, cur_x, self.flag_field, curses.color_pair(6))
                    else:
                        self.scr.addstr(cur_y, cur_x, self.flag_field, curses.color_pair(11))
                elif x.get_number() == 9:
                        self.scr.addstr(cur_y, cur_x, self.closed_field, curses.color_pair(10))
                else:
                    self.scr.addstr(cur_y, cur_x, str(x.get_number()), curses.color_pair(x.get_number()))
        curs_field = self.logic.tuple_in_matrix((self.curs_y, self.curs_x))
        if curs_field.get_mine():
            self.scr.addstr(self.curs_y, self.curs_x, self.explode_field, curses.color_pair(9))
        else:
            self.scr.addstr(self.curs_y, self.curs_x, str(curs_field.get_number()), curses.color_pair(10))
        self.scr.refresh()
        self.scr.box()

    def reset_render(self):
        for y in self.logic.field_matrix:
            for x in y:
                cur_y, cur_x = x.get_foordinate()
                if (cur_y, cur_x) in self.logic.rim_list:
                    continue
                if x.get_open():
                    if x.get_number() == 0:
                        self.scr.addstr(cur_y, cur_x, ' ')
                    else:
                        self.scr.addstr(cur_y, cur_x, str(x.get_number()),
                                        curses.color_pair(x.get_number()))
                else:
                    if x.get_flag():
                        self.scr.addstr(cur_y, cur_x, self.flag_field, curses.color_pair(6))
                    else:
                        self.scr.addstr(cur_y, cur_x, self.closed_field)
        self.scr.box()
        self.scr.move(self.curs_y, self.curs_x)

    def x_start(self):
        x_start = int(self.max_x * 0.36)
        if x_start % 2 != 0:
            return x_start - 1
        return x_start

    def render(self):
        self.render_mine_win()
        self.status.render()

    def update_index(self):
        self.x_index = int(self.curs_x / 2)
        
    def pre_input_action(self):
        self.update_index()
        self.logic.render_list.add(self.logic.field_matrix[self.curs_y][self.x_index])
        if not self.logic.loose:
            self.logic.previous_matrix = self.logic.field_matrix
            
    def after_input_action(self):
        after_index = int(self.curs_x/2)
        self.logic.render_list.add(self.logic.field_matrix[self.curs_y][after_index])

    def up_input(self):
        if not (self.logic.loose or self.logic.win):
            self.pre_input_action()
            if self.curs_y > 1:
                self.curs_y -= 1
            self.after_input_action()

    def left_input(self):
        if not (self.logic.loose or self.logic.win):
            self.pre_input_action()
            if self.curs_x > 2:
                self.curs_x -= 2
            self.pre_input_action()

    def right_input(self):
        if not (self.logic.loose or self.logic.win):
            self.pre_input_action()
            if self.curs_x < self.max_x - 3:
                self.curs_x += 2
            self.pre_input_action()

    def down_input(self):
        if not (self.logic.loose or self.logic.win):
            self.pre_input_action()
            if self.curs_y < self.max_y - 2:
                self.curs_y += 1
            self.pre_input_action()

    def click_input(self):
        if not (self.logic.loose or self.logic.win):
            self.pre_input_action()
            if self.logic.first:
                self.logic.distribute_mines(self.curs_y, self.curs_x)
                self.logic.click_field(self.curs_y, self.curs_x)
            else:
                if not self.logic.field_matrix[self.curs_y][self.x_index].get_open():
                    self.logic.click_field(self.curs_y, self.curs_x)
                else:
                    self.logic.quality_of_life_click(self.curs_y, self.curs_x)

    def flag_input(self):
        if not (self.logic.loose or self.logic.win):
            self.pre_input_action()
            if not self.logic.loose:
                self.logic.flag_field(self.curs_y, self.x_index)

    def reset_input(self):
        self.pre_input_action()
        if self.logic.loose:
            self.logic.loose = False
            self.logic.cheat = True
            self.logic.field_matrix = self.logic.previous_matrix
            self.reset_render()
            self.logic.cheat_count += 1

    def exit_input(self):
        self.logic.pause = True
        self.manager.push_win_stack(self.manager.p_win, self.pause_win)
