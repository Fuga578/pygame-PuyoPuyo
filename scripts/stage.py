import pygame
from scripts.settings import *
from scripts.puyo import Puyo


class Stage:

    def __init__(self, game):
        self.game = game

        # 盤面
        self.initial_board = [
            [1, 2, 3, 4, 5, 0],
            [0, 0, 2, 3, 4, 5],
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

        # 落下ぷよのリスト
        self.falling_puyo_list = []

    def set_puyo(self, grid_x, grid_y, puyo):
        self.board[grid_y][grid_x] = puyo

    def get_puyo(self, grid_x, grid_y):
        # 左右、下の範囲外の場合、ダミーぷよを返す
        if grid_x < 0 or grid_x >= STAGE_COL_NUM or grid_y >= STAGE_ROW_NUM:
            return -1
        # 上の範囲外の場合、空白判定
        if grid_y < 0:
            return None
        return self.board[grid_y][grid_x]

    def remove_puyo(self, grid_x, grid_y):
        self.board[grid_y][grid_x] = None

    def check_falling_puyo(self):
        self.falling_puyo_list = []

        # 下の行からチェック
        for grid_y in range(STAGE_ROW_NUM - 2, -1, -1):
            for grid_x in range(STAGE_COL_NUM):
                # 現在チェックマスのぷよ
                current_puyo = self.get_puyo(grid_x, grid_y)
                if not current_puyo:    # 空白の場合
                    continue

                # 1つ下のぷよ
                below_puyo = self.get_puyo(grid_x, grid_y + 1)
                if below_puyo:  # 1つ下のぷよがある場合、落下しない
                    continue

                # 該当ぷよを一度削除
                self.remove_puyo(grid_x, grid_y)

                # 最終落下y座標を算出
                dest_grid_y = grid_y
                while not self.get_puyo(grid_x, dest_grid_y + 1):
                    dest_grid_y += 1

                # ぷよ落下地点設定
                current_puyo.start_fall(dest_grid_y * TILE_SIZE)

                # 落下場所にぷよを配置
                self.set_puyo(grid_x, dest_grid_y, current_puyo)

                # 落下対象ぷよに追加
                self.falling_puyo_list.append(current_puyo)

        return len(self.falling_puyo_list) > 0

    def fall_puyo(self):
        is_falling = False

        for falling_puyo in self.falling_puyo_list:
            falling_puyo.fall()
            if falling_puyo.is_falling:
                is_falling = True

        return is_falling

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
