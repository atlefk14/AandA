class Nation():
    def __init__(self, name, human=True, difficulty="random"):
        self.name = name
        self.human = human
        self.difficulty = None
        if not self.human:
            self.difficulty = difficulty
