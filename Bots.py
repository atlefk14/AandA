import random as r

def TurtleBot(self):
    moved = dict()
    if self.phase == 0:
        self.moveableUnits()
        self.deployablePlaces = self.findDeployablePlaces()
        self.nextPhase()
    elif self.phase == 1:
        # NOTE!!!!!!! This should be done the round before.
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
        self.nextPhase()
    elif self.phase == 5:
        if self.currentPlayer in self.purchases and self.deployablePlaces.__len__() > 0:
            while self.purchases[self.currentPlayer].__len__() > 0:
                i = r.randint(0, self.deployablePlaces.__len__() - 1)
                tile = self.deployablePlaces[i]
                unit = self.purchases[self.currentPlayer][0]
                self.purchases[self.currentPlayer].remove(unit)
                tile.units.append(unit)
                unit.setPosition(tile.cords)
        if self.winnerwinnerchickendinner():
            return True
        else:
            self.resetDasUnits()
            self.nextPhase()


def randomBot(self):
    moved = dict()
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
            if r.random() > 0.01:
                unit = self.moveable[0]
                pos = unit.getPosition()
                toTile = r.choice(self.map.board[pos[0]][pos[1]].neighbours)
                if toTile.owner != self.currentPlayer:
                    moved[toTile.cords.__str__()] = pos
                self.moveUnit(self.map.board[pos[0]][pos[1]], toTile, 1, unit.__class__, unit)
            else:
                break
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
        self.nextPhase()
    elif self.phase == 5:
        if self.currentPlayer in self.purchases and self.deployablePlaces.__len__() > 0:
            while self.purchases[self.currentPlayer].__len__() > 0:
                i = r.randint(0, self.deployablePlaces.__len__() - 1)
                tile = self.deployablePlaces[i]
                unit = self.purchases[self.currentPlayer][0]
                self.purchases[self.currentPlayer].remove(unit)
                tile.units.append(unit)
                unit.setPosition(tile.cords)

        if self.winnerwinnerchickendinner():
            return True
        else:
            self.resetAllUnits()
            if not self.validBoard()[0]:
                print("Not Valid mando")
                print(self.map.board)
            self.nextPhase()
