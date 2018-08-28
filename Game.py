import MapGenerator as mapGen
import Units
import Buildings
import random as r
import copy
import numpy as np


class GameManager(object):
    def __init__(self):
        self.previous_states = []

    def add_previous(self, game):
        print("Legger til forrige")
        self.previous_states.append(copy.deepcopy(game))

    def go_back(self):
        try:
            print("Går tilbake til forrige")
            previous_state = self.previous_states.pop()
            return previous_state
        except IndexError as e:
            print(e)
            return None


class Game():
    def __init__(self, size, nations):
        self.map = mapGen.MapClass(size, nations)
        self.nations = nations
        self.startPlayer = nations[0]
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

    def phase_0(self):
        self.moveableUnits()
        self.deployablePlaces = self.findDeployablePlaces()
        self.nextPhase()
        self.PCUs = self.calculatePCUs()

    def startingConditions(self, n):
        for tile in self.borderTiles:
            for i in range(n):
                infUnit = Units.Infantry(owner=tile.owner)
                tankUnit = Units.Tank(owner=tile.owner)
                tile.units.append(infUnit)
                tile.units.append(tankUnit)
                tankUnit.setPosition(tile.cords)
                infUnit.setPosition(tile.cords)

        # All the way to the left
        tile = self.map.board[int(self.map.board.__len__() / 2) - 1][0]
        tile.constructions.append(Buildings.Industry(owner=tile.owner))
        print(self.map.board.__len__())
        # All the way to the right
        tile = self.map.board[int(self.map.board.__len__() / 2) - 1][self.map.board.__len__() - 1]
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
                        return (False, h.cords)
        return (True, -1)

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
            c += 1
            if isinstance(unit, type):
                deltaX = abs(fromTile.cords[0] - toTile.cords[0])
                deltaY = abs(fromTile.cords[1] - toTile.cords[1])

                # todo add is legal function instead.
                if deltaX + deltaY <= unit.range:
                    if toTile.owner != self.currentPlayer:
                        if unit.usedSteps == 0:
                            unit.setStep(unit.range)
                        else:
                            unit.setStep(deltaX + deltaY)

                        if toTile.units.__len__() == 0:
                            self.conquerTile(toTile, self.currentPlayer)
                        elif not self.battles.__contains__(toTile.cords):
                            self.battles.append(toTile.cords)
                    else:
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
                            self.battles.remove(fromTile.cords)
                    d += 1
                    c -= 1

    def resetAllUnits(self):
        for h in self.map.board:
            for w in h:
                for unit in w.units:
                    unit.reset()

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
                # print(unit)
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
                total += h.units.__len__()
        return total

    def deleteUnit(self, units):
        for unit in units:
            cords = unit.getPosition()
            tile = self.map.board[cords[0]][cords[1]]
            tile.units.remove(unit)
            if unit in self.moveable:
                self.moveable.remove(unit)
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
        c = 0
        if choice == 'All':
            for key in units:
                toBeDeleted += units[key]
        else:
            for unit in units[choice]:
                if c == n:
                    break
                toBeDeleted.append(unit)
                c += 1

        self.deleteUnit(toBeDeleted)

    def winnerwinnerchickendinner(self):
        winner = True
        for w in self.map.board:
            for h in w:
                if h.owner != self.currentPlayer:
                    winner = False
        return winner

    def findMovableInTile(self, cords):
        units = []
        for unit in self.map.board[cords[0]][cords[1]].units:
            if unit.usedSteps > unit.range:
                units.append(unit)
        return units

    def findUnitCount(self, units):
        c = 0
        for key in units:
            for unit in units[key]:
                c += 1

        return c

    def bot(self):
        import Bots
        if not self.currentPlayer.human:
            if self.currentPlayer.difficulty == "Random":
                Bots.randomBot(self)
            elif self.currentPlayer.difficulty == "Turtle":
                Bots.TurtleBot(self)
            elif self.currentPlayer.difficulty == "Easy":
                Bots.easyBot(self)
