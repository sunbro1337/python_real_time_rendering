import pygame
import math

from contexts.res_context import collect_textures


class Render:
    def __init__(self, sc, screen_config, map_config, texture_config):
        self.sc = sc
        self.screen_config = screen_config
        self.map_config = map_config
        self.texture_config = texture_config
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.textures = collect_textures(texture_config.PATH)

    def multiresolution_rays(self):
        pass
        # TODO
        """
        Сделал фитчу, которая подстраивает колличество лучей под производительность. 
        Если движок рисует кадр за 1 \ FPS, то num_rays добавляю - и картинка становится четче.
        Если не успевает - отнимает num_rays, и картинка становится калькуляторнее.
        """

    def draw_sky(self, player_angle):
        sky_offset = -10 * math.degrees(player_angle) % self.screen_config.WIDTH
        self.sc.blit(self.textures[765], (sky_offset, 0))
        self.sc.blit(self.textures[765], (sky_offset - self.screen_config.WIDTH, 0))
        self.sc.blit(self.textures[765], (sky_offset + self.screen_config.WIDTH, 0))

    def draw_earth(self, color):
        pygame.draw.rect(self.sc, color,
                         (0, self.screen_config.HALF_HEIGHT, self.screen_config.WIDTH, self.screen_config.HALF_HEIGHT))

    def draw_world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, obj, object_position = obj
                self.sc.blit(obj, object_position)

    def draw_world_2d(self, player_pos, player, world_map, player_color, bg_color, env_color):
        # TODO Заимлементить отображение FOV 2d мире с помощью raycast функции
        self.sc.fill(bg_color)
        pygame.draw.circle(self.sc, player_color, player_pos, 12)
        pygame.draw.line(self.sc, player_color, player_pos,
                        (
                            player.x + self.screen_config.WIDTH * math.cos(player.angle),
                            player.y + self.screen_config.WIDTH * math.sin(player.angle)
                        ),
                        )
        for x,y in world_map:
           pygame.draw.rect(self.sc, env_color, (x, y, self.screen_config.TILE, self.screen_config.TILE), 0)

    def show_fps(self, clock, text_color):
        display_fps = str(int(clock.get_fps()))
        render_font = self.font.render(display_fps, False, text_color)
        self.sc.blit(render_font, (self.screen_config.FPS_POSITION))

    def show_minimap(self, sc_mini_map, player, world_map, player_color, bg_color, env_color):
        sc_mini_map.fill(bg_color)
        map_x, map_y = player.x // self.map_config.MAP_SCALE, player.y // self.map_config.MAP_SCALE
        pygame.draw.circle(sc_mini_map, player_color, (int(map_x), int(map_y)), 5)
        pygame.draw.line(sc_mini_map, player_color, (map_x, map_y),
                         (
                             map_x + 12 * math.cos(player.angle),
                             map_y + 12 * math.sin(player.angle)
                         ),
                         2,
                         )
        for x, y in world_map:
            pygame.draw.rect(sc_mini_map, env_color, (x // self.map_config.MAP_SCALE, y // self.map_config.MAP_SCALE, self.map_config.TILE, self.map_config.TILE), 0)
        self.sc.blit(sc_mini_map, self.map_config.POSITION)
