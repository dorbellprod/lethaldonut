import pygame
import math
import time
from random import randint

class Explosion:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.t = time.time() + 0.25
        self.enabled = True
        self.scale = 100
    def update(self, screen, dt):
        #No deltatime here trolololololollololollloololo
        if time.time() >= self.t:
            self.enabled = False
            return
        
        self.scale -= 500 * dt
        if self.scale < 0:
            self.scale = 0
        self.scale
        s = pygame.transform.scale(self.sprite, (math.floor(self.scale), math.floor(self.scale)))
        self.x += randint(-2, 2)
        self.y += randint(-2, 2)
        screen.blit(s, (self.x - s.get_width() / 2, self.y - s.get_height() / 2))