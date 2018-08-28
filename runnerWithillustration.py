import Nations
import Game
import numpy as np
from PIL import Image
import scipy

x, y = 4, 4

Germany = Nations.Nation(name='Germany', human=False)
Russia = Nations.Nation(name='Russia', human=False)
nations = [Germany, Russia]
game = Game.Game(size=(x, y), nations=[Germany, Russia])



def translateToArray(board):
    newBoard = np.zeros((x, y, 3), dtype=np.uint8)
    globalMax = game.findGlobalMax()
    for w in board:
        row = []
        for h in w:
            tileCords = h.cords[0]
            if h.owner == Germany:
                newBoard[h.cords[0]][h.cords[1]] = np.asarray([0, 45+int((80*h.units.__len__())/globalMax), 0], dtype=np.uint8)
            elif h.owner == Russia:
                newBoard[h.cords[0]][h.cords[1]] = np.asarray([150+(int(105*h.units.__len__())/globalMax), 0, 0], dtype=np.uint8)

    return newBoard


while True:
    val = game.bot()
    if game.phase == 5:
        data = translateToArray(game.map.board)
        img = Image.fromarray(data, 'RGB')
        img = img.resize((400, 400))
        img.save("Pictures/"+str(game.turn)+".jpg", 'JPEG')
        #img.show()
    if val == True:
        break
