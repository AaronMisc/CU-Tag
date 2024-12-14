from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, keybinds):
        super().__init__(groups)

        self.image = pygame.surface.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill("red")

        # Rects
        pos = (300, 10)
        self.rect = self.image.get_frect(center = pos)
        self.old_rect = self.rect.copy()

        self.keybinds = keybinds

        # Movement
        self.direction = vector()
        self.speed = 200
        self.gravity = 1200

        # Collision
        self.collision_sprites = collision_sprites

    
    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0, 0)
        if keys[self.keybinds[0]]:
            input_vector.y -= 1
        if keys[self.keybinds[1]]:
            input_vector.x -= 1
        if keys[self.keybinds[2]]:
            input_vector.x += 1
        self.direction.x = input_vector.normalize().x if input_vector else 0

    def move(self, dt):
        # Horizontal
        self.rect.x += self.direction.x * self.speed * dt
        self.collision("x")

        # Vertical
        self.direction.y += self.gravity / 2 * dt
        self.rect.y += self.direction.y * dt
        self.direction.y += self.gravity / 2 * dt
        self.collision("y")

    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == "x":
                    # Left
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right

                    # Right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left

                elif axis == "y":
                    # Top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom

                    # Bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top

                    self.direction.y = 0

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)
