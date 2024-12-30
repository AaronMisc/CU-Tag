from settings import *
from text_base import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surface):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(center = pos)
        self.old_rect = self.rect.copy()