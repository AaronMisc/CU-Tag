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

keybinds = {
    "normal": {
        "Player1": [pygame.K_w, pygame.K_a, pygame.K_d, pygame.K_s],
        "Player2": [pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN],
        "Player3": [pygame.K_t, pygame.K_f, pygame.K_h, pygame.K_g],
        "Player4": [pygame.K_i, pygame.K_j, pygame.K_l, pygame.K_k]
    },
    "compact": {
        "Player1": [pygame.K_2, pygame.K_q, pygame.K_e, pygame.K_w],
        "Player2": [pygame.K_s, pygame.K_z, pygame.K_c, pygame.K_x],
        "Player3": [pygame.K_5, pygame.K_r, pygame.K_y, pygame.K_t],
        "Player4": [pygame.K_g, pygame.K_v, pygame.K_n, pygame.K_b],
        "Player5": [pygame.K_8, pygame.K_u, pygame.K_o, pygame.K_i],
        "Player6": [pygame.K_k, pygame.K_m, pygame.K_PERIOD, pygame.K_COMMA],
        "Player7": [pygame.K_MINUS, pygame.K_p, pygame.K_RIGHTBRACKET, pygame.K_LEFTBRACKET],
        "Player8": [pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN]
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

text_settings = {
    "Label player names": [True, "Label the player names above players. Toggle with F2."],
    "Label player keybinds": [True, "Label the keybinds above players. Toggle with F4."],
    "Label player tag times": [True, "Label the player names above the player. Toggle with F5."],
    "Show player list": [True, "Show the player tag times in the top left. Toggle with F1."],
    "Show player stats": [False, "Show player stats on the top. Toggle with F1."]
}
movement_settings = {
    "Player speed": [200, "How fast the non-tagged player(s) move (left and right)."],
    "Tagged player speed": [300, "How fast the tagged player(s) move (left and right)."],
    "Player jump height": [600, "How high the players jump. Not linear."],
    "Tagged player jump height": [600, "How high the tagged player(s) jumps."],
    "Player gravity": [1200, "Gravity amount affecting the players."],
    "Tagged player gravity": [1200, "Gravity amount affect the tagged player(s)"],
    "Wall sliding allowed": [True, "Make the players fall slower when touching a wall."],
    "Wall jumping": [True, "Allows the players to jump when touching a wall."],
    "Wall detection lenience": [2, "How close you have to be to the ball for wall sliding and jumping."]
}
game_settings = {
    "Player amount": [2, "How many players are in the game."],
    "Keybind type": ["Normal", "What set of keybinds to use. Normal is confortable, up to 4 players. Compact is tight, up to 8 players. Max is black-hole enducing, with each player getting 3 keys, pressing all keys makes them go down, (suggested) for multiple keyboards."],
    "Game mode": ["Endless", "Endless will never end. Countdown ends after the tag time of a player reaches 0. Tags ends after a player gets tagged to much. Claim is when all players get tagged, you can't get un-tagged. Multi allows multiple players to get tagged and is endless."],
    "Tag time": [120000, "A timer the ticks when a player can tag others (after the tag cooldown). Can be used to end the game, depending on the game mode."],
    "Tag cooldown": [3000, "How long the tagged player(s) can't tag for after just being tagged. In milliseconds."],
    "Map": [1, "Which map to use. It is recommended to use the map selector."]
}
advanced_settings = {
    "Semi collision rect height": [8, "The height of the semi collision rect. The higher this is, the further semis will be detected. This makes it less buggy but also causes unexpected falling."],
    "Wall slide rect width": [2, "The width of the wall slide rect. The higher this is, the further you can be away from the wall to wall slide."],
    "Jump rect height": [2, "The height of the jump rect. How many pixels you have to be away from the ground to jump."],
    "Wall slide speed modifier": [0.8, "The multiplication of gravity when wall sliding. 1 means the same as gravity."],
}

tag_cooldown_end = 0
tag_time_colours = {
    3: colours["red"],
    2: colours["yellow"],
    1: colours["green"],
}