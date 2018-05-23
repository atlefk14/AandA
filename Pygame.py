import Nations
import Game
import pygame
import numpy as np
from PIL import Image
from pygame.locals import *

pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

x, y = 2, 2

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
                newBoard[h.cords[0]][h.cords[1]] = np.asarray([0, 45 + int((80 * h.units.__len__()) / globalMax), 0],
                                                              dtype=np.uint8)
            elif h.owner == Russia:
                newBoard[h.cords[0]][h.cords[1]] = np.asarray([150 + (int(105 * h.units.__len__()) / globalMax), 0, 0],
                                                              dtype=np.uint8)

    return newBoard


while True:
    screen.fill(0)
    data = translateToArray(game.map.board)
    img = Image.fromarray(data, 'RGB')
    img = img.resize((640, 480))
    # img.show()
    img = pygame.surfarray.make_surface(np.array(img))
    screen.blit(pygame.transform.rotate(img, 90), (0, 0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key == K_RETURN:
                while True:
                    game.bot()
                    if game.phase == 5:
                        print(game.turn)
                        print(game.currentPlayer)
                        print(game.map.board)
                        break
