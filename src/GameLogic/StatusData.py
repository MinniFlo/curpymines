import time


class StatusData:

    def __init__(self, mine_count):
        self.remaining_mines = mine_count
        self.mine_count_digit_len = len("{}".format(mine_count))
        self.start_time = 0
        self.sum_time = 0
        self.current_time_str = ""
        self.cheat_count = 0

    def format_remaining_mines(self):
        return "{}".format(str(self.remaining_mines).rjust(self.mine_count_digit_len, "0"))

    def calc_time(self):
        cur_time = time.time()
        self.sum_time = int(cur_time - self.start_time)
        minutes = "{}".format(str(self.sum_time // 60).rjust(2, "0"))
        seconds = "{}".format(str(self.sum_time % 60).rjust(2, "0"))
        self.current_time_str = "{}:{}".format(minutes, seconds)
        return self.current_time_str

    def format_cheat_num(self):
        if self.cheat_count < 10:
            return "{}".format(str(self.cheat_count).rjust(2, "0"))
        elif self.cheat_count >= 1000:
            return "too much"
        return "{} <.<\"".format(str(self.cheat_count).rjust(2, "0"))
