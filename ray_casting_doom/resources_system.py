import os
import pygame

from settings import *


def collect_textures(texture_dir):
    textures_dict = {}
    for file in os.listdir(texture_dir):
        path = os.path.join(texture_dir, file)
        if os.path.isfile(path):
            textures_dict[f'{file}'] = pygame.image.load(path).convert()
    return textures_dict


def collect_sprites(sprite_dir):
    sprite_types = {
        'barrel': pygame.image.load('sprites/barrel/0.png').convert_alpha(),
        'pedestal': pygame.image.load('sprites/pedestal/0.png').convert_alpha(),
    }
    return sprite_types

