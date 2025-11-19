import pygame
from scripts.settings import *


class Puyo:

    def __init__(self, game, color_index, pos):
        self.game = game
        self.color_index = color_index
        self.pos = list(pos)

        puyo_key = self.game.puyo_keys[color_index]
        self.image = self.game.assets[puyo_key]

    def render(self, surface):
        surface.blit(self.image, self.pos)

    def update(self):
        pass
