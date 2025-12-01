# ぷよの設定
TILE_SIZE = 60
STAGE_COL_NUM = 6
STAGE_ROW_NUM = 12

# ウィンドウの設定
SCREEN_WIDTH = TILE_SIZE * STAGE_COL_NUM
SCREEN_HEIGHT = TILE_SIZE * STAGE_ROW_NUM

# FPSの設定
FPS = 60

# 色の設定
COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "line_color": (50, 50, 50),
}

# ぷよの落下スピード
FALLING_SPEED = 6

# ぷよを消す連結数
ERASING_PUYO_COUNT = 4

# ぷよ削除のフレーム数
ERASING_PUYO_FRAMES = 30

# 操作ぷよの落下スピード
PLAYER_FALLING_SPEED = 5

# ぷよを固定する接地フレーム
LOCK_GROUNDED_FRAMES = 20
