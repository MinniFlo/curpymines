from .MineLogic import MinefieldLogic
import curses


class MineWindow:

    def __init__(self, scr):
        self.scr = scr
        self.max_y, self.max_x = self.scr.getmaxyx()
        self.logic = MinefieldLogic(self.max_y, self.max_x)
        self.run = True
        self.first = True
        self.curs_y, self.curs_x = (1, 1)

    def user_input(self):
        key = self.scr.getch()

        if key == 105 or key == 119:
            if self.curs_y > 1:
                self.curs_y -= 1
        elif key == 115 or key == 10:
            if self.curs_y < self.max_y - 2:
                self.curs_y += 1
        elif key == 97 or key == 106:
            if self.curs_x > 1:
                self.curs_x -= 1
        elif key == 100 or key == 108:
            if self.curs_x < self.max_x - 2:
                self.curs_x += 1
        elif key == 32:
            if self.first:
                self.logic.distribute_mines(self.curs_y, self.curs_x)
                self.logic.click_field(self.curs_y, self.curs_x)
                self.first = False
            else:
                self.logic.click_field(self.curs_y, self.curs_x)
        elif key == 101:
            if not self.logic.field_matrix[self.curs_y][self.curs_x].get_flag():
                self.logic.field_matrix[self.curs_y][self.curs_x].set_flag(True)
            else:
                self.logic.field_matrix[self.curs_y][self.curs_x].set_flag(False)
        elif key == 27:
            self.run = False

    def draw(self):
        self.scr.bkgd('+')
        self.scr.box()

    def render(self):
        for y in self.logic.field_matrix:
            for x in y:
                cur_y, cur_x = x.get_foordinate()
                if x.get_open():
                    if x.get_number() == 0:
                        self.scr.addstr(cur_y, cur_x, '_')
                    else:
                        self.scr.addstr(cur_y, cur_x, str(x.get_number()))
                elif x.get_flag():
                    self.scr.addstr(cur_y, cur_x, '?')
        self.scr.box()
        self.scr.move(self.curs_y, self.curs_x)

    def while_running(self):
        curses.noecho()
        self.logic.build()
        self.draw()
        self.scr.move(self.curs_y, self.curs_x)
        while self.run:
            self.user_input()
            self.scr.clear()
            self.render()
