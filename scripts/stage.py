import pygame
from scripts.settings import *
from scripts.puyo import Puyo


class Stage:

    def __init__(self, game):
        self.game = game

        # 盤面
        self.initial_board = [
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
        self.board = [[None for _ in range(STAGE_COL_NUM)] for _ in range(STAGE_ROW_NUM)]
        self._create_initial_puyo()

    def set_puyo(self, x, y, puyo):
        self.board[y][x] = puyo

    def get_puyo(self, x, y):
        # 左右、下の範囲外の場合、ダミーぷよを返す
        if x < 0 or x >= STAGE_COL_NUM or y >= STAGE_ROW_NUM:
            return -1
        # 上の範囲外の場合、空白判定
        if y < 0:
            return None
        return self.board[y][x]

    def remove_puyo(self, x, y):
        self.board[y][x] = None

    def _create_initial_puyo(self):
        for row_index, row in enumerate(self.initial_board):
            for col_index, col in enumerate(row):
                if col > 0:
                    color_index = col - 1
                    puyo = Puyo(self.game, color_index, (col_index * TILE_SIZE, row_index * TILE_SIZE))
                    self.set_puyo(col_index, row_index, puyo)

    def _render_grid(self, surface):
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

    def _render_puyo(self, surface):
        for row in self.board:
            for puyo in row:
                if puyo:
                    puyo.render(surface)

    def render(self, surface):
        # グリッド線の描画
        self._render_grid(surface)

        # ぷよの描画
        self._render_puyo(surface)
