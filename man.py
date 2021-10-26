import pygame
from math import radians, sin
import time
import random
pygame.init()
bro = pygame.image.load('data/judges/thiscannotbereal.jpg')
bro = pygame.transform.scale(bro, (40, 40))

#HIT SOUNDS
what = pygame.mixer.Sound('data/sounds/what.wav')
chatter = pygame.mixer.Sound('data/sounds/chatter.mp3')
hit = pygame.mixer.Sound('data/sounds/hit.wav')

finish = pygame.mixer.Sound('data/sounds/finish.ogg')
finish.set_volume(0.5)

hit.set_volume(0.2)
chatter.set_volume(0.3)
what.set_volume(0.5) #😏
extra = pygame.mixer.Sound('data/sounds/extra.mp3')
extra.set_volume(15)
class Man:
    def __init__(self, sprite, scale, angle):
        self.sprite = sprite
        self.rSprite = sprite
        self.scale = scale
        self.angle = angle
        self.x = 0
        self.y = 0
        self.shudder = 50
        self.pm = False
        self.enabled = True
    def stopAllSounds():
        chatter.stop()
        
    def determinePosition(self, res, pm):
        if not self.enabled:
            self.stopAllSounds()
            return
        chatter.stop()
        switchX = {0:(res[0] / 2), 90:self.scale, 180:(res[0] / 2), 270:res[0] - self.scale}
        switchY = {0:(res[1] - self.scale), 90: (res[1] / 2), 180:self.scale, 270:(res[1] / 2)}
        self.x = switchX[self.angle]
        self.x += random.randint(-100, 100) if self.angle % 180 == 0 else 0
        self.y = switchY[self.angle]
        self.y += random.randint(-50, 50) if self.angle % 180 == 90 else 0
        self.rotateSprite(-self.angle)
        self.shudder = 50
        self.pm = pm
        if self.pm:
            what.play()
    def rotateSprite(self, angle):
        rot = pygame.transform.rotate(self.sprite, angle)
        self.rSprite = rot
        chatter.play(-1)
    def deductHealthPoints(self):
        self.health -= 1
        self.shudder *= 1.5

    def update(self, screen, donut, resetFunction):
        colliding, speed = self.colCheck(donut)
        if colliding:
            donut.addOppForce(1, 2)
            if speed:
                if self.pm:
                    what.play()
                    hit.play()
                    extra.play()
                    resetFunction(self.angle, True)
                else:
                    finish.play()
                    hit.play()
                    if self.pm:
                        extra.play()
                    resetFunction(self.angle, True)
        self.x += sin(time.time() * self.shudder * 2)
        self.y += sin(time.time() * self.shudder)
        screen.blit(self.rSprite, (self.x - (self.scale / 2), self.y - (self.scale / 2)))
        if self.pm:
            screen.blit(bro, (self.x - (self.scale / 2), self.y - (self.scale / 2)))
        return True if colliding and speed else False, self.pm

    def kill(self):
        self.enabled = False
    def colCheck(self, donut):
        o = (self.scale / 2) - 5
        d = 50
        xx = donut.x + d > self.x - o and self.x + o > donut.x - d
        yy = donut.y + d > self.y - o and self.y + o > donut.y - d
        return xx and yy, donut.getAvVel() > 250