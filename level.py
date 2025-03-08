from settings import *
from sprites import *
from player import *
from pytimer import Timer

class Level:
    def __init__(self, tmx_map, offset=16, tile_size=32):
        self.offset = offset
        self.tile_size = tile_size
        self.tag_cooldown_timer = Timer(settings["Game"]["Tag cooldown"][0])
        self.players_stats_output = None

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
                Sprite((x * self.tile_size + self.offset, y * self.tile_size + self.offset), tmx_map_opening_setting[1], surf)
        
        # Player setup
        for obj in tmx_map.get_layer_by_name("Objects"): 
            if obj.name == "Player1" or obj.name == "Player4":
                Player((obj.x + self.offset, obj.y + self.offset), (self.all_sprites, self.player_sprites), {"normal": self.collision_sprites, "semi": self.semi_collidable_sprites, "borders": self.border_sprites}, keybinds["normal"][obj.name], obj.image, obj.name)
        
        self.player_sprites_list = self.player_sprites.sprites()
        for player in self.player_sprites_list: # Updating player sprites
            excluside_player_sprites_list = self.player_sprites_list.copy()
            excluside_player_sprites_list.remove(player)
            player.player_sprites = excluside_player_sprites_list

            if player.name == "Player1":
                player.tag()

    def draw_player_tag_times(self):
        display_text_tag_times = ""

        for player in self.player_sprites_list:
            display_text_tag_times += f"{player.name} ({keys_to_names(player.keybinds)}): {int(player.tag_time)}\n"

        draw_text((60, 120), display_text_tag_times, colour=colours["firebrick1"] if pygame.time.get_ticks() >= tag_cooldown_end else colours["firebrick3"], font=fonts["consolas small"], surface=self.display_surface)

    def create_ending_stats(self):
        players_stats = []

        stat_names_checked = False
        stat_names = ["Name", "Tag time"]
        for player in self.player_sprites.sprites():
            player_stats = [player.name, player.tag_time]

            for name, value in player.counters.items():
                if not stat_names_checked:
                    stat_names.append(name)

                player_stats.append(value)
            stat_names_checked = True
            
            players_stats.append(player_stats)
        
        # Sort player stats by tag times
        players_stats.sort(key=lambda player_stats: player_stats[1], reverse=True)
        # Add player places
        for i, player_stats in enumerate(players_stats):
            player_stats.insert(0, i + 1)
        
        self.players_stats_output = tabulate(players_stats, headers=stat_names, tablefmt="grid" if settings["Game"]["Player amount"][0] < 10 else "simple")
    
    def run(self, dt):
        global settings

        self.player_sprites.update(dt)
        if settings["Hidden"]["Game ended"]: self.create_ending_stats()
        self.all_sprites.draw(self.display_surface)
        if settings["Text"]["Show player list"][0]: self.draw_player_tag_times()