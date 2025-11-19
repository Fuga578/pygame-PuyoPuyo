import pygame
from scripts.settings import *


class Puyo:

    def __init__(self, game, color_index, pos):
        self.game = game
        self.color_index = color_index
        self.pos = list(pos)

        puyo_key = self.game.puyo_keys[color_index]
        self.image = self.game.assets[puyo_key]

        self.dest_y = self.pos[1]
        self.is_falling = False

    def start_fall(self, dest_y):
        self.dest_y = dest_y
        self.is_falling = True

    def fall(self):
        if not self.is_falling:
            return

        self.pos[1] += FALLING_SPEED
        if self.pos[1] >= self.dest_y:
            self.pos[1] = self.dest_y
            self.is_falling = False

    def render(self, surface):
        surface.blit(self.image, self.pos)
