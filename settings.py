import pygame
from sys import exit
from pygame.math import Vector2 as vector
from math import ceil
from os.path import join
from random import choice

file_pre_path = ""
try:
    pygame.image.load(join("Images", "Player1.png"))
except:
    file_pre_path = "CU-Tag"

def convert_filename(path:list):
    if file_pre_path != "":
        path.insert(0, file_pre_path)
    return join(*path)

def keys_to_names(keys):
    return ", ".join(pygame.key.name(key) for key in keys)

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
front_surface = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA) # Surface at the front

colours = pygame.colordict.THECOLORS
pygame.font.init()
fonts = {
    "consolas": pygame.font.Font(convert_filename(["Fonts", "Consolas.ttf"]), 32),
    "consolas small": pygame.font.Font(convert_filename(["Fonts", "Consolas.ttf"]), 16),
    "consolas bold": pygame.font.Font(convert_filename(["Fonts", "Consolas-Bold.ttf"]), 48),
    "consolas bold small": pygame.font.Font(convert_filename(["Fonts", "Consolas-Bold.ttf"]), 24),
    "consolas title": pygame.font.Font(convert_filename(["Fonts", "Consolas-Bold.ttf"]), 128)
}

button_cooldown_end = 0
button_cooldown = 500

game_settings = {
    "Player speed": 200,
    "Tagged player speed": 300,
    "Player jump height": 600,
    "Tagged player jump height": 600,
    "Player gravity": 1200,
    "Tagged player gravity": 1200,
    "Tag cooldown": 3000
}
keybinds = {
    "normal": {
        "Player1": [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d],
        "Player2": [pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT],
        "Player3": [pygame.K_t, pygame.K_f, pygame.K_g, pygame.K_h],
        "Player4": [pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l]
    },
    "compact": {
        "Player1": [pygame.K_2, pygame.K_q, pygame.K_w, pygame.K_e],
        "Player2": [pygame.K_s, pygame.K_z, pygame.K_x, pygame.K_c],
        "Player3": [pygame.K_5, pygame.K_r, pygame.K_t, pygame.K_y],
        "Player4": [pygame.K_g, pygame.K_v, pygame.K_b, pygame.K_n],
        "Player5": [pygame.K_8, pygame.K_u, pygame.K_i, pygame.K_o],
        "Player6": [pygame.K_k, pygame.K_m, pygame.K_COMMA, pygame.K_PERIOD],
        "Player7": [pygame.K_MINUS, pygame.K_p, pygame.K_LEFTBRACKET, pygame.K_RIGHTBRACKET],
        "Player8": [pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT]
    },
    "max": {
        "Player1": [pygame.K_1, pygame.K_2, pygame.K_3],
        "Player2": [pygame.K_q, pygame.K_w, pygame.K_e],
        "Player3": [pygame.K_a, pygame.K_s, pygame.K_d],
        "Player4": [pygame.K_z, pygame.K_x, pygame.K_c],
        "Player5": [pygame.K_4, pygame.K_5, pygame.K_6],
        "Player6": [pygame.K_r, pygame.K_t, pygame.K_y],
        "Player7": [pygame.K_f, pygame.K_g, pygame.K_h],
        "Player8": [pygame.K_v, pygame.K_b, pygame.K_n],
        "Player9": [pygame.K_7, pygame.K_8, pygame.K_9],
        "Player10": [pygame.K_u, pygame.K_i, pygame.K_o],
        "Player11": [pygame.K_j, pygame.K_k, pygame.K_l],
        "Player12": [pygame.K_m, pygame.K_COMMA, pygame.K_PERIOD],
        "Player13": [pygame.K_0, pygame.K_MINUS, pygame.K_EQUALS],
        "Player14": [pygame.K_p, pygame.K_LEFTBRACKET, pygame.K_RIGHTBRACKET],
        "Player15": [pygame.K_RSHIFT, pygame.K_RETURN, pygame.K_BACKSLASH],
        "Player16": [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT]
    }
}

label_player_names = False
label_player_keybinds = False
label_player_tag_times = False
show_player_tag_times = True
show_stats = False

tag_cooldown_end = 0
tag_time_colours = {
    3: colours["red"],
    2: colours["yellow"],
    1: colours["green"],
}