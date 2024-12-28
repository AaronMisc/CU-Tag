from settings import *
from sprites import *
from player import *

class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()

        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.semi_collidable_sprites = pygame.sprite.Group()
        self.border_sprites = pygame.sprite.Group()
        
        self.setup(tmx_map)

    def setup(self, tmx_map):
        tmx_map_opening_settings = [
            ["Normal", (self.all_sprites, self.collision_sprites)],
            ["Semi", (self.all_sprites, self.semi_collidable_sprites)],
            ["Borders", (self.all_sprites, self.border_sprites, self.collision_sprites)]
        ]

        for tmx_map_opening_setting in tmx_map_opening_settings:
            for x, y, surf in tmx_map.get_layer_by_name(tmx_map_opening_setting[0]).tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, tmx_map_opening_setting[1])
        
        for obj in tmx_map.get_layer_by_name("Objects"):
            if obj.name == "Player1" or obj.name == "Player2" or obj.name == "Player3" or obj.name == "Player4":
                Player((obj.x, obj.y), self.all_sprites, {"normal": self.collision_sprites, "semi": self.semi_collidable_sprites, "borders": self.border_sprites}, keybinds_normal[obj.name], obj.image)

    def run(self, dt):
        self.display_surface.fill("black")
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.display_surface)