import pygame
from settings import *
from ray_casting import ray_cast_texture, ray_cast_color
from map import world_map
from resources_system import collect_textures



class Render:
    def __init__(self, sc):
        self.sc = sc
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.textures = collect_textures(TextureConfig.PATH)
        print(self.textures)

    def multiresolution_rays(self):
        pass
        # TODO
        """
        Сделал фитчу, которая подстраивает колличество лучей под производительность. 
        Если движок рисует кадр за 1 \ FPS, то num_rays добавляю - и картинка становится четче.
        Если не успевает - отнимает num_rays, и картинка становится калькуляторнее.
        """

    def draw_sky(self, player_angle):
        # Drawing sky and earth
        sky_offset = -10 * math.degrees(player_angle) % ScreenConfig.WIDTH
        self.sc.blit(self.textures['sky3.png'], (sky_offset, 0))
        self.sc.blit(self.textures['sky3.png'], (sky_offset - ScreenConfig.WIDTH, 0))
        self.sc.blit(self.textures['sky3.png'], (sky_offset + ScreenConfig.WIDTH, 0))

    def draw_earth(self):
        pygame.draw.rect(self.sc, ColorRGB.DARK_GRAY,
                         (0, ScreenConfig.HALF_HEIGHT, ScreenConfig.WIDTH, ScreenConfig.HALF_HEIGHT))

    def draw_world(self, player_pos, player_angle, texture_is_enabled=True):
        if texture_is_enabled:
            ray_cast_texture(self.sc, player_pos, player_angle, self.textures)
        else:
            ray_cast_color(self.sc, player_pos, player_angle)

    def draw_world_2d(self, player_pos, player):
        # TODO Заимлементить отображение FOV 2d мире с помощью raycast функции
        self.sc.fill(ColorRGB.DARK_GRAY)
        pygame.draw.circle(self.sc, ColorRGB.GREEN, player_pos, 12)
        pygame.draw.line(self.sc, ColorRGB.GREEN, player_pos,
                        (
                            player.x + ScreenConfig.WIDTH * math.cos(player.angle),
                            player.y + ScreenConfig.WIDTH * math.sin(player.angle)
                        ),
                        )
        for x,y in world_map:
           pygame.draw.rect(self.sc, ColorRGB.RED, (x, y, ScreenConfig.TILE, ScreenConfig.TILE), 0)


    def show_fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render_font = self.font.render(display_fps, 0, ColorRGB.GREEN)
        self.sc.blit(render_font, (ScreenConfig.FPS_POSITION))

    def show_minimap(self, sc_mini_map, player):
        sc_mini_map.fill(ColorRGB.BLACK)
        map_x, map_y = player.x // MinimapConfig.SCALE, player.y // MinimapConfig.SCALE
        pygame.draw.circle(sc_mini_map, ColorRGB.GREEN, (int(map_x), int(map_y)), 5)
        pygame.draw.line(sc_mini_map, ColorRGB.GREEN, (map_x, map_y),
                         (
                             map_x + 12 * math.cos(player.angle),
                             map_y + 12 * math.sin(player.angle)
                         ),
                         2,
                         )
        for x, y in world_map:
            pygame.draw.rect(sc_mini_map, ColorRGB.DARK_BROWN, (x // MinimapConfig.SCALE, y // MinimapConfig.SCALE, MinimapConfig.TILE, MinimapConfig.TILE), 0)
        self.sc.blit(sc_mini_map, MinimapConfig.POSITION)
