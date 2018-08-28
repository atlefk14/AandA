import Nations
import Game

import pygame
import numpy as np
from PIL import Image
from pygame.locals import *
import copy


x, y = 8, 8


Germany = Nations.Nation(name='Germany', human=False)
Russia = Nations.Nation(name='Russia', human=False, difficulty="Easy")
nations = [Germany, Russia]
game = Game.Game(size=(x, y), nations=[Germany, Russia])

game_manager = Game.GameManager()



def translate_to_array(board):
    newBoard = np.zeros((x, y, 3), dtype=np.uint8)
    globalMax = game.findGlobalMax()
    for w in board:
        row = []
        for h in w:
            tileCords = h.cords[0]
            if h.owner.name == 'Germany':
                newBoard[h.cords[0]][h.cords[1]] = np.asarray([0, 45 + int((80 * h.units.__len__()) / globalMax), 0],
                                                              dtype=np.uint8)
            elif h.owner.name == 'Russia':
                newBoard[h.cords[0]][h.cords[1]] = np.asarray([150 + (int(105 * h.units.__len__()) / globalMax), 0, 0],
                                                              dtype=np.uint8)

    return newBoard


pygame.init()

width, height = 1024, 768
screen = pygame.display.set_mode((width, height))
update = True
first = True
while True:
    if update:
        screen.fill(0)
        data = translate_to_array(game.map.board)
        img = Image.fromarray(data, 'RGB')
        img = img.resize((1024, 768))
        # img.show()
        img = pygame.surfarray.make_surface(np.array(img))
        screen.blit(pygame.transform.rotate(img, 90), (0, 0))
        pygame.display.flip()
        update = False

    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key == K_RETURN:
                while True:
                    if first:
                        game_manager.add_previous(game)
                        first = False
                    #old.append(copy.deepcopy(game))
                    game.bot()
                    print(game.phase, game.turn)
                    update = True
                    if game.phase == 0:
                        first = True
                        break

                    elif game.winnerwinnerchickendinner():
                        break

            if event.key == K_BACKSPACE:
                game = game_manager.go_back()
                update = True
