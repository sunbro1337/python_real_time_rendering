import math


# screen settings
class ScreenConfig:
    WIDTH = 1200
    HEIGHT = 800
    HALF_WIDTH = WIDTH // 2
    HALF_HEIGHT = HEIGHT // 2
    FPS_60 = 60
    TILE = 100


# ray casting settings
class RayCastingConfig:
    FOV = math.pi / 3
    HALF_FOV = FOV / 2
    NUM_RAYS = 120
    MAX_DEPTH = 800
    DELTA_ANGLE = FOV / NUM_RAYS
    DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
    PROJ_COEF = 3 * DIST * ScreenConfig.TILE
    SCALE = ScreenConfig.WIDTH / NUM_RAYS


# player settings
class PlayerConfig:
    player_pos = (ScreenConfig.HALF_WIDTH, ScreenConfig.HALF_HEIGHT)
    player_angle  = 0
    player_speed = 2


# colors settings
class ColorRGB:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (220, 0, 0)
    GREEN = (0, 220, 0)
    BLUE = (0, 0, 220)
    DARK_GRAY = (110, 110, 110)
    PURPLE = (120, 0, 120)
    DARK_GREEN = (0, 100, 0)
