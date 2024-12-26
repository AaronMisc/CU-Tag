import pygame
from sys import exit
from pygame.math import Vector2 as vector

WINDOW_WIDTH, WINDOW_HEIGHT = 640, 480
TILE_SIZE = 32

keybinds_normal = {
    "Player1": [pygame.K_w, pygame.K_a, pygame.K_d],
    "Player2": [pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT],
    "Player3": [pygame.K_t, pygame.K_f, pygame.K_h],
    "Player4": [pygame.K_i, pygame.K_j, pygame.K_l]
}