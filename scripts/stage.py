import pygame
from scripts.settings import *


class Stage:

    def __init__(self, game):
        self.game = game

        # 盤面
        self.board = [
            [1, 2, 3, 4, 5, 0],
            [0, 1, 2, 3, 4, 5],
            [0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]

    def _draw_grid(self, surface):
        # 縦線の描画
        for i in range(STAGE_COL_NUM):
            pygame.draw.line(
                surface,
                COLORS["line_color"],
                (i * TILE_SIZE, 0),
                (i * TILE_SIZE, SCREEN_HEIGHT)
            )
        # 横線の描画
        for i in range(STAGE_ROW_NUM):
            pygame.draw.line(
                surface,
                COLORS["line_color"],
                (0, i * TILE_SIZE),
                (SCREEN_WIDTH, i * TILE_SIZE)
            )

    def _draw_puyo(self, surface):
        for row_index, row in enumerate(self.board):
            for col_index, col in enumerate(row):
                if col != 0:
                    puyo_key = self.game.puyo_list[col - 1]
                    puyo_img = self.game.assets[puyo_key]

                    surface.blit(
                        puyo_img,
                        (col_index * TILE_SIZE, row_index * TILE_SIZE)
                    )

    def render(self, surface):
        # グリッド線の描画
        self._draw_grid(surface)

        # ぷよの描画
        self._draw_puyo(surface)
