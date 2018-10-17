class Context:

    def __init__(self, logic, size, difficulty, difficulty_map, small):
        self.logic = logic
        self.y_size, self.x_size = size
        self.difficulty = difficulty
        self.difficulty_map = difficulty_map
        self.small = small

