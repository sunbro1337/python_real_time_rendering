from contexts.maps_context import Maps
from contexts.player_context import Player
from contexts.render_context import Render
from contexts.sprite_context import *
from systems.ray_casting import texture_walls
from configs.global_settings import *


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    sc = pygame.display.set_mode((ScreenConfig.WIDTH, ScreenConfig.HEIGHT))
    sc_mini_map = pygame.Surface(MapConfig.MINIMAP_RESOLUTION)

    sprites = Sprites()
    maps = Maps()
    maps.create_maps()
    player = Player(PlayerConfig.player_pos, PlayerConfig.player_angle, PlayerConfig.player_speed, sprites, maps.collision_walls)
    render = Render(sc)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                
        player.move()

        #sc.fill(ColorRGB.BLACK)
        render.draw_sky(PlayerConfig.player_angle)
        render.draw_earth()
        walls = texture_walls(player, render.textures, maps.world_map, maps.WORLD_WIDTH, maps.WORLD_HEIGHT)
        render.draw_world(walls + [obj.object_locate(player, walls) for obj in sprites.list_of_objects])
        render.show_fps(clock)
        render.show_minimap(sc_mini_map, player, maps.world_map)

        pygame.display.flip()
        clock.tick(ScreenConfig.FPS_60)
