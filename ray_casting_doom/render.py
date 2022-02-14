import pygame
from settings import *
from ray_casting import ray_cast



class Render:
    def __init__(self, sc):
        self.sc = sc
        self.font = pygame.font.SysFont('Arial', 36, bold=True)

    def draw_background(self):
        # Drawing sky and earth
        pygame.draw.rect(self.sc, ColorRGB.SKY_BLUE, (0, 0, ScreenConfig.WIDTH, ScreenConfig.HALF_HEIGHT))
        pygame.draw.rect(self.sc, ColorRGB.DARK_GREEN,
                         (0, ScreenConfig.HALF_HEIGHT, ScreenConfig.WIDTH, ScreenConfig.HALF_HEIGHT))

    def draw_world(self, plater_pos, player_angle):
        ray_cast(self.sc, plater_pos, player_angle)

    def show_fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render_font = self.font.render(display_fps, 0, ColorRGB.GREEN)
        self.sc.blit(render_font, (ScreenConfig.FPS_POSITION))