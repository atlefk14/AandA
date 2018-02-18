class Unit():
    def __init__(self, success=1):
        self.success = success
        self.position = None

    def actionIsSuccessful(self, x):
        if x >= self.success:
            return True
        else:
            return False

    def getPosition(self):

        return self.position

    def setPosition(self, position):
        try:
            self.position = position
            return True
        except:
            return False


class Infantry(Unit):
    def __init__(self, owner, success=2):
        super().__init__()
        self.range = 1
        self.owner = owner
        self.success = success
        #self.setPosition(position)
        self.cost = 2

class Tank(Unit):
    def __init__(self, owner, success=3):
        super().__init__()
        self.range = 2
        self.owner = owner
        self.success = success
        #self.setPosition(position)
        self.cost = 5
