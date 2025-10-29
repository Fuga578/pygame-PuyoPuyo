import pygame
import sys
from scripts.settings import *
from scripts.stage import Stage
from scripts.utils import load_image


class Game:

    def __init__(self):
        pygame.init()

        # ウィンドウの設定
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("ぷよぷよ")

        # FPSの設定
        self.clock = pygame.time.Clock()

        # 盤面
        self.stage = Stage(self)

        # ぷよの一覧
        self.puyo_list = ["blue_puyo", "green_puyo", "purple_puyo", "red_puyo", "yellow_puyo"]

        # アセット
        self.assets = {
            "blue_puyo": load_image("assets/img/blue_puyo.png", size=(TILE_SIZE, TILE_SIZE)),
            "green_puyo": load_image("assets/img/green_puyo.png", size=(TILE_SIZE, TILE_SIZE)),
            "purple_puyo": load_image("assets/img/purple_puyo.png", size=(TILE_SIZE, TILE_SIZE)),
            "red_puyo": load_image("assets/img/red_puyo.png", size=(TILE_SIZE, TILE_SIZE)),
            "yellow_puyo": load_image("assets/img/yellow_puyo.png", size=(TILE_SIZE, TILE_SIZE)),
        }

    def run(self):
        while True:

            # 背景の塗りつぶし
            self.screen.fill(COLORS["black"])

            # ステージの描画
            self.stage.render(self.screen)

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

            # 更新
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
