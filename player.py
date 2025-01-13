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
        self.speed = movement_settings["Player speed"][0]
        self.jump_height = movement_settings["Player jump height"][0]
        self.gravity = movement_settings["Player gravity"][0]
        self.is_jumping = False
        self.moving_left = False
        self.moving_right = False

        # Collision
        self.border_sprites = collision_sprites["borders"]
        self.normal_collision_sprites = collision_sprites["normal"]
        self.normal_collision_rects = self.get_collision_rects(self.normal_collision_sprites)
        self.semi_collidable_sprites = collision_sprites["semi"]
        self.semi_collision_rects = [pygame.Rect((sprite.rect.x, sprite.rect.y), (sprite.rect.width, advanced_settings["Semi collision rect height"][0])) for sprite in self.semi_collidable_sprites]
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
        self.phasing_timer = Timer(100)

        self.name = name
        self.keybinds = keybinds
        self.tagged = False
        self.tag_time = game_settings["Tag time"][0]

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

        if len(self.keybinds) == 4:
            down_key = keys[self.keybinds[3]]
        else:
            down_key = keys[self.keybinds[0]] and keys[self.keybinds[2]]
        if down_key: # Down
            self.phasing_timer.start()
        else:
            if keys[self.keybinds[0]]: # Left
                self.moving_left = True
            elif keys[self.keybinds[2]]: # Right
                self.moving_right = True
            if keys[self.keybinds[1]]: # Jump
                self.is_jumping = True
        
    def move(self, dt):
        if self.is_jumping:
            if self.touching_sides["bottom"]:
                self.direction.y = -self.jump_height
                self.collision_sprites = self.normal_collision_sprites
                self.collision_rects = self.normal_collision_rects
                self.counters["Jumps"] += 1
            elif any((self.touching_sides["left"], self.touching_sides["right"])):
                self.direction.y = -self.jump_height * advanced_settings["Wall slide speed modifier"][0]
                self.counters["Jumps"] += 0.5
            self.is_jumping = False

        self.direction.x = 0
        if self.moving_left:
            self.direction.x -= 1
            self.moving_left = False
        elif self.moving_right:
            self.direction.x += 1
            self.moving_right = False

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
        bottom_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, advanced_settings["Jump rect height"][0]))
        semi_bottom_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, advanced_settings["Semi collision rect height"][0]))
        left_rect = pygame.Rect(self.rect.topleft + vector(-advanced_settings["Wall slide rect width"][0], self.rect.height/4), (advanced_settings["Wall slide rect width"][0], self.rect.height / 2))
        right_rect = pygame.Rect((self.rect.topright + vector(0, self.rect.height/4), (advanced_settings["Wall slide rect width"][0], self.rect.height / 2)))

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
        if not self.phasing_timer.active and not self.direction.y < 0 and self.touching_sides["semi"] and not self.is_jumping:
            self.collision_sprites = self.all_collision_sprites
            self.collision_rects = self.all_collision_rects
        else:
            self.collision_sprites = self.normal_collision_sprites
            self.collision_rects = self.normal_collision_rects

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
        self.speed =  movement_settings["Player speed"][0]
        self.jump_height =  movement_settings["Player jump height"][0]
        self.gravity =  movement_settings["Player gravity"][0]
    
    def tag(self):     
        self.tagged = True
        self.tag_cooldown_end = self.current_time + game_settings["Tag cooldown"][0]

        self.speed =  movement_settings["Tagged player speed"][0]
        self.jump_height =  movement_settings["Tagged player jump height"][0]
        self.gravity =  movement_settings["Tagged player gravity"][0]

    def display_text(self):
        global text_settings
        x_pos = self.rect.x + self.rect.width // 2
        y_offset = 0
        if text_settings["Label player tag times"][0]:
            y_offset += 16
            draw_text((x_pos, self.rect.y - y_offset), str(int(self.tag_time)), colours["firebrick1"], fonts["consolas small"], centred=True, surface=front_surface)
        if text_settings["Label player keybinds"][0]:
            y_offset += 16
            draw_text((x_pos, self.rect.y - y_offset), keys_to_names(self.keybinds), colours["skyblue1"], fonts["consolas small"], centred=True, surface=front_surface)
        if text_settings["Label player names"][0]:
            y_offset += 24
            draw_text((x_pos, self.rect.y - y_offset), self.name, colours["white"], fonts["consolas bold small"], centred=True, surface=front_surface)
        if self.tagged:
            y_offset += 40
            remaining_tagged_time = ceil((self.tag_cooldown_end - self.current_time) / 1000)
            draw_text((self.rect.x + 2, self.rect.y - y_offset), str(remaining_tagged_time) if remaining_tagged_time > 0 else "T", tag_time_colours[remaining_tagged_time] if remaining_tagged_time > 0 else colours["white"], fonts["consolas bold"], surface=front_surface)

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
        self.input()
        self.move(dt)
        self.display_text()
        self.update_counters(dt)