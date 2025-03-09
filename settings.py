import pygame
from sys import exit
from pygame.math import Vector2 as vector
from math import ceil
from os.path import join
from random import choice
from pytmx.util_pygame import load_pygame
import pygame_gui
from tabulate import tabulate
from pytimer import Timer

file_pre_path = ""
try:
    pygame.image.load(join("Images", "Player1.png"))
except:
    file_pre_path = "Leveldotpy"

def convert_filename(path:list):
    if file_pre_path != "":
        path.insert(0, file_pre_path)
    return join(*path)

def keys_to_names(keys):
    return ", ".join(pygame.key.name(key) for key in keys)

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
front_surface = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA) # Surface at the front

colours = pygame.colordict.THECOLORS
button_cooldown_end = 0
pygame.font.init()
fonts = {
    "consolas": pygame.font.Font(convert_filename(["Fonts", "Consolas.ttf"]), 32),
    "consolas medium": pygame.font.Font(convert_filename(["Fonts", "Consolas.ttf"]), 24),
    "consolas small": pygame.font.Font(convert_filename(["Fonts", "Consolas.ttf"]), 16),
    "consolas bold": pygame.font.Font(convert_filename(["Fonts", "Consolas-Bold.ttf"]), 48),
    "consolas bold medium": pygame.font.Font(convert_filename(["Fonts", "Consolas-Bold.ttf"]),36),
    "consolas bold small": pygame.font.Font(convert_filename(["Fonts", "Consolas-Bold.ttf"]), 24),
    "consolas title": pygame.font.Font(convert_filename(["Fonts", "Consolas-Bold.ttf"]), 96)
}

map_details = { # map_details[name][detail], detail 0 is nickname, 1 is description, 2 is tile size
    "A1": ["Simple map", "A simple map with straight platforms.\nGood layout for gameplay.\nHas normal and semi platforms.", 32],
    "T1": ["Playground", "An interesting map with many pots for players to go in.\nHas normal and semi platforms.\nHas stairs that have an interesting glitch.\nFuller layout.", 32],
    "T2": ["Dots", "Many small platforms.\nHas normal, semi and limit platforms.\nAn interesting map design but players can get stuck.\nGameplay is fun but a bit questionable.", 32]
}
map_names = [name for name in map_details.keys()]

keybinds = { # keybinds[collection][playerid][keyid], for normal and compact: keyid 0 is up, 1 is left, 2 is right, 3 is down; for max: keyid 0 is left, keyid 1 is up, keyid 2 is right
    "normal": {
        "Player1": [pygame.K_a, pygame.K_w, pygame.K_d, pygame.K_s],
        "Player2": [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN],
        "Player3": [pygame.K_f, pygame.K_t, pygame.K_h, pygame.K_g],
        "Player4": [pygame.K_j, pygame.K_i, pygame.K_l, pygame.K_k]
    },
    "compact": {
        "Player1": [pygame.K_q, pygame.K_2, pygame.K_e, pygame.K_w],
        "Player2": [pygame.K_z, pygame.K_s, pygame.K_c, pygame.K_x],
        "Player3": [pygame.K_r, pygame.K_5, pygame.K_y, pygame.K_t],
        "Player4": [pygame.K_v, pygame.K_g, pygame.K_n, pygame.K_b],
        "Player5": [pygame.K_u, pygame.K_8, pygame.K_o, pygame.K_i],
        "Player6": [pygame.K_m, pygame.K_k, pygame.K_PERIOD, pygame.K_COMMA],
        "Player7": [pygame.K_p, pygame.K_MINUS, pygame.K_RIGHTBRACKET, pygame.K_LEFTBRACKET],
        "Player8": [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN]
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

settings = { # settings[page][option][index], index 0 is value, 1 is description, 2 is type, 3 (for int and float) is min and max, 3 (for str) is possible option list, 4 is bool for wether it is a hard limit
    "Text": {
        "Label player names": [True, "Label the player names above players. Toggle with F2.", bool],
        "Label player keybinds": [True, "Label the keybinds above players. Toggle with F4.", bool],
        "Label player game ends": [True, "Label the player tage times above the player. Toggle with F5.", bool],
        "Show player list": [True, "Show the player game ends in the top left. Toggle with F1.", bool]
    },
    "Movement": {
        "Player speed": [200, "How fast the non-tagged player(s) move (left and right).", int, [20, 1000], False],
        "Tagged player speed": [300, "How fast the tagged player(s) move (left and right).", int, [20, 1000], False],
        "Player jump height": [600, "How high the players jump. Not linear.", int, [20, 2000], False],
        "Tagged player jump height": [600, "How high the tagged player(s) jumps.", int, [20, 2000], False],
        "Player gravity": [1200, "Gravity amount affecting the players.", int, [60, 8000], False],
        "Tagged player gravity": [1200, "Gravity amount affecting the tagged player(s). Suggested to be the same as normal players.", int, [60, 8000], False],
        "Wall sliding allowed": [True, "Make the players fall slower when touching a wall.", bool],
        "Wall jumping": [True, "Allows the players to jump when touching a wall.", bool],
    },
    "Game": {
        "Player amount": [16, "How many players are in the game.", int, [1, 16], True],
        "Keybind type": ["Normal", "What set of keybinds to use. Normal is confortable, up to 4 players. Compact is tight, up to 8 players. Max is black-hole enducing, with each player getting 3 keys, pressing all keys makes them go down, (suggested) for multiple keyboards.", str, ["Normal", "Compact", "Max"]],
        "Game mode": ["Countdown", "Endless will never end. Countdown ends after the game end of a player reaches 0. Tags ends after a player gets tagged to much. Claim is when all players get tagged, you can't get un-tagged. Multi allows multiple players to get tagged and is endless.", str, ["Endless", "Countdown", "Tags", "Claim", "Multi"]],
        "Game end": [120000, "For countdown: A timer the ticks when a player can tag others (after the tag cooldown). For tags: How many tags before the game ends. For endless, claim and multi: Only for display, doesn't do anything.", int, [0, 1000000], False],
        "Tag cooldown": [3000, "How long the tagged player(s) can't tag for after just being tagged. In milliseconds.", int, [0, 10000], False],
        "Map": ["A1", "Which map to use. It is recommended to use the map selector.", str, [name for name in map_names]]
    },
    "Advanced": {
        "Semi collision rect height": [8, "The height of the semi collision rect. The higher this is, the further semis will be detected. This makes it less buggy but also causes unexpected falling.", int, [1, 32], False],
        "Wall slide rect width": [2, "The width of the wall slide rect. The higher this is, the further you can be away from the wall to wall slide.", int, [0, 128], False],
        "Jump rect height": [2, "The height of the jump rect. How many pixels you have to be away from the ground to jump.", int, [1, 128], False],
        "Wall jump modifier": [0.8, "The multiplication of jump height when wall jumping. 1 means the same as jump height.", float, [0, 1], True],
        "Wall slide speed modifier": [0.1, "The multiplication of gravity when wall sliding. 1 means the same as gravity.", float, [0, 1], True],
    },
    "Hidden": {
        "Game ended": False
    }
}
instructions_dict = {
    "Movement": "==MOVEMENT==\nEach players gets their own set of keybinds.\nPlayers can move left or right, phase or jump.\nPhasing makes the semi-colliable (yellow) platforms non-collidable.\nYou can jump through semi-collidable platforms.\nWall jump by jumping when touching a collidable platform on the left or right.\nWall slide by touching a collidable platform on the left or right.\n==GAME==\nPlayer1 starts tagged. The tagged player's goal is try to tag the other players.\nWhen you get tagged, there is a 3 second (can be changed) cooldown before you can tag others.\nTagged players will have numbers showing the time before the start, or the letter T if they can tag.\nTo tag, touch another player. If you are tagged, your game end will tick down.\nIf a player tags 2 player at the same time, it will tag the player who has a higher game end.\nIf they have the same time it will tag a random one.\n==KEYBINDS==\nIf a player has 4 keys, press the bottom middle key to go down.\nIf a player only has 3 keys, then press left and right at the same time to go down.\n==HOTKEYS==\nF1: Toggle showing player names, game ends and keys in top left.\nF2: Toggle labelling names above the players.\nF4: Toggle tabelling the keybinds above the players.\nF5: Toggle labelling the player game ends above the player.\nDELETE: Press 5 times to exit the game.\n==ENDING==\nThe game ends based on what is selected in settings.\nBy default the game ends when a player's game end reaches 0.",
    "Settings": "==USING SETTINGS==\nSelect the group on the top, then the option on the left.\nThe bottom text on the button will say the default (not the current amount) and a short description.\nOn the right, there will be the title, description and current setting.\nThere are many modes, use the buttons and text to change the settings.\n==NUMBERS AND LIMITS==\nWhen changing the numbers, sometimes there will be limits (you can tell because it says must).\nFor some there is no limit, which might cause potential errors.\n==DEBUG AND MENU==\nF3: Toggle showing FPS. This is not always precise.\nEsc: Go back to previous page.\nDELETE: Press 5 times to quit a game.",
    "Platforms": "White: Basic platform, can collide with, jump on, and doesn't change the player.\nYellow: Semi-collidable platform. You can jump through the bottom or sides.\nIt only has collision once you are above it. See the hotkeys and game to see how to phase through.\nGrey: Prevention platforms. Same as basic (white) but with no jumping or sliding.",
    "Keybinds": "==NORMAL==\nPlayer1: W A D S (jump, left, right, down)\nPlayer2: Up Left Right Down (arrows)\nPlayer3: T F H G\nPlayer4: I J L K\n==COMPACT==\nPlayer1: 2 Q E W (jump, left, right, down)\nPlayer2: S Z C X\nPlayer3: 5 R Y T\nPlayer4: G V N B\nPlayer5: 8 U O I\nPlayer6: K M . , (period and comma)\nPlayer7: - P ] [\nPlayer8: Up Left Right Down (arrows)\n==MAX==\nPlayer1: 1 2 3 Player2: Q W E\nPlayer3: A S D Player4: Z X C\nPlayer5: 4 5 6 Player6: R T Y\nPlayer7: F G H Player8: V B N\nPlayer9: 7 8 9 Player10: U I O\nPlayer11: J K L Player12: M , . (comma and period)\nPlayer13: 0 - = (equals) Player14: P [ ]\nPlayer15: RShift Return \\ (backslash) Player16: Left Up Right (arrows)",
    "Level editor": "Note: it is recommended to see a tutorial, but if you don't want to you can try understand this.\nOn the top right is the layers. The eye icon changes whether it's hidden.\nThe one highlighted in blue is the one selected.\nMake sure you are on the correct layer. The layer you place it on will determine the platform type.\nUnder the layers, those are the tilesets.\nAt the bottom of that there is an icon that will say New Tileset when hovered over.\nOpen the needed tilesets by clicking on the files.\nClick a tile in a tileset to start placing that.\nThey type of platform is detemined by layer, not by tile.\nOn the top are the tools. Press B to select the stamp brush to add tiles.\nPress E for the eraser. On the right are the rotate and mirror buttons.\nSave the file using Ctrl+S.\nOpening the game should show the files there."
}
credits_text = """==PROJECT==
Leveldotpy
Author: AaronMisc
Published on: 08/03/2025
Title: Leveldotpy
Respository link: https://github.com/AaronMisc/Leveldotpy/
Version: Alpha 1.0

==RESOURCES==
Fonts: Consolas. Luc(as) de Groot
Images made in: Pixilart. pixilart.com
Level editor: Tiled. www.mapeditor.org

==LANGUAGE AND LIBRARIES==
Python: Python software foundation. www.python.org
Pygame: Pete Shinners, Pygame Community. www.pygame.org
Pygame Community Edition: Pygame Community. https://pygame-ce.org/
PyTMX: Bitcraft. https://github.com/bitcraft/PyTMX
pygame_gui: MyreMylar. https://pygame-gui.readthedocs.io
Tabulate: Sergey Astanin. https://pypi.org/project/tabulate/

==SPECIAL THANKS==
ClearCode platformer tutorial
    Video: https://www.youtube.com/watch?v=WViyCAa6yLI
    Channel: https://www.youtube.com/@ClearCode
"""

tag_cooldown_end = 0
tag_time_colours = {
    3: colours["red"],
    2: colours["yellow"],
    1: colours["green"],
}