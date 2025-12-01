import pygame
import random
import math
from scripts.settings import *
from scripts.puyo import Puyo
from enum import Enum, auto


class PlayerState(Enum):
    PLAYING = auto()
    FIX = auto()


class Player:

    def __init__(self, game):
        self.game = game

        self.center_puyo = None
        self.rotated_puyo = None

        # 中心ぷよの位置
        self.grid_x = 0
        self.grid_y = 0
        self.top = self.grid_y * TILE_SIZE
        self.left = self.grid_x * TILE_SIZE
        # 中心ぷよから見た回転ぷよの位置
        self.grid_dx = 0
        self.grid_dy = 0
        self.rotation = 0

        self.grounded_frames = 0

    def create_puyo(self):
        # ぷよを作成できるかチェック
        if self.game.stage.get_puyo(grid_x=2, grid_y=0):
            return False

        # 接地フレーム初期化
        self.grounded_frames = 0

        # カラーの決定
        center_puyo_color_index = random.randint(0, len(self.game.puyo_keys) - 1)
        rotated_puyo_color_index = random.randint(0, len(self.game.puyo_keys) - 1)

        # 中心ぷよの位置
        self.grid_x = 2
        self.grid_y = -1
        self.top = self.grid_y * TILE_SIZE
        self.left = self.grid_x * TILE_SIZE

        # 中心ぷよから見た回転ぷよの位置
        self.grid_dx = 0
        self.grid_dy = -1
        self.rotation = 0

        # ぷよの作成
        self.center_puyo = Puyo(
            self.game,
            center_puyo_color_index,
            (self.grid_x, self.grid_y)
        )
        self.rotated_puyo = Puyo(
            self.game,
            rotated_puyo_color_index,
            (
                self.grid_x + self.grid_dx,
                self.grid_y + self.grid_dy
            )
        )
        self._set_puyo_pos()

        return True

    def _auto_fall(self):
        # 操作ぷよの下にぷよがない場合
        if not self.game.stage.get_puyo(self.grid_x, self.grid_y + 1) \
                and not self.game.stage.get_puyo(self.grid_x + self.grid_dx, self.grid_y + self.grid_dy + 1):
            self.top += PLAYER_FALLING_SPEED    # 自由落下
            # 自由落下でマス目の境界を超えた場合、位置を下に1つずらす
            if math.floor(self.top / TILE_SIZE) != self.grid_y:
                self.grid_y += 1
                # 再度1つ下のぷよが無いかチェック
                if not self.game.stage.get_puyo(self.grid_x, self.grid_y + 1) \
                        and not self.game.stage.get_puyo(self.grid_x + self.grid_dx, self.grid_y + self.grid_dy + 1):
                    self.grounded_frames = 0
                    return True
                else:
                    self.top = self.grid_y * TILE_SIZE
                    self.grounded_frames = 1
                    return True
            # 自由落下でマス目の境界を超えていない場合、接地していないので自由落下を継続
            else:
                self.grounded_frames = 0
                return True
        # 操作ぷよの下にぷよがある場合
        else:
            if self.grounded_frames == 0:
                self.grounded_frames = 1
                return True
            else:
                self.grounded_frames += 1
                if self.grounded_frames > LOCK_GROUNDED_FRAMES:
                    return False
                return True

    def _set_puyo_pos(self):
        rx = self.left + math.sin(self.rotation * math.pi / 180) * TILE_SIZE
        ry = self.top - math.cos(self.rotation * math.pi / 180) * TILE_SIZE

        self.center_puyo.pos = [self.left, self.top]
        self.rotated_puyo.pos = [rx, ry]

    def fix(self):
        # 中心ぷよを固定
        if self.grid_y >= 0:
            self.game.stage.set_puyo(self.grid_x, self.grid_y, self.center_puyo)
        # 回転ぷよを固定
        if self.grid_y + self.grid_dy >= 0:
            self.game.stage.set_puyo(self.grid_x + self.grid_dx, self.grid_y + self.grid_dy, self.rotated_puyo)

    def render(self, surface):
        if self.center_puyo:
            self.center_puyo.render(surface)
        if self.rotated_puyo:
            self.rotated_puyo.render(surface)

    def update(self):
        is_auto_fall = self._auto_fall()
        if not is_auto_fall:
            return PlayerState.FIX

        self._set_puyo_pos()
        return PlayerState.PLAYING
