from settings import *
from pytimer import Timer
from text_base import draw_text

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, keybinds, surface, name):
        super().__init__(groups)

        # Rects
        self.image = surface
        self.rect = self.image.get_frect(center = pos)
        self.old_rect = self.rect.copy()

        # Movement
        self.direction = vector()
        self.speed = game_settings["Player speed"]
        self.jump_height = game_settings["Player jump height"]
        self.gravity = game_settings["Player gravity"]
        self.is_jumping = False

        # Collision
        self.border_sprites = collision_sprites["borders"]
        self.normal_collision_sprites = collision_sprites["normal"]
        self.normal_collision_rects = self.get_collision_rects(self.normal_collision_sprites)
        self.semi_collidable_sprites = collision_sprites["semi"]
        self.semi_collision_rects = [pygame.Rect((sprite.rect.x, sprite.rect.y), (sprite.rect.width, 1)) for sprite in self.semi_collidable_sprites]
        self.all_collision_sprites = pygame.sprite.Group(self.normal_collision_sprites.sprites() + self.semi_collidable_sprites.sprites())
        self.all_collision_rects = self.normal_collision_rects + self.semi_collision_rects
        self.player_sprites = None

        self.touching_sides = {
            "bottom": False,
            "left": False,  
            "right": False,
            "semi": False 
        }

        # Others
        self.phasing_timer = Timer(300)

        self.name = name
        self.keybinds = keybinds
        self.tagged = False
        self.tag_time = 60000

        self.counters = {
            "Tags": 0,
            "Tagged": 0,
            "Jumps": 0,
            "Air time": 0,
            "Move time": 0
        }
        self.current_time = pygame.time.get_ticks()
    
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
                self.counters["Jumps"] += 1
            elif any((self.touching_sides["left"], self.touching_sides["right"])):
                self.direction.y = -self.jump_height * 0.8
                self.counters["Jumps"] += 0.5
            self.is_jumping = False

        # Horizontal
        self.rect.x += self.direction.x * self.speed * dt
        self.collision("x")

        # Vertical
        if not self.touching_sides["bottom"] and not self.touching_sides["semi"] and any((self.touching_sides["left"], self.touching_sides["right"])) and self.direction.y >= 0: # Wall sliding
            self.rect.y += self.gravity / 10 * dt
        else: # Falling
            self.direction.y += self.gravity / 2 * dt
            self.rect.y += self.direction.y * dt
            self.direction.y += self.gravity / 2 * dt
        self.collision("y")
    
    def update_touching_sides(self):
        bottom_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        semi_bottom_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 8))
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

    def update_collision(self):
        if not self.phasing_timer.active and not self.direction.y <= 0 and self.touching_sides["semi"]:
            self.collision_sprites = self.all_collision_sprites
            self.collision_rects = self.all_collision_rects
        else:
            self.collision_sprites = self.normal_collision_sprites
            self.collision_rects = self.normal_collision_rects

    def tag_display(self):
        global front_surface

        remaining_tagged_time = ceil((self.tag_cooldown_end - self.current_time) / 1000)

        draw_text((self.rect.x + 2, self.rect.y - 50), str(remaining_tagged_time) if remaining_tagged_time > 0 else "T", tag_time_colours[remaining_tagged_time] if remaining_tagged_time > 0 else colours["white"], fonts["consolas bold"], surface=front_surface)

    def tag_check(self, dt):
        self.tag_time -= dt * 1000

        taggable_sprites = []

        for sprite in self.player_sprites:
            if sprite != self and self.rect.colliderect(sprite.rect): # If the player has tagged another player
                taggable_sprites.append([sprite, sprite.tag_time])
        
        if taggable_sprites == []:
            return
        
        taggable_sprites.sort(key=lambda x: x[1], reverse=True) # Sort by tag time
        if len(taggable_sprites) > 1 and taggable_sprites[0][0] == taggable_sprites[1][0]: # If there are players with the same tag time
            taggable_sprites = [sprite for sprite in taggable_sprites if sprite[1] == taggable_sprites[0][1]]
            tag_sprite = choice(taggable_sprites)
        else:
            tag_sprite = taggable_sprites[0][0]
    
        tag_sprite.tag()
        self.counters["Tags"] += 1
        sprite.counters["Tagged"] += 1

        self.tagged = False
        self.speed = game_settings["Player speed"]
        self.jump_height = game_settings["Player jump height"]
        self.gravity = game_settings["Player gravity"]
    
    def tag(self):     
        self.tagged = True
        self.tag_cooldown_end = self.current_time + game_settings["Tag cooldown"]

        self.speed = game_settings["Tagged player speed"]
        self.jump_height = game_settings["Tagged player jump height"]
        self.gravity = game_settings["Tagged player gravity"]

    def update_counters(self, dt):
        if self.direction != vector(0, 0):
            self.counters["Move time"] += dt * 1000
        if not any(self.touching_sides.values()):  # If the player is not touching any sides
            self.counters["Air time"] += dt * 1000

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.current_time = pygame.time.get_ticks()
        self.phasing_timer.update()
        self.update_collision()
        self.update_touching_sides()
        if self.tagged:
            if self.tag_cooldown_end < self.current_time: self.tag_check(dt)
            self.tag_display()
        self.input()
        self.move(dt)
        self.update_counters(dt)