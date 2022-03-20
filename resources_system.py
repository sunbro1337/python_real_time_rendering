import os
import pygame

from settings import *


def convert_str_to_int(str: str) -> int:
    result = 0
    for char in str:
        result += int(hex(ord(char))[2:], base=16)
    return result


def collect_textures(texture_dir: str) -> dict:
    textures_dict = {}
    for file in os.listdir(texture_dir):
        path = os.path.join(texture_dir, file)
        if os.path.isfile(path):
            key = convert_str_to_int(file)
            textures_dict[key] = pygame.image.load(path).convert()
            print(f"Find texture: file={file}, key={key}, value={textures_dict[key]}")
    print(f"Textures: {textures_dict}")
    return textures_dict


def collect_sprites(sprite_dir: str) -> dict:
    pass
