import pygame
import sys
from scripts.settings import *


class Game:

    def __init__(self):
        pygame.init()

        # ウィンドウの設定
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("ぷよぷよ")

        # FPSの設定
        self.clock = pygame.time.Clock()

    def run(self):
        while True:

            # 背景の塗りつぶし
            self.screen.fill(COLORS["black"])

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
