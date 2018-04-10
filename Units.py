class Unit():
    def __init__(self, success=1):
        self.success = success
        self.position = None
        self.usedSteps = 0

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

    def setStep(self, increment):

        self.usedSteps += increment

    def reset(self):
        self.usedSteps = 0


class Infantry(Unit):
    def __init__(self, owner, success=2):
        super().__init__()
        self.range = 1
        self.owner = owner
        self.type = 'Inf'
        # self.setPosition(position)
        self.attSuccess = success-1
        self.defSuccess = success
        self.attachment = []

        self.cost = 2


    def __repr__(self):
        return self.owner.name + "_" + self.type


class Tank(Unit):
    def __init__(self, owner, success=3):
        super().__init__()
        self.range = 2
        self.owner = owner
        self.attSuccess = success
        self.defSuccess = success
        # self.setPosition(position)
        self.cost = 5
