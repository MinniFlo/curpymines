import time


class StatusWindow:

    def __init__(self, scr, logic):
        self.scr = scr
        _, self.max_x = self.scr.getmaxyx()
        self.logic = logic

    def render(self):
        while not self.logic.loose:
            if self.logic.flag_count >= 10:
                self.scr.addstr(0, 2, 'Mines left: {}'.format(self.logic.flag_count))
            else:
                self.scr.addstr(0, 2, 'Mines left: 0{}'.format(self.logic.flag_count))

            if not self.logic.first:
                self.scr.addstr(0, self.max_x - 7, self.logic.calc_time())
            else:
                self.scr.addstr(0, self.max_x - 7, '00:00')
            self.scr.refresh()
            time.sleep(2)
