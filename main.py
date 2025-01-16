from settings import *
from level import *
from pytmx.util_pygame import load_pygame

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption('CU-Tag')
        self.clock = pygame.time.Clock()

        self.tmx_maps = {
            "A1": load_pygame(convert_filename(["Maps", "MapA1.tmx"])),
            "T1": load_pygame(convert_filename(["Maps", "MapT1.tmx"])),
            "T2": load_pygame(convert_filename(["Maps", "MapT2.tmx"])),
        }

        self.game_state = "menu"
        self.settings_page = "Text"
        self.settings_option = "Label player names"
        self.settings_option_details = [True, "Label the player names above players. Toggle with F2.", bool]

        self.background_colour = colours["black"]
        self.show_fps = False
        self.display_fullscreen = False
        self.tag_cooldown_end = 0

        self.create_buttons()

    def create_buttons(self):
        # Menu
        self.menu_buttons = pygame.sprite.Group(
            Button(x=440, y=160, w=400, h=150, heading_text="Start", heading_text_font=fonts["consolas bold"], body_text="Start a new game", body_text_font=fonts["consolas"], body_text_offset=40),
            Button(x=10, y=465, w=300, h=75, heading_text="Settings", body_text="Change and view settings"),
            Button(x=10, y=550, w=300, h=75, heading_text="Instructions", body_text="How to play"),
            Button(x=10, y=635, w=300, h=75, heading_text="Credits", body_text="View credits"),
            Button(x=1070, y=635, w=200, h=75, heading_text="Quit", body_text="Quit the game")
        )

        self.return_button = pygame.sprite.GroupSingle(
            Button(x=1070, y=635, w=200, h=75, heading_text="Return", body_text="Back to menu")
        )

        # Settings
        self.settings_selection_buttons = pygame.sprite.Group(
            Button(x=10, y=60, w=200, h=75, heading_text="Text", body_text="What texts are shown"),
            Button(x=220, y=60, w=200, h=75, heading_text="Movement", body_text="How players move"),
            Button(x=430, y=60, w=200, h=75, heading_text="Game", body_text="How the game works"),
            Button(x=640, y=60, w=200, h=75, heading_text="Advanced", body_text="More options"),
        )
        self.settings_buttons = {}
        for setting_group_name, settings_group_dict in settings.items():
            sprite_group = pygame.sprite.Group(
                    Button(x=10, y=145+i*70, w=500, h=60, heading_text=setting[0], body_text=f"{setting[1][0]}. {setting[1][1] if len(setting[1][1]) < 44 else f"{setting[1][1][:42]}..."}") for i, setting in enumerate(settings_group_dict.items())
                )
            self.settings_buttons.update({setting_group_name: sprite_group})
    
    def run(self):
        global button_cooldown_end, front_surface, settings

        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                
                if event.type == pygame.MOUSEBUTTONUP:
                    button_cooldown_end = 0 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_click = True
                else:
                    self.mouse_click = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.display_fullscreen = not self.display_fullscreen
                        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE if self.display_fullscreen else pygame.FULLSCREEN)
                    
                    if event.key == pygame.K_F7:
                        print(pygame.mouse.get_pos())

                    if event.key == pygame.K_F1:
                        settings["Text"]["Show player list"][0] = not settings["Text"]["Show player list"][0]
                    if event.key == pygame.K_F2:
                        settings["Text"]["Label player names"][0] = not settings["Text"]["Label player names"][0]
                    if event.key == pygame.K_F3:
                        self.show_fps = not self.show_fps                  
                    if event.key == pygame.K_F4:
                        settings["Text"]["Label player keybinds"][0] = not settings["Text"]["Label player keybinds"][0]
                    if event.key == pygame.K_F5:
                        settings["Text"]["Label player tag times"][0] = not settings["Text"]["Label player tag times"][0]
                    if event.key == pygame.K_F6:
                        settings["Text"]["Show player tag times"][0] = not settings["Text"]["Show player tag times"][0]

                    if event.key == pygame.K_ESCAPE:
                        self.return_page()

            self.display_surface.fill(self.background_colour)
            
            if self.game_state == "menu":
                draw_text((360, 30), "AM - Tag", font=fonts["consolas title"], surface=self.display_surface)
                self.menu_buttons.update()
                self.menu_buttons.draw(self.display_surface)

                if self.mouse_click:
                    menu_button_sprites = self.menu_buttons.sprites()
                    if menu_button_sprites[0].is_clicked(): # Start
                        self.game_level = Level(self.tmx_maps[settings["Game"]["Map"][0]])
                        self.game_state = "game"
                    if menu_button_sprites[1].is_clicked(): # Settings
                        self.game_state = "settings"
                    if menu_button_sprites[2].is_clicked(): # Instructions
                        self.game_state = "instructions"
                    if menu_button_sprites[3].is_clicked(): # Credits
                        self.game_state = "credits"
                    if menu_button_sprites[4].is_clicked(): # Quit
                        self.stop()
                

            elif self.game_state == "game":
                if dt < (1 / 20): # Don't run the game at less than 20 fps
                    self.game_level.run(dt)

            elif self.game_state == "settings":
                draw_text((10, 10), "Settings", font=fonts["consolas bold"], surface=self.display_surface)
                draw_text((230, 22), f"Change the settings. Current page: {self.settings_page} settings.", font=fonts["consolas"], surface=self.display_surface)
                
                # Draw buttons at the top for selection the settings page
                self.settings_selection_buttons.update()
                self.settings_selection_buttons.draw(self.display_surface)

                # Draw buttons on the left based on the settings page, for selecting the settings options
                self.settings_buttons[self.settings_page].update()
                self.settings_buttons[self.settings_page].draw(self.display_surface)

                # Return button
                self.return_button.update()
                self.return_button.draw(self.display_surface)

                if self.mouse_click:
                    # Get button sprites
                    settings_selection_button_sprites = self.settings_selection_buttons.sprites()
                    settings_option_button_sprites = self.settings_buttons[self.settings_page].sprites()
                    buttons = settings_selection_button_sprites + settings_option_button_sprites

                    for button in buttons:
                        if button.is_clicked():
                            if button in settings_selection_button_sprites: # If the button is a page selection button
                                self.settings_page = button.heading_text # Change the page
                            else: # If the button is a option selection button
                                self.settings_option = button.heading_text # Change option
                                self.settings_option_details = settings[self.settings_page][self.settings_option] # Get the option details using settings
                
                # Draw the option changing
                if self.settings_option_details[2] == bool: # Type of the option
                    pass
                elif self.settings_option_details[2] == int or self.settings_option_details[2] == float:
                    pass
                elif self.settings_option_details[2] == str:
                    pass

            elif self.game_state == "instructions":
                pass

            elif self.game_state == "credits":
                pass

            # Return button check
            if self.return_button.sprite.is_clicked():
                self.return_page()
            
            if self.show_fps:
                draw_text((60, 60), f"FPS: {int(self.clock.get_fps())}", surface=self.display_surface)

            self.display_surface.blit(front_surface, (0, 0))
           
            pygame.display.update()

            front_surface.fill((0, 0, 0, 0))
    
    def stop(self):
        pygame.quit()
        exit()
    
    def return_page(self):
        if self.game_state != "menu" and self.game_state != "game":
            self.game_state = "menu"

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()