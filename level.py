from settings import *
from sprites import *

class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()

        # Groups
        self.all_sprites = pygame.sprite.Group()
        
        self.setup(tmx_map)
    
    def setup(self, tmx_map):
        for x, y, surf, in tmx_map.get_layer_by_name("Platforms").tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)
        
        for obj in tmx_map.get_layer_by_name("Objects").tiles():
            if obj.name == "player1":
                pass

    def run(self):
        self.display_surface.fill("black")
        self.all_sprites.draw(self.display_surface)