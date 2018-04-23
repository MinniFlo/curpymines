from .MineLogic import MinefieldLogic
from curpymines.Colors import Colors
import curses
import time


class MineWindow:

    def __init__(self, scr):
        self.scr = scr
        self.max_y, self.max_x = self.scr.getmaxyx()
        self.logic = MinefieldLogic(self.max_y, self.max_x)
        self.run = True
        self.first = True
        self.curs_y, self.curs_x = (4, 8)
        self.color = Colors()

    def user_input(self):
        key = self.scr.getch()
        x_index = int(self.curs_x / 2)
        if key == 105 or key == 119:
            if self.curs_y > 1:
                self.curs_y -= 1
        elif key == 115 or key == 10:
            if self.curs_y < self.max_y - 2:
                self.curs_y += 1
        elif key == 97 or key == 106:
            if self.curs_x > 2:
                self.curs_x -= 2
        elif key == 100 or key == 108:
            if self.curs_x < self.max_x - 3:
                self.curs_x += 2
        elif key == 32:
            if self.first:
                self.logic.distribute_mines(self.curs_y, self.curs_x)
                self.logic.click_field(self.curs_y, self.curs_x)
                self.first = False
            else:
                if not self.logic.field_matrix[self.curs_y][x_index].get_open():
                    self.logic.click_field(self.curs_y, self.curs_x)
                else:
                    self.logic.quality_of_life_click(self.curs_y, self.curs_x)
        elif key == 101:
            cur_field = self.logic.field_matrix[self.curs_y][x_index]
            if not cur_field.get_flag():
                cur_field.set_flag(True)
            else:
                cur_field.set_flag(False)
            self.logic.render_list.add(cur_field)
        elif key == 27:
            self.run = False

    def draw(self):
        for y in range(self.max_y):
            for x in range(int(self.max_x/2)):
                self.scr.addstr(y, x*2, '+')
        self.scr.box()

    def render(self):
        if self.logic.loose:
            self.end_game()
        else:
            for cur_field in self.logic.render_list:
                cur_y, cur_x = cur_field.get_foordinate()
                if cur_field.get_open():
                    if cur_field.get_number() == 0:
                        self.scr.addstr(cur_y, cur_x, ' ')
                    else:
                        self.scr.addstr(cur_y, cur_x, str(cur_field.get_number()),
                                        curses.color_pair(cur_field.get_number()))
                else:
                    if cur_field.get_flag():
                        self.scr.addstr(cur_y, cur_x, '?', curses.color_pair(6))
                    else:
                        self.scr.addstr(cur_y, cur_x, '+')
            self.scr.box()
            self.scr.move(self.curs_y, self.curs_x)
            self.logic.render_list.clear()

    def end_game(self):
        self.scr.clear()
        for y in self.logic.field_matrix:
            for x in y:
                cur_y, cur_x = x.get_foordinate()
                if (cur_y, cur_x) in self.logic.rim_list:
                    continue
                if x.get_number() == 0:
                    self.scr.addstr(cur_y, cur_x, ' ')
                elif x.get_flag():
                    if x.get_mine():
                        self.scr.addstr(cur_y, cur_x, '?', curses.color_pair(6))
                    else:
                        self.scr.addstr(cur_y, cur_x, '?', curses.color_pair(11))
                elif x.get_number() == 9:
                        self.scr.addstr(cur_y, cur_x, '+', curses.color_pair(9))
                else:
                    self.scr.addstr(cur_y, cur_x, str(x.get_number()), curses.color_pair(x.get_number()))
        curs_field = self.logic.tuple_in_matrix((self.curs_y, self.curs_x))
        if curs_field.get_mine():
            self.scr.addstr(self.curs_y, self.curs_x, 'x', curses.color_pair(10))
        else:
            self.scr.addstr(self.curs_y, self.curs_x, str(curs_field.get_number()), curses.color_pair(10))
        self.scr.move(self.curs_y, self.curs_x)
        self.scr.refresh()
        self.scr.box()

    def while_running(self):
        curses.noecho()
        self.logic.build()
        self.draw()
        self.scr.move(self.curs_y, self.curs_x)
        while self.run:
            self.user_input()
            self.render()
