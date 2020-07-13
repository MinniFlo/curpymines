class Context:

    def update(self, logic, size, difficulty, difficulty_map, fullscreen, small, value_size):
        self.logic = logic
        self.y_size, self.x_size = size
        self.y_value, self.x_value = value_size
        self.difficulty = difficulty
        self.difficulty_map = difficulty_map
        self.fullscreen = fullscreen
        self.small = small

    def __init__(self, logic, size, difficulty, difficulty_map, fullscreen, small, value_size):
        self.update(logic, size, difficulty, difficulty_map, fullscreen, small, value_size)

