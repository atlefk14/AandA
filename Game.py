import MapGenerator as mapGen
import Units
import Buildings
import random as r

class Game():
    def __init__(self, size, nations):
        self.map = mapGen.MapClass(size, nations)
        self.nations = nations
        self.startPlayer = nations[0]
        self.units = dict()
        self.currentPlayer = self.startPlayer
        self.terminal = False
        self.turn = 0
        self.phase = 0
        self.purchases = dict()
        self.PCUs = None  # self.calculatePCUs()
        self.deployablePlaces = None
        self.borderTiles = self.calulateBorder()
        self.startingConditions(n=2)
        self.battles = []
        self.moveable = self.moveableUnits()
        self.recruitAbleList = [2, 5, 10]

    def calulateBorder(self):
        borderTiles = []
        for w in self.map.board:
            last = None
            for h in w:
                if last is not None:
                    if h.owner != last.owner:
                        borderTiles.append(last)
                        borderTiles.append(h)
                last = h
        return borderTiles

    def startingConditions(self, n):
        for tile in self.borderTiles:
            for i in range(n):
                infUnit = Units.Infantry(owner=tile.owner)
                tile.units.append(infUnit)
                infUnit.setPosition(tile.cords)
                if tile.owner not in self.units:
                    self.units[tile.owner] = []
                self.units[tile.owner].append(infUnit)

    def rotate(self, n=1):
        return self.nations[n:] + self.nations[:n]

    def findDeployablePlaces(self):
        deployablePlaces = []
        for w in self.map.board:
            for h in w:
                # h.constructions.append(Buildings.Industry('Germany'))
                for const in h.constructions:
                    if isinstance(const, Buildings.Industry):
                        deployablePlaces.append(h)
        return deployablePlaces

    def findMyUnits(self):

        return self.units[self.currentPlayer]

    def calculatePCUs(self):
        PCUs = 0
        for w in self.map.board:
            for h in w:
                if h.owner == self.currentPlayer:
                    PCUs += h.value
        return PCUs

    def nextTurn(self):
        self.nations = self.rotate()
        self.currentPlayer = self.nations[0]
        if self.currentPlayer == self.startPlayer:
            self.turn += 1
        self.phase = 0
        return

    def getTurn(self):
        return self.turn

    def nextPhase(self):
        self.phase += 1
        if self.phase == 4:
            self.nextTurn()
        return

    def getPhase(self):

        return self.phase

    def recruitAble(self, n):
        rtr = []
        for pos in self.recruitAbleList:
            if pos < n:
                rtr.append(pos)

        return rtr

    def recruitUnit(self, n):
        if n == 0:
            inf = Units.Infantry(self.currentPlayer)
        if not n.__str__() in self.purchases:
            self.purchases[n.__str__()] = []
        self.purchases[n.__str__()].append(inf)

    def initTurn(self):
        self.deployablePlaces = self.calculatePCUs()
        self.PCUs = self.calculatePCUs()
        self.battles = []

    def conquerTile(self, tile, newOwner):
        try:
            tile.owner = newOwner
        except:
            return None

    def moveUnit(self, fromTile, toTile, n, type):
        c = 0
        d = 0
        while True:
            if d == n:
                break
            unit = fromTile.units[c]
            c += 1
            if isinstance(unit, type):
                deltaX = abs(fromTile.cords[0] - toTile.cords[0])
                deltaY = abs(fromTile.cords[1] - toTile.cords[1])
                ##Add is legal function instead.
                if deltaX + deltaY <= unit.range:
                    if fromTile.owner !=toTile.owner:
                        if not self.battles.__contains__(toTile.cords):
                            self.battles.append(toTile.cords)
                    unit.setStep(deltaY + deltaX)
                    unit.setPosition(toTile.cords)
                    if unit.usedSteps == unit.range:
                        self.moveable.remove(unit)
                    toTile.units.append(unit)
                    fromTile.units.remove(unit)
                    d += 1
                    c -= 1
    def findPossibleBattles(self):
        battlePositions = set()
        for w in self.map.board:
            for h in w:
                for unit in h.units:
                    if not h.owner == self.currentPlayer and unit.owner == self.currentPlayer:
                        battlePositions.add(h.cords)
        return list(battlePositions)

    def getDice(self, n=6):
        return r.randint(1, n)

    def doBattle(self, cords, attacking=dict(), defending=dict()):
        for unit in self.map.board[cords[0]][cords[1]].units:
            if unit.owner == self.currentPlayer and self.map.board[cords[0]][cords[1]].owner != self.currentPlayer:
                if unit.type not in attacking:
                    attacking[unit.type] = []
                unit.setPosition(cords)
                attacking[unit.type].append(unit)
            else:
                if unit.type not in defending:
                    defending[unit.type] = []
                unit.setPosition(cords)
                defending[unit.type].append(unit)
        aHits = 0
        for key in attacking:
            for unit in attacking[key]:
                dice = self.getDice()
                #print(unit)
                if dice <= unit.attSuccess:
                    aHits += 1
        dHits = 0
        for key in defending:
            for unit in defending[key]:
                dice = self.getDice()
                if dice <= unit.defSuccess:
                    dHits += 1

        return (attacking, dHits), (defending, aHits)

    def deleteUnit(self, units):
        for unit in units:
            self.units[unit.owner].remove(unit)
            cords = unit.getPosition()
            self.map.board[cords[0]][cords[1]].units.remove(unit)
        return True

    def moveableUnits(self):
        moveable = []
        for unit in self.units[self.currentPlayer]:
            if unit.usedSteps != unit.range:
                moveable.append(unit)
        self.moveable = moveable

    def takeCasualties(self, units, choice, n):
        toBeDeleted = []
        c=0
        for unit in units[choice]:
            if c == n:
                break
            toBeDeleted.append(unit)
            c+=1
        return toBeDeleted

    def newOwner(self, cords):
        isNewOwner = True
        newOwner = ""
        for unit in self.map.board[cords[0]][cords[1]].units:
            if unit.owner == self.map.board[cords[0]][cords[1]].owner:
                isNewOwner = False
            else:
                newOwner = unit.owner

        if isNewOwner == True:
            self.conquerTile(self.map.board[cords[0]][cords[1]], newOwner)

    def direction(self, n):
        if n == 0:
            return (1,0)
        elif n == 1:
            return (0,1)
        elif n ==2:
            return (-1, 0)
        elif n ==3:
            return (0, -1)

    def randomBot(self):
        moved = dict()
        if self.phase == 0:
            self.moveableUnits()
            self.nextPhase()
        elif self.phase == 1:
            #NOTE!!!!!!! This should be done the round before.
            self.PCUs = self.calculatePCUs()
            used = 0
            while True:
                pos = self.recruitAble(self.PCUs-used)
                if pos.__len__() == 0:
                    self.nextPhase()
                    break
                #print(pos)
                choice = r.randint(0, len(pos)-1)
                self.recruitUnit(choice)
                used += pos[choice]
                print(choice)
        elif self.phase == 2:
            while self.moveable.__len__() > 0:
                if r.random() > 0.1:
                    unit = self.moveable[0]
                    pos = unit.getPosition()
                    toTile = r.choice(self.map.board[pos[0]][pos[1]].neighbours)
                    if toTile.owner != self.currentPlayer:
                        moved[toTile.cords.__str__()] = pos
                    self.moveUnit(self.map.board[pos[0]][pos[1]], toTile, 1, unit.__class__)
                    print(toTile)
                else:
                    break
            while self.battles.__len__() > 0:
                results = self.doBattle(self.battles[0])
                attacker = results[0]
                defender = results[1]
                retreat = 0.1
                random = r.random()
                if attacker[1] > 0:
                    pos = list(attacker[0].keys())
                    print(pos)

                if 0 < defender[1] < defender[0].__len__():
                    defenderKeys = list(defender[0].keys())
                    self.currentPlayer = defender[0][defenderKeys[0]][0].owner
                    print(self.map.board)
                    return defender
                else:
                    defenderDeleted = self.takeCasualties(defender[0], choice='Inf', n=defender[1])
                    print(self.map.board)
                    print(defender)
                    self.deleteUnit(defenderDeleted)
                if random < retreat:
                    print("eg trekke meg vekk wææ")
                    print(random)
            self.nextPhase()
        elif self.phase == 3:
            while self.moveable.__len__() > 0:
                if r.random() > 0.5:
                    unit = self.moveable[0]
                    pos = unit.getPosition()
                    toTile = r.choice(self.map.board[pos[0]][pos[1]].neighbours)
                    if toTile.owner != self.currentPlayer:
                        moved[toTile.cords.__str__()] = pos
                    self.moveUnit(self.map.board[pos[0]][pos[1]], toTile, 1, unit.__class__)
                else:
                    break
        elif self.phase == 4:
            print("Phase 4")



'''
game = Game((2, 2), [('Germany', 2), ('Russia', 2)])
game.nextTurn()
game.initTurn()
game.nextTurn()
game.initTurn()
print(game.findMyUnits().__len__())
# print(game.map.board)
#game.conquerTile(game.map.board[4][3], game.currentPlayer)
# print(game.map.board[3][4])
# print(game.map.board)
# print(game.map.board[0][3])
game.moveableUnits()

print(game.moveable)
#print(game.map.board[0][1])
game.moveUnit(game.map.board[0][0], game.map.board[0][1], 2, Units.Infantry)   #Ser ikke forskjell når eg sende 1 og 2 units
#game.moveUnit(game.map.board[0][0], game.map.board[0][1], 1, Units.Infantry)
#game.moveUnit(game.map.board[0][3], game.map.board[0][2], 1, Units.Infantry)
#print(game.map.board)

print(game.battles[0])
results = game.doBattle(game.battles[0])
print(results)
attacker = results[0]
defender = results[1]0
attacker = game.takeCasualties(attacker[0], choice='Inf', n=attacker[1])
print(attacker)
defender = game.takeCasualties(defender[0], choice='Inf', n=defender[1])
print(defender)
game.deleteUnit(defender)
game.deleteUnit(attacker)
print(game.map.board[0][1])
game.newOwner(game.battles[0])
print(game.map.board[0][1])
game.moveableUnits()
print(game.moveable)
'''