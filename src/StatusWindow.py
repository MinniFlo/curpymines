
class StatusWindow:

    def __init__(self, scr, context):
        self.scr = scr
        _, self.max_x = self.scr.getmaxyx()
        self.context = context
        self.logic = context.logic
        self.small = context.small

    def render(self):
        if not self.logic.pause:
            self.scr.addstr(0, 2, 'Mines left: {}'.format(self.logic.format_flag_num()))

            if not self.small:
                if self.logic.cheat:
                    cheat_string = 'cheatcount: {}'.format(self.logic.format_cheat_num())
                    self.scr.addstr(0, self.max_x - len(cheat_string) - 2, cheat_string)
                else:
                    if self.logic.loose or self.logic.win:
                        end_time_string = self.logic.current_time_str
                        self.scr.addstr(0, self.max_x - len(end_time_string) - 2, end_time_string)
                    else:
                        if not self.logic.first:
                            time_string = self.logic.calc_time()
                            self.scr.addstr(0, self.max_x - len(time_string) - 2, time_string)
                        else:
                            self.scr.addstr(0, self.max_x - 7, '00:00')
                self.scr.refresh()
            else:
                if self.logic.cheat:
                    self.scr.addstr(1, 2, 'cheatcount: {}'.format(self.logic.format_cheat_num()))
                else:
                    if self.logic.loose or self.logic.win:
                        self.scr.addstr(1, 2, self.logic.current_time_str)
                    else:
                        if not self.logic.first:
                            self.scr.addstr(1, 2, self.logic.calc_time())
                        else:
                            self.scr.addstr(1, 2, '00:00')
                self.scr.refresh()


