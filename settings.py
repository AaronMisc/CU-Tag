import pygame
from sys import exit
from pygame.math import Vector2 as vector
from os.path import join

file_pre_path = ""
try:
    pygame.image.load(join("Images", "Player1.png"))
except:
    file_pre_path = "CU-Tag"

def convert_filename(path:list):
    if file_pre_path != "":
        path.insert(0, file_pre_path)
    return join(*path)

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TILE_SIZE = 32

keybinds_normal = {
    "Player1": [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d],
    "Player2": [pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT],
    "Player3": [pygame.K_t, pygame.K_f, pygame.K_g, pygame.K_h],
    "Player4": [pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l]
}

colours = pygame.colordict.THECOLORS

pygame.font.init()
fonts = {
    "consolas": pygame.font.Font(convert_filename(["Fonts", "Consolas.ttf"]), 32),
    "consolas small": pygame.font.Font(convert_filename(["Fonts", "Consolas.ttf"]), 16),
    "consolas bold": pygame.font.Font(convert_filename(["Fonts", "Consolas-Bold.ttf"]), 32),
    "consolas bold small": pygame.font.Font(convert_filename(["Fonts", "Consolas-Bold.ttf"]), 16)
}