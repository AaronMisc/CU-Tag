from settings import *
from sprites import *
from player import *
from pytimer import Timer

class Level:
    def __init__(self, tmx_map, offset = 16):
        self.offset = offset
        self.tag_cooldown_timer = Timer(game_settings["Tag cooldown"])

        self.display_surface = pygame.display.get_surface()

        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.semi_collidable_sprites = pygame.sprite.Group()
        self.border_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        
        self.setup(tmx_map)

    def setup(self, tmx_map):
        tmx_map_opening_settings = [
            ["Normal", (self.all_sprites, self.collision_sprites)],
            ["Semi", (self.all_sprites, self.semi_collidable_sprites)],
            ["Borders", (self.all_sprites, self.border_sprites, self.collision_sprites)]
        ]

        # Map setup
        for tmx_map_opening_setting in tmx_map_opening_settings:
            for x, y, surf in tmx_map.get_layer_by_name(tmx_map_opening_setting[0]).tiles():
                Sprite((x * TILE_SIZE + self.offset, y * TILE_SIZE + self.offset), tmx_map_opening_setting[1], surf)
        
        # Player setup
        for obj in tmx_map.get_layer_by_name("Objects"):
            if obj.name == "Player1" or obj.name == "Player2" or obj.name == "Player3" or obj.name == "Player4":
                Player((obj.x + self.offset, obj.y + self.offset), (self.all_sprites, self.player_sprites), {"normal": self.collision_sprites, "semi": self.semi_collidable_sprites, "borders": self.border_sprites}, keybinds_normal[obj.name], obj.image, obj.name)
        
        player_sprites_list = self.player_sprites.sprites()
        for player in player_sprites_list: # Updating player sprites
            excluside_player_sprites_list = player_sprites_list.copy()
            excluside_player_sprites_list.remove(player)
            player.player_sprites = excluside_player_sprites_list

            if player.name == "Player1":
                player.tag()

    def run(self, dt):
        self.player_sprites.update(dt)
        self.all_sprites.draw(self.display_surface)