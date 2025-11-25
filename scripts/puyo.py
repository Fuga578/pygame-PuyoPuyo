import pygame
from scripts.settings import *


class DummyPuyo:

    def __init__(self, color_index):
        self.color_index = color_index
        self.is_erase_checked = False


class Puyo:

    def __init__(self, game, color_index, grid_pos):
        self.game = game
        self.color_index = color_index
        self.grid_pos = list(grid_pos)

        self.pos = [self.grid_pos[0] * TILE_SIZE, self.grid_pos[1] * TILE_SIZE]

        puyo_key = self.game.puyo_keys[color_index]
        self.image = self.game.assets[puyo_key]

        self.is_falling = False

        self.is_erase_checked = False

        self.is_erasing = False
        self.is_render = True
        self.erasing_frame = 0

    def start_fall(self, dest_grid_y):
        self.grid_pos[1] = dest_grid_y
        self.is_falling = True

    def fall(self):
        if not self.is_falling:
            return

        dest_y = self.grid_pos[1] * TILE_SIZE
        self.pos[1] += FALLING_SPEED
        if self.pos[1] >= dest_y:
            self.pos[1] = dest_y
            self.is_falling = False

    def start_erase(self):
        self.erasing_frame = 0
        self.is_erasing = True

    def erase(self):
        if not self.is_erasing:
            return

        frame_ratio = self.erasing_frame / ERASING_PUYO_FRAMES
        if frame_ratio >= 1:
            self.is_erasing = False
            self.is_render = False
        elif frame_ratio >= 0.75:
            self.is_render = True
        elif frame_ratio >= 0.5:
            self.is_render = False
        elif frame_ratio >= 0.25:
            self.is_render = True
        else:
            self.is_render = False

        self.erasing_frame += 1

    def render(self, surface):
        if self.is_render:
            surface.blit(self.image, self.pos)
