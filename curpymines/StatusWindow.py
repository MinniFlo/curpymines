import curses

class StatusWindow:

    def __init__(self, scr, logic):
        self.scr = scr
        self.logic = logic

    def render(self):
        self.scr.addstr(0, 2, 'Mines left: {}'.format(self.logic.flag_count))
        self.scr.refresh()
