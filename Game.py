import MapGenerator as mapGen
import Units
import Buildings
import random as r
import numpy as np

class Game():
    def __init__(self, size, nations):
        self.map = mapGen.MapClass(size, nations)
        self.nations = nations
        self.startPlayer = nations[0]
        #self.units = dict()
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
        self.recruitAbleList = [2, 5]
        self.history = []

        self.lastTurn = self.map.board

    def goback(self):
        self.map.board = self.lastTurn
        self.turn-=1


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
                tankUnit = Units.Tank(owner=tile.owner)
                tile.units.append(infUnit)
                tile.units.append(tankUnit)
                tankUnit.setPosition(tile.cords)
                infUnit.setPosition(tile.cords)
                #if tile.owner not in self.units:
                    #self.units[tile.owner] = []
                #self.units[tile.owner].append(infUnit)
                #self.units[tile.owner].append(tankUnit)

        deployed = list()
        for tile in self.borderTiles:
            if tile.owner not in deployed:
                deployed.append(tile.owner)
                tile.constructions.append(Buildings.Industry(owner=tile.owner))


    def rotate(self, n=1):
        return self.nations[n:] + self.nations[:n]

    def findDeployablePlaces(self):
        deployablePlaces = []
        for w in self.map.board:
            for h in w:
                if h.owner == self.currentPlayer:
                    for const in h.constructions:
                        if isinstance(const, Buildings.Industry):
                            deployablePlaces.append(h)

        return deployablePlaces

    def validBoard(self):
        for w in self.map.board:
            for h in w:
                for unit in h.units:
                    if unit.owner != h.owner:
                        return False
        return True


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
        if self.phase == 5:
            self.nextTurn()
            self.lastTurn = np.array(self.map.board, copy=True)
        else:
            self.phase += 1
        return

    def getPhase(self):

        return self.phase

    def recruitable(self, n):
        rtr = []
        for pos in self.recruitAbleList:
            if pos < n:
                rtr.append(pos)
        return rtr

    def recruitUnit(self, n):
        if n == 0:
            unit = Units.Infantry(self.currentPlayer)
        elif n == 1:
            unit = Units.Tank(self.currentPlayer)

        if self.currentPlayer not in self.purchases:
            self.purchases[self.currentPlayer] = []
        self.purchases[self.currentPlayer].append(unit)


    def initTurn(self):
        self.deployablePlaces = self.calculatePCUs()
        self.PCUs = self.calculatePCUs()
        self.battles = []

    def conquerTile(self, tile, newOwner):

        tile.owner = newOwner


    def moveUnit(self, fromTile, toTile, n, type, unit):
        c = 0
        d = 0
        while True:
            if d == n:
                break
            #unit = fromTile.units[c]
            c += 1
            if isinstance(unit, type):
                deltaX = abs(fromTile.cords[0] - toTile.cords[0])
                deltaY = abs(fromTile.cords[1] - toTile.cords[1])
                ##Add is legal function instead.
                if deltaX + deltaY <= unit.range:
                    if toTile.owner != self.currentPlayer:
                        if toTile.units.__len__() == 0:
                            self.conquerTile(toTile, self.currentPlayer)
                        elif not self.battles.__contains__(toTile.cords):
                            self.battles.append(toTile.cords)
                    unit.setStep(deltaY + deltaX)
                    unit.setPosition(toTile.cords)
                    unit.setOldPosition(fromTile.cords)
                    if unit.usedSteps == unit.range:
                        try:
                            self.moveable.remove(unit)
                        except ValueError:
                            print(ValueError.args)

                    toTile.units.append(unit)
                    fromTile.units.remove(unit)
                    if self.battles.__contains__(fromTile.cords):
                        valid = False
                        for unit in fromTile.units:
                            if unit.owner == self.currentPlayer:
                                valid = True
                                break
                        if not valid:
                            print(fromTile.cords)
                            self.battles.remove(fromTile.cords)
                    d += 1
                    c -= 1


    def resetDasUnits(self):
        for h in self.map.board:
            for w in h:
                for unit in w.units:
                    unit.reset()
    '''
        for unit in self.units[self.currentPlayer]:
            unit.reset()
    '''


    def findPossibleBattles(self):
        battlePositions = set()
        for w in self.map.board:
            for h in w:
                for unit in h.units:
                    if not h.owner == self.currentPlayer and unit.owner == self.currentPlayer:
                        battlePositions.add(h.cords)
        return list(battlePositions)

    def findGlobalMax(self):
        maxUnit = 0
        for w in self.map.board:
            for h in w:
                length = h.units.__len__()
                if length > maxUnit:
                    maxUnit = length

        return maxUnit


    def getDice(self, n=6):
        return r.randint(1, n)

    def moveUnit2(self, unit, toTile, unitType):
        #unit = fromTile.units[c]
        pos = unit.getPosition()
        fromTile = self.map.board[pos[0], pos[1]]
        if isinstance(unit, unitType):
            deltaX = abs(fromTile.cords[0] - toTile.cords[0])
            deltaY = abs(fromTile.cords[1] - toTile.cords[1])
            ##Add is legal function instead.
            if deltaX + deltaY <= unit.range:
                if fromTile.owner !=toTile.owner:
                    if not self.battles.__contains__(toTile.cords):
                        self.battles.append(toTile.cords)

                unit.setStep(deltaY + deltaX)
                unit.setPosition(toTile.cords)
                unit.setOldPosition(fromTile.cords)
                if unit.usedSteps == unit.range:
                    self.moveable.remove(unit)
                toTile.units.append(unit)
                fromTile.units.remove(unit)

    def doBattle(self, cords):
        attacking = dict()
        defending = dict()
        for unit in self.map.board[cords[0]][cords[1]].units:
            if unit.owner == self.currentPlayer and self.map.board[cords[0]][cords[1]].owner != self.currentPlayer:
                if unit.type not in attacking:
                    attacking[unit.type] = []
                attacking[unit.type].append(unit)
            else:
                if unit.type not in defending:
                    defending[unit.type] = []
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

    def calculateIndivualUnits(self):
        dictOfNations = dict()
        for nation in self.nations:
            total = 0
            for w in self.map.board:
                for h in w:
                    if h.owner == nation:
                        total += h.units.__len__()
            dictOfNations[nation] = total

        return dictOfNations

    def calculateUnits(self):
        total = 0
        for w in self.map.board:
            for h in w:
                total+=h.units.__len__()
        return total

    def deleteUnit(self, units):
        #x, y = units[0].getPosition()
        #heiLengde = self.map.board[x][y].units.__len__()
        for unit in units:
            cords = unit.getPosition()
            tile = self.map.board[cords[0]][cords[1]]
            tile.units.remove(unit)
            if unit in self.moveable:
                self.moveable.remove(unit)
        #hadeLengde = self.map.board[x][y].units.__len__()
        #print("hei: "+str(heiLengde))
        #print("hade: "+ str(hadeLengde))
        return True

    def moveableUnits(self):
        moveable = []
        for h in self.map.board:
            for w in h:
                for unit in w.units:
                    if unit.owner == self.currentPlayer:
                        if unit.usedSteps != unit.range:
                            moveable.append(unit)

        self.moveable = moveable

    def takeCasualties(self, units, choice, n):
        toBeDeleted = []
        c=0
        if choice == 'All':
            for key in units:
                toBeDeleted += units[key]
            #print(toBeDeleted.__len__())
            #print(n)
        else:
            for unit in units[choice]:
                if c == n:
                    break
                toBeDeleted.append(unit)
                c+=1

        self.deleteUnit(toBeDeleted)



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

    def winnerwinnerchickendinner(self):
        winner = True
        for w in self.map.board:
            for h in w:
                if h.owner != self.currentPlayer:
                    winner = False
        return winner

    def findUnitCount(self, units):
        c = 0
        for key in units:
            for unit in units[key]:
                c+=1

        return c

    def bot(self):
        if not self.currentPlayer.human:
            if self.currentPlayer.difficulty == "Random":
                self.randomBot()
            elif self.currentPlayer.difficulty == "Turtle":
                print("Turle")
                self.TurtleBot()
            elif self.currentPlayer.difficulty == "Easy":
                self.easyBot()
    '''
    def easyBot(self):
        if self.phase == 0:
            self.moveableUnits()
            self.deployablePlaces = self.findDeployablePlaces()
            self.nextPhase()

        elif self.phase == 1:
            self.PCUs = self.calculatePCUs()
            used = 0
            while True:
                pos = self.recruitable(self.PCUs - used)
                if pos.__len__() == 0:
                    self.nextPhase()
                    break
                choice = r.randint(0, len(pos) - 1)
                self.recruitUnit(choice)
                used += pos[choice]
        elif self.phase == 2:
            self.battles = []
            while self.moveable.__len__() > 0:
                unit = self.moveable[0]
                x, y = unit.getPosition()
                currentTile = self.map.board[x][y]
                possibleDestinations = currentTile.neighbours
                realisticDestination = []
                for tile in possibleDestinations:
                    if tile.owner != self.currentPlayer:
                        print("Foe"+ str(tile.units.__len__()))
                        print(currentTile.units.__len__())
                        if tile.units.__len__() <= currentTile.units.__len__():
                            print("I add")
                            realisticDestination.append(tile)
                if realisticDestination.__len__() == 0:
                    print("Ingen realistiske mål, turlemode")
                    break
                destTile = r.choice(realisticDestination)
                if destTile.units.__len__() == currentTile.units.__len__():
                    for unit in currentTile.units:
                        self.moveUnit(currentTile, destTile, 1, unit.__class__, unit)
                else:
                    c = currentTile.units.__len__()
                    for unit in currentTile.units:
                        if c == 1:
                            break
                        self.moveUnit(currentTile, destTile, 1, unit.__class__, unit)
                        c-=1
                self.phase = 2.5
        elif self.phase == 2.5:
            while self.battles.__len__() > 0:
                results = self.doBattle(self.battles[0])
                attacker = results[0]
                defender = results[1]
                attackFinished = False
                defendFinished = False
                if attacker[1] > 0:
                    attackerCount = self.findUnitCount(attacker[0])
                    attackerTypes = list(attacker[0].keys())
                    if attacker[1] >= attackerCount:
                        self.takeCasualties(attacker[0], 'All', attackerCount)
                        attackFinished = True
                    else:
                        toBeDeleted = dict()
                        for i in range(attacker[1]):
                            unitType = r.choice(attackerTypes)
                            unit = attacker[0][unitType][0]
                            if not unit.type in toBeDeleted:
                                toBeDeleted[unit.type] = []
                            toBeDeleted[unit.type].append(unit)
                            attacker[0][unitType].remove(unit)
                            if attacker[0][unitType].__len__() == 0:
                                attacker[0].pop(unitType, None)
                            attackerTypes = list(attacker[0].keys())

                        for key in toBeDeleted:
                            self.takeCasualties(toBeDeleted, toBeDeleted[key][0].type, toBeDeleted[key].__len__())

                if defender[1] > 0:
                    defenderCount = self.findUnitCount(defender[0])
                    defenderTypes = list(defender[0].keys())
                    if defender[1] >= defenderCount:
                        self.takeCasualties(defender[0], 'All', defenderCount)
                        defendFinished = True

                    else:
                        defenderKeys = list(defender[0].keys())
                        if not defender[0][defenderKeys[0]][0].owner.human:
                            toBeDeleted = dict()
                            for i in range(defender[1]):
                                unitType = r.choice(defenderTypes)
                                unit = defender[0][unitType][0]
                                if not unit.type in toBeDeleted:
                                    toBeDeleted[unit.type] = []
                                toBeDeleted[unit.type].append(unit)
                                defender[0][unitType].remove(unit)
                                if defender[0][unitType].__len__() == 0:
                                    defender[0].pop(unitType, None)
                                defenderTypes = list(defender[0].keys())
                            for key in toBeDeleted:
                                self.takeCasualties(toBeDeleted, toBeDeleted[key][0].type, toBeDeleted[key].__len__())
                        else:
                            self.currentPlayer = defender[0][defenderKeys[0]][0].owner
                            return defender

                if defendFinished and not attackFinished:
                    self.conquerTile(self.map.board[self.battles[0][0]][self.battles[0][1]], self.currentPlayer)

                if attackFinished or defendFinished:
                    self.battles.remove(self.battles[0])

            self.phase = 3
        elif self.phase == 3:
            while self.moveable.__len__() > 0:
                if r.random() > 0.5:
                    unit = self.moveable[0]
                    pos = unit.getPosition()
                    possible = []
                    for tile in self.map.board[pos[0]][pos[1]].neighbours:
                        if tile.owner == self.currentPlayer:
                            possible.append(tile)
                    if possible.__len__() == 0:
                        self.moveable.remove(self.moveable[0])
                        break
                    toTile = r.choice(possible)

                    if toTile.owner == self.currentPlayer:
                        self.moveUnit(self.map.board[pos[0]][pos[1]], toTile, 1, unit.__class__, unit)
                else:
                    break
            self.nextPhase()
        elif self.phase == 4:
            #print("Phase 4")
            self.nextPhase()
        elif self.phase == 5:
            #print("Phase 5")
            if self.winnerwinnerchickendinner():
                print(self.turn)
                return True
            else:
                if self.turn % 100 == 0:
                    print(self.calculateIndivualUnits())
                self.resetDasUnits()
                self.nextPhase()

            if self.currentPlayer in self.purchases and self.deployablePlaces.__len__() > 0:
                while self.purchases[self.currentPlayer].__len__() > 0:

                    i = r.randint(0, self.deployablePlaces.__len__() - 1)
                    tile = self.deployablePlaces[i]
                    unit = self.purchases[self.currentPlayer][0]
                    self.purchases[self.currentPlayer].remove(unit)
                    tile.units.append(unit)
                    unit.setPosition(tile.cords)
                    #self.units[self.currentPlayer].append(unit)
    '''
    def TurtleBot(self):
        moved = dict()
        print("Hei")
        if self.phase == 0:
            self.moveableUnits()
            self.deployablePlaces = self.findDeployablePlaces()
            self.nextPhase()
        elif self.phase == 1:
            #NOTE!!!!!!! This should be done the round before.
            self.PCUs = self.calculatePCUs()
            used = 0
            while True:
                pos = self.recruitable(self.PCUs-used)
                if pos.__len__() == 0:
                    self.nextPhase()
                    break
                choice = r.randint(0, len(pos)-1)
                self.recruitUnit(choice)
                used += pos[choice]
        elif self.phase == 2:
            while self.moveable.__len__() > 0:
                break
            self.nextPhase()

        elif self.phase == 3:
            while self.moveable.__len__() > 0:
                if r.random() > 0.5:
                    unit = self.moveable[0]
                    pos = unit.getPosition()
                    possible = []
                    for tile in self.map.board[pos[0]][pos[1]].neighbours:
                        if tile.owner == self.currentPlayer:
                            possible.append(tile)
                    if possible.__len__() == 0:
                        self.moveable.remove(self.moveable[0])
                        break
                    toTile = r.choice(possible)
                    if toTile.owner == self.currentPlayer:
                        self.moveUnit(self.map.board[pos[0]][pos[1]], toTile, 1, unit.__class__, unit)
                else:
                    break
            self.nextPhase()
        elif self.phase == 4:
            #print("Phase 4")
            self.nextPhase()
        elif self.phase == 5:
            #print("Phase 5")
            if self.winnerwinnerchickendinner():
                print(self.turn)
                return True
            else:
                if self.turn % 100 == 0:
                    print(self.calculateIndivualUnits())
                self.resetDasUnits()
                self.nextPhase()

            if self.currentPlayer in self.purchases and self.deployablePlaces.__len__() > 0:
                while self.purchases[self.currentPlayer].__len__() > 0:
                    i = r.randint(0, self.deployablePlaces.__len__() - 1)
                    tile = self.deployablePlaces[i]
                    unit = self.purchases[self.currentPlayer][0]
                    self.purchases[self.currentPlayer].remove(unit)
                    tile.units.append(unit)
                    unit.setPosition(tile.cords)
                    #self.units[self.currentPlayer].append(unit)

    def findAllBattles(self):
        battles = set()
        for w in self.map.board:
            for h in w:
                for unit in h.units:
                    if unit.owner != h.owner:
                        battles.add(h.cords)
        return list(battles)

    def randomBot(self):
        moved = dict()
        if self.phase == 0:
            self.moveableUnits()
            self.deployablePlaces = self.findDeployablePlaces()
            #print(self.currentPlayer)
            #print(self.deployablePlaces)
            self.nextPhase()
        elif self.phase == 1:
            #NOTE!!!!!!! This should be done the round before.
            self.PCUs = self.calculatePCUs()
            used = 0
            while True:
                pos = self.recruitable(self.PCUs-used)
                if pos.__len__() == 0:
                    self.nextPhase()
                    break
                choice = r.randint(0, len(pos)-1)
                self.recruitUnit(choice)
                used += pos[choice]
        elif self.phase == 2:
            self.battles = []
            while self.moveable.__len__() > 0:
                if r.random() > 0.1:
                    unit = self.moveable[0]
                    pos = unit.getPosition()
                    toTile = r.choice(self.map.board[pos[0]][pos[1]].neighbours)
                    if toTile.owner != self.currentPlayer:
                        moved[toTile.cords.__str__()] = pos
                    self.moveUnit(self.map.board[pos[0]][pos[1]], toTile, 1, unit.__class__, unit)
                    #print(toTile)
                else:
                    break
            self.phase=2.5

        elif self.phase == 2.5:
            Real = self.findAllBattles()
            #print(self.battles)
            #print(Real)
            while self.battles.__len__() > 0:
                results = self.doBattle(self.battles[0])
                attacker = results[0]
                defender = results[1]
                attackFinished = False
                defendFinished = False
                if attacker[1] > 0:
                    attackerCount = self.findUnitCount(attacker[0])
                    attackerTypes = list(attacker[0].keys())
                    if attacker[1] >= attackerCount:
                        #print(type(attacker[1]))
                        x, y = self.battles[0]
                        before = self.map.board[x][y].units.__len__()
                        #print(self.battles[0])
                        #print("Before: " + str(before))
                        self.takeCasualties(attacker[0], 'All', attackerCount)
                        #print(attackerCount)
                        #print(attacker[0])
                        #print("After: "+str(self.map.board[x][y].units.__len__()))
                        attackFinished = True
                    else:
                        toBeDeleted = dict()
                        x, y = self.battles[0]
                        before = self.map.board[x][y].units.__len__()
                        for i in range(attacker[1]):
                            unitType = r.choice(attackerTypes)
                            unit = attacker[0][unitType][0]
                            if not unit.type in toBeDeleted:
                                toBeDeleted[unit.type] = []
                            toBeDeleted[unit.type].append(unit)
                            attacker[0][unitType].remove(unit)
                            if attacker[0][unitType].__len__() == 0:
                                attacker[0].pop(unitType, None)
                            attackerTypes = list(attacker[0].keys())

                        for key in toBeDeleted:
                            self.takeCasualties(toBeDeleted, toBeDeleted[key][0].type, toBeDeleted[key].__len__())
                        after = self.map.board[x][y].units.__len__()
                        #print("Remove some")
                        #print(self.battles[0])
                        #print("Before: "+str(before))
                        #print("After: "+str(after))

                if defender[1] > 0:
                    defenderCount = self.findUnitCount(defender[0])
                    defenderTypes = list(defender[0].keys())
                    if defender[1] >= defenderCount:
                        self.takeCasualties(defender[0], 'All', defenderCount)
                        defendFinished = True
                    else:
                        defenderKeys = list(defender[0].keys())
                        if not defender[0][defenderKeys[0]][0].owner.human:
                            toBeDeleted = dict()
                            for i in range(defender[1]):
                                unitType = r.choice(defenderTypes)
                                unit = defender[0][unitType][0]
                                if not unit.type in toBeDeleted:
                                    toBeDeleted[unit.type] = []
                                toBeDeleted[unit.type].append(unit)
                                defender[0][unitType].remove(unit)
                                if defender[0][unitType].__len__() == 0:
                                    defender[0].pop(unitType, None)
                                defenderTypes = list(defender[0].keys())
                            for key in toBeDeleted:
                                self.takeCasualties(toBeDeleted, toBeDeleted[key][0].type, toBeDeleted[key].__len__())
                        else:
                            self.currentPlayer = defender[0][defenderKeys[0]][0].owner
                            return defender

                if defendFinished and not attackFinished:
                    self.conquerTile(self.map.board[self.battles[0][0]][self.battles[0][1]], self.currentPlayer)

                if attackFinished or defendFinished:
                    self.battles.remove(self.battles[0])

            self.phase = 3
        elif self.phase == 3:
            while self.moveable.__len__() > 0:
                if r.random() > 0.5:
                    unit = self.moveable[0]
                    pos = unit.getPosition()
                    possible = []
                    for tile in self.map.board[pos[0]][pos[1]].neighbours:
                        if tile.owner == self.currentPlayer:
                            possible.append(tile)
                    if possible.__len__() == 0:
                        self.moveable.remove(self.moveable[0])
                        break
                    toTile = r.choice(possible)

                    if toTile.owner == self.currentPlayer:
                        self.moveUnit(self.map.board[pos[0]][pos[1]], toTile, 1, unit.__class__, unit)
                else:
                    break
            self.nextPhase()
        elif self.phase == 4:
            #print("Phase 4")
            self.nextPhase()
        elif self.phase == 5:
            #print(self.map.board)
            #print("Phase 5")
            if self.currentPlayer in self.purchases and self.deployablePlaces.__len__() > 0:
                #print("Eg KJØBE FARRR")
                #print(self.deployablePlaces)
                #print(self.purchases[self.currentPlayer])
                while self.purchases[self.currentPlayer].__len__() > 0:
                    i = r.randint(0, self.deployablePlaces.__len__() - 1)
                    tile = self.deployablePlaces[i]
                    unit = self.purchases[self.currentPlayer][0]
                    #print(self.currentPlayer)
                    #print(unit.owner)
                    self.purchases[self.currentPlayer].remove(unit)
                    tile.units.append(unit)
                    unit.setPosition(tile.cords)
                    #self.units[self.currentPlayer].append(unit)

            if self.winnerwinnerchickendinner():
                print(self.turn)
                return True
            else:
                self.resetDasUnits()
                self.nextPhase()
                print(self.map.board)
                print(self.calculateIndivualUnits())


