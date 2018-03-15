import MapGenerator as mapGen
import Units
import Buildings
import random as r


class Game(object):
    def __init__(self, size, nations):
        self.map = mapGen.MapClass(size, nations)
        self.nations = nations
        self.startPlayer = nations[0][0]
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
        self.currentPlayer = self.nations[0][0]
        if self.currentPlayer == self.startPlayer:
            self.turn += 1
        self.phase = 0
        return

    def getTurn(self):
        return self.turn

    def nextPhase(self):
        if self.phase == 4:
            self.nextTurn()
        self.phase += 1

        return

    def getPhase(self):

        return self.phase

    def recruitUnit(self, n, type):
        if type == 1:
            inf = Units.Infantry(self.currentPlayer)

        if type in self.purchases:
            self.purchases[type] = []
        self.purchases[type].append(inf)

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
        for unit in fromTile.units:
            if c == n:
                break
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
                    toTile.units.append(unit)
                    fromTile.units.remove(unit)

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

    def doBattle(self, cords, attacking = dict(), defending = dict()):
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
                print(unit)
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
game.moveUnit(game.map.board[0][0], game.map.board[0][1], 2, Units.Infantry)
#game.moveUnit(game.map.board[0][0], game.map.board[0][1], 1, Units.Infantry)
#game.moveUnit(game.map.board[0][3], game.map.board[0][2], 1, Units.Infantry)
print(game.map.board[0][1])
print(game.battles[0])
results = game.doBattle(game.battles[0])
print(results)
attacker = results[0]
defender = results[1]
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
