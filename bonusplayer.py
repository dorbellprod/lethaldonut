import pygame
from math import sin
from random import randint
import time

finish = pygame.mixer.Sound('data/sounds/finish.ogg')

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

class Player:
    def __init__(self, x, y, vel, size):
        self.x = x
        self.y = y
        self.vel = vel
        self.size = size
    def update(self, canMove, keys, res, sprite, screen, dt):
        ang = 50
        if canMove:
            if keys[pygame.K_LEFT]:
                self.x -= self.vel * dt
            if keys[pygame.K_RIGHT]:
                self.x += self.vel * dt
            if keys[pygame.K_UP]:
                self.y -= self.vel * dt
            if keys[pygame.K_DOWN]:
                self.y += self.vel * dt
        self.x = clamp(self.x, self.size, res[0] - self.size)
        self.y = clamp(self.y, self.size, res[1] - self.size)
        _sprite = pygame.transform.rotate(sprite, sin(time.time() * ang) * 5)
        screen.blit(_sprite, (self.x - sprite.get_width() / 2, self.y - sprite.get_height() / 2))

class FlyingDonut:
    def __init__(self, vel, res):
        self.vel = vel
        d = randint(1, 2)
        if d == 1:
            self.dir = 1
            self.kill = res[0] + 75
            self.x = -75
        else:
            self.dir = -1
            self.kill = -75
            self.x = res[0] + 75
        self.y = randint(30, res[1] - 30)
    def update(self, screen, sprite, res, dt, player):
        colliding = self.colCheck(sprite, player)
        if colliding:
            print("YOU LOSE, LOISER")
            finish.play()
        self.x += self.vel * self.dir * dt
        screen.blit(sprite, (self.x - sprite.get_width() / 2, self.y - sprite.get_height() / 2))
        return colliding
    def colCheck(self, sprite, player):
        o = (sprite.get_width() / 2) - 15
        p = 20 - 5
        xx = self.x + o > player.x - p and self.x - o < player.x + p
        yy = self.y + o > player.y - p and self.y - o < player.y + p
        return xx and yy