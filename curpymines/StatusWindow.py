
class StatusWindow:

    def __init__(self, scr, logic):
        self.scr = scr
        _, self.max_x = self.scr.getmaxyx()
        self.logic = logic

    def render(self):
        self.scr.addstr(0, 2, 'Mines left: {}'.format(self.logic.format_flag_num()))

        if self.logic.cheat:
            self.scr.addstr(0, self.max_x - 14, "cheatcount: ")
        else:
            if self.logic.loose:
                self.scr.addstr(0, self.max_x - 7, self.logic.calc_time())
            else:
                if not self.logic.first:
                    self.scr.addstr(0, self.max_x - 7, self.logic.calc_time())
                else:
                    self.scr.addstr(0, self.max_x - 7, '00:00')
                self.scr.refresh()


