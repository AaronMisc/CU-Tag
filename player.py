from settings import *
from pytimer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, keybinds, surface):
        super().__init__(groups)

        self.image = surface

        # Rects
        self.rect = self.image.get_frect(center = pos)
        self.old_rect = self.rect.copy()

        self.keybinds = keybinds

        # Movement
        self.direction = vector()
        self.speed = 200
        self.gravity = 1200
        self.is_jumping = False
        self.jump_height = 600

        # Collision
        self.collision_sprites = collision_sprites
        self.touching_sides = {
            "bottom": False,
            "left": False,  
            "right": False
        }

        # Timers
        self.timers = {
            "wall jump": Timer(200)
        }
    
    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0, 0)
        if keys[self.keybinds[0]]: # Jump
            self.is_jumping = True
        if not self.timers["wall jump"].active:
            if keys[self.keybinds[1]]: # Left
                input_vector.x -= 1
            if keys[self.keybinds[2]]: # Right
                input_vector.x += 1
        # self.direction.x = input_vector.normalize().x if input_vector else 0
        self.direction.x = input_vector.x

    def move(self, dt):
        if self.is_jumping:
            if self.touching_sides["bottom"]:
                self.direction.y = -self.jump_height
            elif any((self.touching_sides["left"], self.touching_sides["right"])):
                self.timers["wall jump"].start()
                self.direction.y = -self.jump_height * 0.8
                self.direction.x = 1 if self.touching_sides["left"] else -1
            self.is_jumping = False

        # Horizontal
        self.rect.x += self.direction.x * self.speed * dt
        self.collision("x")

        # Vertical
        if not self.touching_sides["bottom"] and any((self.touching_sides["left"], self.touching_sides["right"])) and self.direction.y >= 0:
            self.rect.y += self.gravity / 10 * dt
        else:
            self.direction.y += self.gravity / 2 * dt
            self.rect.y += self.direction.y * dt
            self.direction.y += self.gravity / 2 * dt
        self.collision("y")
    
    def check_contact(self):
        bottom_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        left_rect = pygame.Rect(self.rect.topleft + vector(-2, self.rect.height/4), (2, self.rect.height / 2))
        right_rect = pygame.Rect((self.rect.topright + vector(0, self.rect.height/4), (2, self.rect.height / 2)))
        collision_rects = [sprite.rect for sprite in self.collision_sprites]

        # Collisions
        self.touching_sides["bottom"] = True if bottom_rect.collidelist(collision_rects) >= 0 else False
        self.touching_sides["left"] = True if left_rect.collidelist(collision_rects) >= 0 else False
        self.touching_sides["right"] = True if right_rect.collidelist(collision_rects) >= 0 else False

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

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.update_timers()
        self.input()
        self.move(dt)
        self.check_contact()