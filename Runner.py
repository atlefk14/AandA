from Game import Game
import Units
import Nations

def actionPhase(game):


    game.nextPhase()
    return game



def movementPhase(game):

    game.moveableUnits()
    print(game.map.board)
    text = input("would you like to move any pieces?  y/n")
    if text == "y":
        game.moveUnit(game.map.board[0][0], game.map.board[0][1], 2, Units.Infantry)
        #Move something
    else:
        game.nextPhase()
        return game

    game.nextPhase()
    return game

def placingPhase(game):



    game.nextPhase()
    return game
def buyingPhase(game):



    game.nextPhase()
    return game



def gameLoop(game):
    while True:
        if game.phase == 0:
            game.nextPhase()
        elif game.phase == 1:
            buyingPhase(game)
        elif game.phase == 2:
            movementPhase(game)
        elif game.phase == 3:
            actionPhase(game)
        elif game.phase == 4:
            placingPhase(game)
        print(game.phase)
        print(game.currentPlayer)


listOfNations = [Nations.Nation('Germany'), Nations.Nation('Russia', human = False)]
game = Game((2, 2), listOfNations)
