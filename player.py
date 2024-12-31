from settings import *
from pytimer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, keybinds, surface):
        super().__init__(groups)

        # Rects
        self.image = surface
        self.rect = self.image.get_frect(center = pos)
        self.old_rect = self.rect.copy()

        # Movement
        self.direction = vector()
        self.speed = 200
        self.jump_height = 600
        self.gravity = 1200
        self.is_jumping = False

        # Collision
        self.border_sprites = collision_sprites["borders"]
        self.normal_collision_sprites = collision_sprites["normal"]
        self.normal_collision_rects = self.get_collision_rects(self.normal_collision_sprites)
        self.semi_collidable_sprites = collision_sprites["semi"]
        self.semi_collision_rects = [pygame.Rect((sprite.rect.x, sprite.rect.y), (sprite.rect.width, 1)) for sprite in self.semi_collidable_sprites]
        self.all_collision_sprites = pygame.sprite.Group(self.normal_collision_sprites.sprites() + self.semi_collidable_sprites.sprites())
        self.all_collision_rects = self.normal_collision_rects + self.semi_collision_rects

        self.touching_sides = {
            "bottom": False,
            "left": False,  
            "right": False,
            "semi": False 
        }

        # Others
        self.phasing_timer = Timer(300)

        self.keybinds = keybinds
        self.tagged = False
    
    def get_collision_rects(self, sprite_group):
        collision_rects = []
        for sprite in sprite_group:
            if sprite not in self.border_sprites:
                collision_rects.append(sprite.rect)
        return collision_rects

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0, 0)
        if keys[self.keybinds[0]]: # Jump
            self.is_jumping = True
        if keys[self.keybinds[1]]: # Left
            input_vector.x -= 1
        if keys[self.keybinds[3]]: # Right
            input_vector.x += 1
        if keys[self.keybinds[2]] and not self.is_jumping: # Down
            self.phasing_timer.start()

        self.direction.x = input_vector.normalize().x if input_vector else 0

    def move(self, dt):
        if self.is_jumping:
            if self.touching_sides["bottom"]:
                self.direction.y = -self.jump_height
            elif any((self.touching_sides["left"], self.touching_sides["right"])):
                self.direction.y = -self.jump_height * 0.8
            self.is_jumping = False

        # Horizontal
        self.rect.x += self.direction.x * self.speed * dt
        self.collision("x")

        # Vertical
        if not self.touching_sides["bottom"] and any((self.touching_sides["left"], self.touching_sides["right"])) and self.direction.y >= 0: # Wall sliding
            self.rect.y += self.gravity / 10 * dt
        else: # Falling
            self.direction.y += self.gravity / 2 * dt
            self.rect.y += self.direction.y * dt
            self.direction.y += self.gravity / 2 * dt
        self.collision("y")
    
    def check_contact(self):
        bottom_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        semi_bottom_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 32))
        left_rect = pygame.Rect(self.rect.topleft + vector(-2, self.rect.height/4), (2, self.rect.height / 2))
        right_rect = pygame.Rect((self.rect.topright + vector(0, self.rect.height/4), (2, self.rect.height / 2)))

        # Collisions
        self.touching_sides["bottom"] = True if bottom_rect.collidelist(self.collision_rects) >= 0 else False
        self.touching_sides["left"] = True if left_rect.collidelist(self.collision_rects) >= 0 else False
        self.touching_sides["right"] = True if right_rect.collidelist(self.collision_rects) >= 0 else False
        self.touching_sides["semi"] = True if semi_bottom_rect.collidelist(self.semi_collision_rects) >= 0 else False

    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == "x":
                    if sprite not in self.semi_collidable_sprites:
                        # Left
                        if self.rect.left <= sprite.rect.right and int(self.old_rect.left) >= sprite.old_rect.right:
                            self.rect.left = sprite.rect.right

                        # Right
                        if self.rect.right >= sprite.rect.left and int(self.old_rect.right) <= sprite.old_rect.left:
                            self.rect.right = sprite.rect.left

                elif axis == "y":
                    # Top
                    if self.rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    
                    # Bottom
                    if self.rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top

                    self.direction.y = 0

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update_collision(self):
        if not self.phasing_timer.active and not self.direction.y <= 0 and self.touching_sides["semi"]:
            self.collision_sprites = self.all_collision_sprites
            self.collision_rects = self.all_collision_rects
        else:
            self.collision_sprites = self.normal_collision_sprites
            self.collision_rects = self.normal_collision_rects
            
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.update_timers()
        self.update_collision()
        self.check_contact()
        self.move(dt)
        self.input()
        