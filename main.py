import pygame
import sys
from scripts.settings import *
from scripts.stage import Stage
from scripts.player import Player, PlayerState
from scripts.utils import load_image
from enum import Enum, auto


class GameState(Enum):
    START = auto()  # ゲームスタート
    CHECK_FALL_PUYO = auto()    # 落下ぷよのチェック
    FALL_PUYO = auto()  # ぷよの落下
    CHECK_ERASE_PUYO = auto()   # 消えるぷよのチェック
    ERASE_PUYO = auto()     # ぷよの消去
    CREATE_PLAYER_PUYO = auto() # 操作ぷよの作成
    PLAYING = auto()    # ぷよの操作
    FIX = auto()    # ぷよの固定
    GAME_OVER = auto()  # ゲームオーバー


class Game:

    def __init__(self):
        pygame.init()

        # ウィンドウの設定
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("ぷよぷよ")

        # FPSの設定
        self.clock = pygame.time.Clock()

        # ゲームの状態
        self.game_state = GameState.START

        # ぷよの一覧
        self.puyo_keys = ["blue_puyo", "green_puyo", "purple_puyo", "red_puyo", "yellow_puyo"]

        # アセット
        self.assets = {
            "blue_puyo": load_image("assets/img/blue_puyo.png", size=(TILE_SIZE, TILE_SIZE)),
            "green_puyo": load_image("assets/img/green_puyo.png", size=(TILE_SIZE, TILE_SIZE)),
            "purple_puyo": load_image("assets/img/purple_puyo.png", size=(TILE_SIZE, TILE_SIZE)),
            "red_puyo": load_image("assets/img/red_puyo.png", size=(TILE_SIZE, TILE_SIZE)),
            "yellow_puyo": load_image("assets/img/yellow_puyo.png", size=(TILE_SIZE, TILE_SIZE)),
        }

        # 入力
        self.inputs = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
        }

        # 盤面
        self.stage = Stage(self)

        # プレイヤー操作ぷよ
        self.player = Player(self)

    def run(self):
        while True:

            # 背景の塗りつぶし
            self.screen.fill(COLORS["black"])

            # ステージの描画
            self.stage.render(self.screen)

            # プレイヤー操作ぷよの描画
            self.player.render(self.screen)

            # ゲームの状態遷移
            match self.game_state:
                # ゲーム開始
                case GameState.START:
                    self.game_state = GameState.CHECK_FALL_PUYO
                # 落下ぷよのチェック
                case GameState.CHECK_FALL_PUYO:
                    is_exist_falling_puyo = self.stage.check_falling_puyo()
                    # 落下対象のぷよが存在する場合
                    if is_exist_falling_puyo:
                        self.game_state = GameState.FALL_PUYO
                    else:
                        self.game_state = GameState.CHECK_ERASE_PUYO
                # ぷよの落下
                case GameState.FALL_PUYO:
                    is_falling = self.stage.fall_puyo()
                    # ぷよの落下が終了した場合
                    if not is_falling:
                        self.game_state = GameState.CHECK_ERASE_PUYO
                # 消去ぷよのチェック
                case GameState.CHECK_ERASE_PUYO:
                    is_exist_erasing_puyo = self.stage.check_erasing_puyo()
                    if is_exist_erasing_puyo:
                        self.game_state = GameState.ERASE_PUYO
                    else:
                        self.game_state = GameState.CREATE_PLAYER_PUYO
                # ぷよの消去
                case GameState.ERASE_PUYO:
                    is_erasing = self.stage.erase_puyo()
                    # ぷよの消去が終了した場合
                    if not is_erasing:
                        self.game_state = GameState.CHECK_FALL_PUYO
                # ぷよの作成
                case GameState.CREATE_PLAYER_PUYO:
                    is_created_puyo = self.player.create_puyo()
                    if is_created_puyo:
                        self.game_state = GameState.PLAYING
                    else:
                        self.game_state = GameState.GAME_OVER
                # ぷよの操作
                case GameState.PLAYING:
                    next_player_state = self.player.update()
                    match next_player_state:
                        case PlayerState.PLAYING:
                            self.game_state = GameState.PLAYING
                        case PlayerState.FIX:
                            self.game_state = GameState.FIX
                # ぷよの固定
                case GameState.FIX:
                    self.player.fix()
                    self.game_state = GameState.CHECK_FALL_PUYO

            # イベントの取得
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # キーボード押下
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_UP:
                        self.inputs["up"] = True
                    if event.key == pygame.K_DOWN:
                        self.inputs["down"] = True
                    if event.key == pygame.K_LEFT:
                        self.inputs["left"] = True
                    if event.key == pygame.K_RIGHT:
                        self.inputs["right"] = True
                # キーボード押下
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.inputs["up"] = False
                    if event.key == pygame.K_DOWN:
                        self.inputs["down"] = False
                    if event.key == pygame.K_LEFT:
                        self.inputs["left"] = False
                    if event.key == pygame.K_RIGHT:
                        self.inputs["right"] = False

            # 更新
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
