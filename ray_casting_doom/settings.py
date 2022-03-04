import math


# screen settings
class ScreenConfig:
    WIDTH = 1200
    HEIGHT = 800
    HALF_WIDTH = WIDTH // 2
    HALF_HEIGHT = HEIGHT // 2
    FPS_60 = 60
    TILE = 100
    FPS_POSITION = WIDTH - 65, 5


class MinimapConfig:
    SCALE = 5
    TILE = ScreenConfig.TILE // SCALE
    WIDTH = ScreenConfig.WIDTH // SCALE
    HEIGHT = ScreenConfig.HEIGHT // SCALE
    POSITION = (0, ScreenConfig.HEIGHT - ScreenConfig.HEIGHT // SCALE)


# ray casting settings
class RayCastingConfig:
    FOV = math.pi / 3
    HALF_FOV = FOV / 2
    NUM_RAYS = 300
    MAX_DEPTH = 800
    DELTA_ANGLE = FOV / NUM_RAYS
    DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
    PROJ_COEF = 3 * DIST * ScreenConfig.TILE
    SCALE = ScreenConfig.WIDTH / NUM_RAYS
    colored = False


class TextureConfig:
    PATH = 'textures'
    WIDTH = 1200
    HEIGHT = 1200
    SCALE = WIDTH // ScreenConfig.TILE


class SpritesConfig:
    PATH = 'sprites'
    DOUBLE_PI = 2 * math.pi
    CENTER_RAY = RayCastingConfig.NUM_RAYS // 2 - 1
    FAKE_RAYS = 100


# player settings
class PlayerConfig:
    player_pos = (ScreenConfig.HALF_WIDTH // 4, ScreenConfig.HALF_HEIGHT - 50)
    player_angle  = 0
    player_speed = 2


# colors settings
class ColorRGB:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (220, 0, 0)
    GREEN = (0, 220, 0)
    BLUE = (0, 0, 220)
    DARK_GRAY = (40, 40, 40)
    PURPLE = (120, 0, 120)
    DARK_GREEN = (0, 100, 0)
    SKY_BLUE = (0, 186, 255)
    DARK_BROWN = (97, 61, 25)
    DARK_ORANGE = (255, 140, 0)
