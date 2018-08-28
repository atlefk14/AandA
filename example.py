import Game
import Nations
import random as r

Germany = Nations.Nation(name='Germany', human=True)
Russia = Nations.Nation(name='Russia', human=False)

x, y = 4, 4

game = Game.Game(size=(x, y), nations=[Germany, Russia])

while True:
    if game.winnerwinnerchickendinner():
        break
    if not game.currentPlayer.human:
        game.bot()
        print(game.turn)
    else:
        if game.phase == 0:
            game.phase_0()
        elif game.phase == 1:
            used = 0
            possible_unit_purchases = game.recruitable(game.PCUs - used)
            # Here one should add some AI logic, that decides what if it should buy units (from possible_unit_purchases)
            # or simply skip to next phase.
            print(possible_unit_purchases)
            # In the example below, a unit type is randomly picked from the list of possible units.
            choice = r.randint(0, len(possible_unit_purchases) - 1)
            game.recruitUnit(choice)
            used += possible_unit_purchases[choice]
            # This procedure should be repeated until the AI decides it is enough, or it isn't possible to buy anymore.
            game.nextPhase()

        elif game.phase == 2:
            # This is the phase that allows the AI to move units into enemy territory
            game.battles = []
            unit = game.moveable[0]
            # Again here, the AI should have some logic for where to move the units.
            # In this example, the first moveable unit is moved to a random location.
            pos = unit.getPosition()
            toTile = r.choice(game.map.board[pos[0]][pos[1]].neighbours)
            game.moveUnit(game.map.board[pos[0]][pos[1]], toTile, 1, unit.__class__, unit)
            # This procedure should be repeated until there are no more units to moved.
            game.nextPhase()
        elif game.phase == 2.5:
            # This the phase where the battles is being executed.
            if len(game.battles) > 0:
                print("Do actions")
                results = game.doBattle(game.battles[0])
                attacker = results[0]
                defender = results[1]
            game.nextPhase()
        elif game.phase == 3:
            # This is the same as phase two, just not allowed to move into unfriendly territory.
            # Again here the AI should make a decision, if it should move or not.
            unit = game.moveable[0]
            pos = unit.getPosition()
            possible = []
            for tile in game.map.board[pos[0]][pos[1]].neighbours:
                if tile.owner == game.currentPlayer:
                    possible.append(tile)
            if len(possible) != 0:
                toTile = r.choice(possible)
                game.moveUnit(game.map.board[pos[0]][pos[1]], toTile, 1, unit.__class__, unit)

            game.nextPhase()
        elif game.phase == 4:
            # Not implemented yet
            game.nextPhase()
        elif game.phase == 5:
            # This is the phase where one places the units that is produced in phase 1.
            if game.currentPlayer in game.purchases and game.deployablePlaces.__len__() > 0:
                tile = game.deployablePlaces[0]
                unit = game.purchases[game.currentPlayer][0]
                game.purchases[game.currentPlayer].remove(unit)
                tile.units.append(unit)
                unit.setPosition(tile.cords)

            if game.winnerwinnerchickendinner():
                break
            else:
                game.resetAllUnits()
                if not game.validBoard()[0]:
                    print("Not Valid mando")
                    print(game.map.board)
                game.nextPhase()
