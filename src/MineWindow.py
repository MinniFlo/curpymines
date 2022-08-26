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
        self.cursor_y, self.cursor_x = (self.max_y // 2 - 1, 2)
        self.color = Colors()
        self.x_index = self.cursor_x // 2
        self.closed_field = '*'
        self.flag_field = '?'
        self.explode_field = 'x'

    def draw(self):
        for y in range(self.max_y):
            for x in range(int(self.max_x/2)):
                self.scr.addstr(y, x*2, self.closed_field, curses.color_pair(12))
        self.cursor_x = self.x_start()
        self.scr.box()
        self.scr.addstr(self.cursor_y, self.cursor_x, self.closed_field, curses.A_REVERSE)
        self.logic.add_field_to_render_list((self.cursor_y, self.x_index))

    def render_mine_win(self):
        if self.logic.loose:
            self.end_game()
        else:
            for field in self.logic.render_list:
                logic_coordinates = field.get_coordinates()
                y_pos, x_pos = field.get_render_coordinates()
                if logic_coordinates in self.logic.game_grid.boarder:
                    continue
                if not (y_pos, x_pos) == (self.cursor_y, self.cursor_x):
                    style = curses.A_NORMAL
                else:
                    style = curses.A_REVERSE
                if field.get_open():
                    if field.get_number() == 0:
                        self.scr.addstr(y_pos, x_pos, ' ', style)
                    else:
                        if self.is_relevant_number(logic_coordinates):
                            self.scr.addstr(y_pos, x_pos, str(field.get_number()),
                                            curses.color_pair(field.get_number()) | style)
                        else:
                            self.scr.addstr(y_pos, x_pos, str(field.get_number()),
                                            curses.color_pair(12) | style)
                else:
                    if field.get_flag():
                        self.scr.addstr(y_pos, x_pos, self.flag_field, curses.color_pair(6) | style)

                    else:
                        if self.is_relevant(logic_coordinates):
                            self.scr.addstr(y_pos, x_pos, self.closed_field, style)
                        else:
                            self.scr.addstr(y_pos, x_pos, self.closed_field, curses.color_pair(12) | style)

            self.scr.box()
            self.logic.render_list.clear()
            self.logic.check_win()

            if self.logic.win:
                if not self.logic.cheat:
                    self.scr.addstr(0, int(self.max_x/2 - 4), ' win ^.^ ')
                else:
                    self.scr.addstr(0, int(self.max_x/2 - 6), ' cheater >.> ')

    def end_game(self):
        for y in self.logic.game_grid.grid:
            for x in y:
                y_pos, x_pos = x.get_render_coordinates()
                if x.get_coordinates() in self.logic.game_grid.boarder:
                    continue
                if x.get_number() == 0:
                    self.scr.addstr(y_pos, x_pos, ' ')
                elif x.get_flag():
                    if x.get_mine():
                        self.scr.addstr(y_pos, x_pos, self.flag_field, curses.color_pair(6))
                    else:
                        self.scr.addstr(y_pos, x_pos, self.flag_field, curses.color_pair(11))
                elif x.get_number() == 9:
                    self.scr.addstr(y_pos, x_pos, self.closed_field, curses.color_pair(10))
                else:
                    self.scr.addstr(y_pos, x_pos, str(x.get_number()), curses.color_pair(x.get_number()))
        curs_field = self.logic.game_grid.get_field_with_coordinates((self.cursor_y, self.x_index))
        if curs_field.get_mine():
            self.scr.addstr(self.cursor_y, self.cursor_x, self.explode_field, curses.color_pair(9))
        else:
            self.scr.addstr(self.cursor_y, self.cursor_x, str(curs_field.get_number()), curses.color_pair(10))
        self.scr.refresh()
        self.scr.box()

    def reset_render(self):
        for row in self.logic.game_grid.grid:
            for field in row:
                y_pos, x_pos = field.get_render_coordinates()
                if field.get_coordinates() in self.logic.game_grid.boarder:
                    continue
                if field.get_open():
                    if field.get_number() == 0:
                        self.scr.addstr(y_pos, x_pos, ' ')
                    else:
                        self.scr.addstr(y_pos, x_pos, str(field.get_number()),
                                        curses.color_pair(field.get_number()))
                else:
                    if field.get_flag():
                        self.scr.addstr(y_pos, x_pos, self.flag_field, curses.color_pair(6))
                    else:
                        self.scr.addstr(y_pos, x_pos, self.closed_field)
        self.scr.box()

    def is_relevant(self, tup):
        y, x = tup
        for field_tup in self.logic.game_grid.neighbors_of_coordinates(y, x):
            if self.logic.game_grid.get_field_with_coordinates(field_tup).get_open():
                return True
        return False

    def is_relevant_number(self, tup):
        y, x = tup
        for field_tup in self.logic.game_grid.neighbors_of_coordinates(y, x):
            field = self.logic.game_grid.get_field_with_coordinates(field_tup)
            if (not field.get_open()) and (not field.get_flag()):
                return True
        return False

    def x_start(self):
        x_start = int(self.max_x * 0.36)
        if x_start % 2 != 0:
            return x_start - 1
        return x_start

    def render(self):
        self.render_mine_win()
        self.status.render()

    def update_index(self):
        self.x_index = self.cursor_x // 2
        
    def pre_input_action(self):
        self.update_index()
        self.logic.add_field_to_render_list((self.cursor_y, self.x_index))
        if not self.logic.loose:
            self.logic.game_grid.update_previous_game_state()
            
    def after_input_action(self):
        self.update_index()
        self.logic.add_field_to_render_list((self.cursor_y, self.x_index))

    def up_input(self):
        if not (self.logic.loose or self.logic.win):
            self.pre_input_action()
            if self.cursor_y > 1:
                self.cursor_y -= 1
            self.after_input_action()

    def left_input(self):
        if not (self.logic.loose or self.logic.win):
            self.pre_input_action()
            if self.cursor_x > 2:
                self.cursor_x -= 2
            self.pre_input_action()

    def right_input(self):
        if not (self.logic.loose or self.logic.win):
            self.pre_input_action()
            if self.cursor_x < self.max_x - 3:
                self.cursor_x += 2
            self.pre_input_action()

    def down_input(self):
        if not (self.logic.loose or self.logic.win):
            self.pre_input_action()
            if self.cursor_y < self.max_y - 2:
                self.cursor_y += 1
            self.pre_input_action()

    def click_input(self):
        if not (self.logic.loose or self.logic.win):
            self.pre_input_action()
            if self.logic.first:
                self.logic.first_click(self.cursor_y, self.x_index)
            else:
                if not self.logic.game_grid.grid[self.cursor_y][self.x_index].get_open():
                    self.logic.click_closed_field(self.cursor_y, self.x_index)
                else:
                    self.logic.click_open_field(self.cursor_y, self.x_index)

    def flag_input(self):
        if not (self.logic.loose or self.logic.win):
            self.pre_input_action()
            if not self.logic.loose:
                self.logic.flag_field(self.cursor_y, self.x_index)

    def reset_input(self):
        if self.logic.loose:
            self.pre_input_action()
            self.logic.loose = False
            self.logic.cheat = True
            self.logic.game_grid.set_grid_to_previous_state()
            self.reset_render()
            self.logic.statusData.cheat_count += 1

    def exit_input(self):
        self.logic.pause = True
        self.manager.push_win_stack(self.manager.p_win, self.pause_win)
