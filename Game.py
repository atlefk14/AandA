import MapGenerator as mapGen
import Units
import Buildings


class Game(object):
    def __init__(self, size, nations):
        self.map = mapGen.MapClass(size, nations)
        self.nations = nations
        self.startPlayer = nations[0][0]
        self.currentPlayer = self.startPlayer
        self.terminal = False
        self.turn = 0
        self.phase = 0
        self.purchases = dict()
        self.PCUs = None  # self.calculatePCUs()
        self.deployablePlaces = None  # self.findDeployablePlaces()
        self.borderTiles = self.calulateBorder()
        self.myUnits = []

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
                '''if 'inf' not in tile.units:
                    tile.units['inf'] = []
                tile.units['inf'].append(Units.Infantry(owner=tile.owner))
                '''
                tile.units.append(Units.Infantry(owner=tile.owner))

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
        unitList = []
        for w in self.map.board:
            for h in w:
                if h.owner == self.currentPlayer:
                    unitList+=h.units
        self.myUnits = unitList

        return self.myUnits

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

    def nextPhase(self):
        if self.phase == 4:
            self.nextTurn()
        self.phase += 1

        return

    def recruitUnit(self, n, type):
        if type == 1:
            inf = Units.Infantry(self.currentPlayer)

        if type in self.purchases:
            self.purchases[type] = []
        self.purchases[type].append(inf)

    def initTurn(self):
        self.deployablePlaces = self.calculatePCUs()
        self.PCUs = self.calculatePCUs()

    def conquerTile(self, tile, newOwner):
        try:
            tile.owner = newOwner
        except:
            return None

    def moveUnit(self, fromTile, toTile, n, type):
        c = 0
        for i in fromTile.units:
            if c == n:
                break
            c += 1
            if isinstance(i, type):
                deltaX = abs(fromTile.cords[0] - toTile.cords[0])
                deltaY = abs(fromTile.cords[1] - toTile.cords[1])
                ##Add is legal function instead.
                if deltaX + deltaY <= i.range:
                    i.setStep(deltaY+deltaX)
                    toTile.units.append(i)
                    fromTile.units.remove(i)
                # if fromTile.neighbours.__contains__(toTile):

    def findPossibleBattles(self):
        battlePositions = set()
        for w in self.map.board:
            for h in w:
                for unit in h.units:
                    if not h.owner == self.currentPlayer and unit.owner == self.currentPlayer:
                        battlePositions.add(h.cords)
                        print(h)
        return battlePositions

    def doBattle(self, cords):
        enemies = dict()
        friendlies = dict()
        for unit in self.map.board[cords[0]][cords[1]]:
            if unit.owner == self.currentPlayer:
                if unit.type not in friendlies:
                    friendlies[unit.type] = 0
                friendlies[unit.type] += 1
            else:
                if unit.type not in enemies:
                    enemies[unit.type] = 0
                enemies[unit.type] += 1
        

game = Game((6, 6), [('Germany', 2), ('Russia', 2)])
game.startingConditions(2)
game.nextTurn()
game.initTurn()
game.nextTurn()
game.initTurn()
print(game.findMyUnits().__len__())

game.calulateBorder()
# print(game.map.board)
game.conquerTile(game.map.board[4][3], game.currentPlayer)
# print(game.map.board[3][4])
# print(game.map.board)
# print(game.map.board[0][3])
game.moveUnit(game.map.board[0][2], game.map.board[0][3], 1, Units.Infantry)
game.moveUnit(game.map.board[0][2], game.map.board[0][3], 1, Units.Infantry)

print(game.findPossibleBattles())

# print(game.borderTiles)
