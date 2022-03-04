import os
import pygame

from settings import *


def collect_textures(texture_dir):
    textures_dict = {}
    for file in os.listdir(texture_dir):
        path = os.path.join(texture_dir, file)
        if os.path.isfile(path):
            textures_dict[f'{file}'] = pygame.image.load(path).convert()
    print(f"Textures: {textures_dict}")
    return textures_dict


def collect_sprites(sprite_dir):
    sprite_types = {}
    sprite_list = []
    for dir in os.listdir(sprite_dir):
        path_dir = os.path.join(sprite_dir, dir)
        if os.path.isdir(path_dir):
            for file in os.listdir(path_dir):
                path_file = os.path.join(path_dir, file)
                if os.path.isfile(path_file):
                    sprite_list.append(pygame.image.load(path_file).convert_alpha())
        sprite_types[f"{dir}"] = sprite_list
        sprite_list = []
    print(f"Sprites: {sprite_types}")
    return sprite_types
