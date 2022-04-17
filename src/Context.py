class Context:

    def update(self, logic, size, difficulty, fullscreen, small, value_size):
        self.logic = logic
        # number of terminal monospace that are needed to display game
        self.y_size, self.x_size = size
        # number of fields in height and width wise
        self.y_value, self.x_value = value_size
        # set difficulty
        self.difficulty = difficulty
        # mapping of difficulty number to mine percentage
        self.fullscreen = fullscreen
        self.small = small

    def __init__(self, logic, size, difficulty, fullscreen, small, value_size):
        self.update(logic, size, difficulty, fullscreen, small, value_size)
