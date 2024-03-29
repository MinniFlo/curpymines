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
        self.update_index()
        self.scr.box()
        self.scr.addstr(self.cursor_y, self.cursor_x, self.closed_field, curses.color_pair(12) | curses.A_REVERSE)
        self.logic.add_field_to_render_list((self.cursor_y, self.x_index))

    def render_mine_win(self):
        if self.logic.loose:
            self.render_loose()
        else:
            self.render_fields_from_render_list()
            self.logic.check_win()
            if self.logic.win:
                if not self.logic.cheat:
                    self.scr.addstr(0, int(self.max_x / 2 - 4), ' win ^.^ ')
                else:
                    self.scr.addstr(0, int(self.max_x / 2 - 6), ' cheater >.> ')

    def render_fields_from_render_list(self):
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
                field.set_relevant(self.logic.game_grid.is_relevant_open_field(logic_coordinates))
            else:
                field.set_relevant(self.logic.game_grid.is_relevant_closed_field(logic_coordinates))

            self.scr.addstr(y_pos, x_pos, field.get_current_symbol(),
                            curses.color_pair(field.get_current_color_id()) | style)
        self.scr.box()
        self.logic.render_list.clear()

    def render_loose(self):
        for row in self.logic.game_grid.grid:
            for field in row:
                y_pos, x_pos = field.get_render_coordinates()
                if field.get_coordinates() in self.logic.game_grid.boarder:
                    continue
                # colors all flags
                if field.get_flag():
                    # correct flag
                    if field.get_mine():
                        self.scr.addstr(y_pos, x_pos, self.flag_field, curses.color_pair(11))
                    # incorrect flag
                    else:
                        self.scr.addstr(y_pos, x_pos, self.flag_field, curses.color_pair(9))
                    continue
                # color empty fields
                if field.get_number() == 0:
                    self.scr.addstr(y_pos, x_pos, ' ')
                # colors all closed mines
                elif field.get_number() == 9:
                    self.scr.addstr(y_pos, x_pos, self.closed_field, curses.color_pair(10))
                # color all fields with numbers on
                else:
                    field_num = field.get_number()
                    self.scr.addstr(y_pos, x_pos, str(field_num), curses.color_pair(field_num))
        # colors cursor position
        curs_field = self.logic.game_grid.get_field_with_coordinates((self.cursor_y, self.x_index))
        # on mine
        if curs_field.get_mine():
            self.scr.addstr(self.cursor_y, self.cursor_x, self.explode_field, curses.color_pair(9))
        else:
            self.scr.addstr(self.cursor_y, self.cursor_x, str(curs_field.get_number()), curses.color_pair(9))

        self.scr.refresh()
        self.scr.box()

    def reset_render(self):
        for row in self.logic.game_grid.grid:
            for field in row:
                y_pos, x_pos = field.get_render_coordinates()
                if field.get_coordinates() in self.logic.game_grid.boarder:
                    continue
                self.scr.addstr(y_pos, x_pos, field.get_current_symbol(),
                                curses.color_pair(field.get_current_color_id()))
        self.scr.box()

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
            
    def add_current_courser_pos_to_render(self):
        self.update_index()
        self.logic.add_field_to_render_list((self.cursor_y, self.x_index))

    def up_input(self):
        if not (self.logic.loose or self.logic.win):
            self.add_current_courser_pos_to_render()
            if self.cursor_y > 1:
                self.cursor_y -= 1
            self.add_current_courser_pos_to_render()

    def left_input(self):
        if not (self.logic.loose or self.logic.win):
            self.add_current_courser_pos_to_render()
            if self.cursor_x > 2:
                self.cursor_x -= 2
            self.add_current_courser_pos_to_render()

    def right_input(self):
        if not (self.logic.loose or self.logic.win):
            self.add_current_courser_pos_to_render()
            if self.cursor_x < self.max_x - 3:
                self.cursor_x += 2
            self.add_current_courser_pos_to_render()

    def down_input(self):
        if not (self.logic.loose or self.logic.win):
            self.add_current_courser_pos_to_render()
            if self.cursor_y < self.max_y - 2:
                self.cursor_y += 1
            self.add_current_courser_pos_to_render()

    def click_input(self):
        if not (self.logic.loose or self.logic.win):
            self.logic.update_last_game_state()
            if self.logic.first:
                self.logic.first_click(self.cursor_y, self.x_index)
            else:
                if not self.logic.game_grid.grid[self.cursor_y][self.x_index].get_open():
                    self.logic.click_closed_field(self.cursor_y, self.x_index)
                else:
                    self.logic.click_open_field(self.cursor_y, self.x_index)

    def flag_input(self):
        if not (self.logic.loose or self.logic.win or self.logic.first):
            self.logic.flag_field(self.cursor_y, self.x_index)

    def reset_input(self):
        if self.logic.loose:
            self.logic.loose = False
            self.logic.cheat = True
            self.logic.reset_to_last_game_state()
            self.reset_render()
            self.logic.statusData.cheat_count += 1
            self.add_current_courser_pos_to_render()

    def exit_input(self):
        self.logic.pause = True
        self.manager.push_win_stack(self.manager.p_win, self.pause_win)
