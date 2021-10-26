import pygame
import math

#AWFUL code xdxdxdxd

colOff = 55


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


class Donut:
    def __init__(self, x, y, velx, vely, sprite):
        self.x = x
        self.y = y
        self.velx = velx
        self.vely = vely
        self.sprite = sprite
    def update(self, surface, decreaseAmount, res, deltaTimeMultiplier):

        self.x += self.velx * deltaTimeMultiplier
        self.y += self.vely * deltaTimeMultiplier
        self.x = clamp(self.x, colOff - 1, res[0] - colOff + 1)
        self.y = clamp(self.y, colOff - 1, res[1] - colOff + 1)

        friction = decreaseAmount * deltaTimeMultiplier
        if int(self.velx) != 0:
            self.velx -= self.velx / friction
        else:
            self.velx = 0
        if int(self.vely) != 0:
            self.vely -= self.vely / friction
        else:
            self.vely = 0
        xx, yy = self.oob(res)
        if xx:
            self.addOppForce(1, 0)
        if yy:
            self.addOppForce(1, 1)
        surface.blit(self.sprite, (self.x - self.sprite.get_width() / 2, self.y - self.sprite.get_height() / 2))
        #print(self.getAvVel())
    def getRect(self):
        return pygame.Rect(self.x - colOff, self.y - colOff, self.x + colOff, self.y + colOff)
    def addForce(self, mousePos, scale):
        #I put a lot of parentheses, just to be safe lolol
        #Also this is an absolutely terrible script FYI

        #Calculate magnitude (distance)
        delta = (self.x - mousePos[0], self.y - mousePos[1])
        v = (delta[0] * delta[0]) + (delta[1] * delta[1])
        mag = math.sqrt(v)
        if mag > 150: return
        #Canculate angle
        #ang = math.atan(delta[1] / delta[0])
        #angd = math.degrees(ang)
        pn = [clamp(delta[0], -100, 100) / 100, clamp(delta[1], -100, 100) / 100]
        self.velx += pn[0] * scale
        self.vely += pn[1] * scale
        print(pn, mag)
    def addOppForce(self, scale, mode):
        if mode == 0:
            self.velx = -self.velx * scale
        elif mode == 1:
            self.vely = -self.vely * scale
        elif mode == 2:
            self.velx = -self.velx * scale
            self.vely = -self.vely * scale
        else:
            print("BRUH WHAT THE FUCK ARE YOU DOING!?!?")
    def getAvVel(self):
        #h = (math.fabs(self.velx) + math.fabs(self.vely)) / 2
        h = math.sqrt(self.velx * self.velx + self.vely * self.vely)
        return h
    
    def oob(self, res):
        xx = self.x + colOff > res[0] or self.x - colOff < 0
        yy = self.y + colOff > res[1] or self.y - colOff < 0
        return xx, yy
    def oobt(self, res):
        xx = self.x > res[0] or self.x < 0
        yy = self.y > res[1] or self.y < 0
        return xx, yy
        

