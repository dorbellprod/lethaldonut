#SCRAPPED


import pygame

colOff = 60
#
# MISC
#
res = (512, 512)
tileSize = 32
levelRects = []

def colCheck(o, o2, x1, y1, x2, y2):
    xcheck = x1 + o > x2 and x1 - o < x2 + o2
    ycheck = y1 + o > y2 and y1 - o2 < y2 + o2 
    return xcheck, ycheck
class Level:
    def __init__(self, startPos):
        self.startPos = startPos
    def update(self, screen, tiles, tilemap, donut):
        levelRects = []
        y = 0
        for row in tilemap:
            x = 0
            for tile in row:
                if tile == 0:
                    x += 1
                    continue
                levelRects.append(pygame.Rect(x * tileSize, y * tileSize, tileSize, tileSize))
                xx, yy = colCheck(colOff, tileSize, donut.x, donut.y, x * tileSize, y * tileSize)
                if xx and yy:
                    print("AAAAAAA")
                    donut.velx = -donut.velx
                    donut.vely = -donut.vely

                screen.blit(tiles[tile], (x * tileSize, y * tileSize))
                x += 1
            y += 1




level1 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
