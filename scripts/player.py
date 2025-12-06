import pygame
import random
import math
from scripts.settings import *
from scripts.puyo import Puyo
from enum import Enum, auto


class PlayerState(Enum):
    PLAYING = auto()
    FIX = auto()
    MOVE = auto()
    ROTATE = auto()


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

        self.move_source_x = 0
        self.move_dest_x = 0
        self.moving_frame = 0

        self.left_before_rotate = 0
        self.left_after_rotate = 0
        self.rotation_before_rotate = 0
        self.rotating_frame = 0

        self.is_right_rotation = False

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
        self.rotation = 270

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

    def _fall(self):
        # 操作ぷよの下にぷよがない場合
        if not self.game.stage.get_puyo(self.grid_x, self.grid_y + 1) \
                and not self.game.stage.get_puyo(self.grid_x + self.grid_dx, self.grid_y + self.grid_dy + 1):
            self.top += PLAYER_FALLING_SPEED    # 自由落下
            if self.game.inputs["down"]:
                self.top += PLAYER_DOWN_SPEED
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
        rx = self.left + math.cos(self.rotation * math.pi / 180) * TILE_SIZE
        ry = self.top + math.sin(self.rotation * math.pi / 180) * TILE_SIZE

        self.center_puyo.pos = [self.left, self.top]
        self.center_puyo.grid_pos = [self.grid_x, self.grid_y]
        self.rotated_puyo.pos = [rx, ry]
        self.rotated_puyo.grid_pos = [self.grid_x + self.grid_dx, self.grid_y + self.grid_dy]

    def fix(self):
        # 中心ぷよを固定
        if self.grid_y >= 0:
            self.game.stage.set_puyo(self.grid_x, self.grid_y, self.center_puyo)
        # 回転ぷよを固定
        if self.grid_y + self.grid_dy >= 0:
            self.game.stage.set_puyo(self.grid_x + self.grid_dx, self.grid_y + self.grid_dy, self.rotated_puyo)

    def _check_move(self):
        can_move = True
        if self.game.inputs["left"] or self.game.inputs["right"]:
            # 左右の確認
            dx = -1 if self.game.inputs["left"] else 1
            # 中心ぷよ
            if self.game.stage.get_puyo(self.grid_x + dx, self.grid_y):
                can_move = False
            # 回転ぷよ
            if self.game.stage.get_puyo(self.grid_x + self.grid_dx + dx, self.grid_y + self.grid_dy):
                can_move = False

            # 接地していない場合、さらに1つ下の左右を確認
            if self.grounded_frames == 0:
                # 中心ぷよ
                if self.game.stage.get_puyo(self.grid_x + dx, self.grid_y + 1):
                    can_move = False
                # 回転ぷよ
                if self.game.stage.get_puyo(self.grid_x + self.grid_dx + dx, self.grid_y + self.grid_dy + 1):
                    can_move = False

            if can_move:
                self.move_source_x = self.grid_x * TILE_SIZE
                self.move_dest_x = (self.grid_x + dx) * TILE_SIZE

                self.grid_x += dx

        return can_move

    def move(self):
        # 左右移動中も自由落下
        self._fall()

        frames_ratio = self.moving_frame / PLAYER_MOVE_FRAMES
        frames_ratio = min(frames_ratio, 1)

        self.left = (self.move_dest_x - self.move_source_x) * frames_ratio + self.move_source_x
        self._set_puyo_pos()

        self.moving_frame += 1

        # 移動終了判定
        is_moving = True
        if frames_ratio == 1:
            is_moving = False
            self.moving_frame = 0

        return is_moving

    def _check_rotate(self):
        can_rotate = True

        if self.game.inputs["a"] or self.game.inputs["d"]:
            self.is_right_rotation = False if self.game.inputs["a"] else True

            grid_x = self.grid_x
            grid_y = self.grid_y + (1 if self.grounded_frames == 0 else 0)  # 落下中の場合、1つ下をみる

            grid_dx = 0
            grid_dy = 0

            # 右回転をチェック
            if self.is_right_rotation:
                if self.rotation == 0:  # 右 -> 下
                    # 下 or 右下にぷよがあれば上に移動
                    if self.game.stage.get_puyo(grid_x, grid_y + 1) or self.game.stage.get_puyo(grid_x + 1, grid_y + 1):
                        grid_dy = -1
                elif self.rotation == 90:   # 下 -> 左
                    # 左にぷよがあれば右に移動
                    if self.game.stage.get_puyo(grid_x - 1, grid_y):
                        grid_dx = 1
                        # 右にもぷよがある場合は移動できない
                        if self.game.stage.get_puyo(grid_x + 1, grid_y):
                            can_rotate = False
                elif self.rotation == 180:  # 左 -> 上
                    # 何もしない
                    pass
                elif self.rotation == 270:  # 上 -> 右
                    # 右にぷよがあれば左に移動
                    if self.game.stage.get_puyo(grid_x + 1, grid_y):
                        grid_dx = -1
                        # 左にもぷよがある場合は移動できない
                        if self.game.stage.get_puyo(grid_x - 1, grid_y):
                            can_rotate = False
            # 左回転をチェック
            else:
                if self.rotation == 0:  # 右 -> 上
                    # 何もしない
                    pass
                elif self.rotation == 270:  # 上 -> 左
                    # 左にぷよがあれば右に移動
                    if self.game.stage.get_puyo(grid_x - 1, grid_y):
                        grid_dx = 1
                        # 右にもぷよがある場合は移動できない
                        if self.game.stage.get_puyo(grid_x + 1, grid_y):
                            can_rotate = False
                elif self.rotation == 180:  # 左 -> 下
                    # 下 or 左下にぷよがあれば上に移動
                    if self.game.stage.get_puyo(grid_x, grid_y + 1) or self.game.stage.get_puyo(grid_x - 1, grid_y + 1):
                        grid_dy = -1
                elif self.rotation == 90:  # 下 -> 右
                    # 右にぷよがあれば左に移動
                    if self.game.stage.get_puyo(grid_x + 1, grid_y):
                        grid_dx = -1
                        # 左にもぷよがある場合は移動できない
                        if self.game.stage.get_puyo(grid_x - 1, grid_y):
                            can_rotate = False

            if can_rotate:
                # 上に移動時のみ一気にあげる
                if grid_dy == -1:
                    # 設置している場合1段上に移動
                    if self.grounded_frames > 0:
                        self.grid_y += grid_dy
                        self.grounded_frames = 0
                    self.top = self.grid_y * TILE_SIZE

                # 回転前後の情報をセット
                self.left_before_rotate = grid_x * TILE_SIZE
                self.left_after_rotate = (grid_x + grid_dx) * TILE_SIZE
                self.rotation_before_rotate = self.rotation

                # 次の状態をセット
                self.grid_x += grid_dx
                if self.is_right_rotation:
                    next_rotation = int((self.rotation + 90) % 360)
                else:
                    next_rotation = int((self.rotation - 90) % 360)
                vecs = {
                    0: (1, 0),  # 右
                    90: (0, 1),  # 下
                    180: (-1, 0),  # 左
                    270: (0, -1),  # 上
                }
                self.grid_dx, self.grid_dy = vecs[next_rotation]

        return can_rotate

    def rotate(self):
        # 回転中も自由落下
        self._fall()

        frames_ratio = self.rotating_frame / PLAYER_ROTATE_FRAMES
        frames_ratio = min(frames_ratio, 1)

        self.left = (self.left_after_rotate - self.left_before_rotate) * frames_ratio + self.left_before_rotate
        if self.is_right_rotation:
            self.rotation = (self.rotation_before_rotate + frames_ratio * 90) % 360
        else:
            self.rotation = (self.rotation_before_rotate - frames_ratio * 90) % 360
        self._set_puyo_pos()

        self.rotating_frame += 1

        # 回転終了判定
        is_rotating = True
        if frames_ratio == 1:
            is_rotating = False
            self.rotating_frame = 0

        return is_rotating

    def render(self, surface):
        if self.center_puyo:
            self.center_puyo.render(surface)
        if self.rotated_puyo:
            self.rotated_puyo.render(surface)

    def update(self):
        is_fall = self._fall()
        if not is_fall:
            return PlayerState.FIX
        self._set_puyo_pos()

        if self.game.inputs["left"] or self.game.inputs["right"]:
            can_move = self._check_move()
            if can_move:
                return PlayerState.MOVE
        elif self.game.inputs["a"] or self.game.inputs["d"]:
            can_rotate = self._check_rotate()
            if can_rotate:
                return PlayerState.ROTATE

        return PlayerState.PLAYING
