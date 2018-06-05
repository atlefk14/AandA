def moveUnit2(self, unit, toTile, unitType):
    # unit = fromTile.units[c]
    pos = unit.getPosition()
    fromTile = self.map.board[pos[0], pos[1]]
    if isinstance(unit, unitType):
        deltaX = abs(fromTile.cords[0] - toTile.cords[0])
        deltaY = abs(fromTile.cords[1] - toTile.cords[1])
        ##Add is legal function instead.
        if deltaX + deltaY <= unit.range:
            if fromTile.owner != toTile.owner:
                if not self.battles.__contains__(toTile.cords):
                    self.battles.append(toTile.cords)

            unit.setStep(deltaY + deltaX)
            unit.setPosition(toTile.cords)
            unit.setOldPosition(fromTile.cords)
            if unit.usedSteps == unit.range:
                self.moveable.remove(unit)
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


def findAllBattles(self):
    battles = set()
    for w in self.map.board:
        for h in w:
            for unit in h.units:
                if unit.owner != h.owner:
                    battles.add(h.cords)
    return list(battles)



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