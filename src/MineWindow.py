from Colors import Colors
import curses
from SuperWin import SuperWin
from StatusWindow import StatusWindow
from PauseWin import PauseWin
from grid_n_fields import FieldContext as FC


class MineWindow(SuperWin):

    def __init__(self, scr, context, manager):
        self.scr = scr
        self.manager = manager
        self.context = context
        self.logic = self.context.logic
        self.status = StatusWindow(self.manager.s_win, self.context)
        self.pause_win = PauseWin(self.manager.p_win, self.manager, self.context)
        self.max_y, self.max_x = self.scr.getmaxyx()
        self.cursor_y, self.cursor_x = (1, 2)
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
        self.logic.render_list.add((self.cursor_y, self.x_index))

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
        for coordinates in self.logic.render_list:
            if coordinates in self.logic.game_grid.boarder:
                continue
            with FC(self.logic.game_grid, coordinates) as field:
                y_pos, x_pos = field.render_coordinates
                if not (y_pos, x_pos) == (self.cursor_y, self.cursor_x):
                    style = curses.A_NORMAL
                else:
                    style = curses.A_REVERSE

                if field.is_open:
                    field.is_relevant = self.logic.game_grid.is_relevant_open_field(coordinates)
                else:
                    field.is_relevant = self.logic.game_grid.is_relevant_closed_field(coordinates)

                self.scr.addstr(y_pos, x_pos, field.symbol,
                                curses.color_pair(field.color_id) | style)
        self.scr.box()
        self.logic.render_list.clear()

    def render_loose(self):
        for y in range(self.logic.game_grid.y_size):
            for x in range(self.logic.game_grid.x_size):
                if (y, x) in self.logic.game_grid.boarder:
                    continue
                with FC(self.logic.game_grid, (y, x)) as field:
                    y_pos, x_pos = field.render_coordinates
                    # colors all flags
                    if field.is_flag:
                        # correct flag
                        if field.is_mine:
                            self.scr.addstr(y_pos, x_pos, self.flag_field, curses.color_pair(11))
                        # incorrect flag
                        else:
                            self.scr.addstr(y_pos, x_pos, self.flag_field, curses.color_pair(9))
                        continue
                    # color empty fields
                    if field.number == 0:
                        self.scr.addstr(y_pos, x_pos, ' ')
                    # colors all closed mines
                    elif field.number == 9:
                        self.scr.addstr(y_pos, x_pos, self.closed_field, curses.color_pair(10))
                    # color all fields with numbers on
                    else:
                        field_num = field.number
                        self.scr.addstr(y_pos, x_pos, str(field_num), curses.color_pair(field_num))
        # colors cursor position
        with FC(self.logic.game_grid, (self.cursor_y, self.x_index)) as curs_field:
            # on mine
            if curs_field.is_mine:
                self.scr.addstr(self.cursor_y, self.cursor_x, self.explode_field, curses.color_pair(9))
            else:
                self.scr.addstr(self.cursor_y, self.cursor_x, str(curs_field.number), curses.color_pair(9))

        self.scr.refresh()
        self.scr.box()

    def reset_render(self):
        for y in range(self.logic.game_grid.y_size):
            for x in range(self.logic.game_grid.x_size):
                if (y, x) in self.logic.game_grid.boarder:
                    continue
                with FC(self.logic.game_grid, (y, x)) as field:
                    y_pos, x_pos = field.render_coordinates
                    self.scr.addstr(y_pos, x_pos, field.symbol,
                                    curses.color_pair(field.color_id))
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
        self.logic.render_list.add((self.cursor_y, self.x_index))

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
            cursor_coordinates = (self.cursor_y, self.x_index)
            if self.logic.first:
                self.logic.first_click(cursor_coordinates)
            else:
                with FC(self.logic.game_grid, cursor_coordinates) as field:
                    if not field.is_open:
                        self.logic.click_closed_field(cursor_coordinates)
                    else:
                        self.logic.click_open_field(cursor_coordinates)

    def flag_input(self):
        if not (self.logic.loose or self.logic.win or self.logic.first):
            self.logic.flag_field((self.cursor_y, self.x_index))

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
