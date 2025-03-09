from settings import *
from level import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption('AaronMisc - Leveldotpy')
        self.clock = pygame.time.Clock()
        self.ui_manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.tmx_maps = {
            name: load_pygame(convert_filename(["Maps", f"Map{name}.tmx"])) for name in map_names
        }

        self.game_state = "menu"
        self.settings_page = "Text"
        self.settings_option = "Label player names"
        self.settings_option_details = [True, "Label the player names above players. Toggle with F2.", bool]
        self.instructions_page = "Movement"

        self.background_colour = colours["black"]
        self.show_fps = False
        self.display_fullscreen = False
        self.tag_cooldown_end = 0
        self.delete_counter = 0

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
            if setting_group_name == "Hidden":
                continue
            sprite_group = pygame.sprite.Group(
                    Button(x=10, y=145+i*70, w=500, h=60, heading_text=setting[0], body_text=f"{setting[1][0]}. {setting[1][1] if len(setting[1][1]) < 44 else f"{setting[1][1][:42]}..."}") for i, setting in enumerate(settings_group_dict.items())
                )
            self.settings_buttons.update({setting_group_name: sprite_group})
        self.bool_selection_buttons = pygame.sprite.Group(
            Button(x=520, y=550, w=500, h=75, heading_text="True", body_text=""),
            Button(x=520, y=635, w=500, h=75, heading_text="False", body_text="")
        )
        self.str_selection_buttons = pygame.sprite.Group(
            Button(x=520, y=550, w=500, h=75, heading_text="Next", body_text=""),
            Button(x=520, y=635, w=500, h=75, heading_text="Previous", body_text="")
        )
        self.number_selection_submit_button = Button(x=520, y=550, w=500, h=75, heading_text="Submit", body_text="")
        self.number_selection_buttons = pygame.sprite.Group(self.number_selection_submit_button)
        self.settings_number_text_entry = pygame_gui.elements.UITextEntryLine(pygame.rect.Rect((520, 465), (500, 75)), manager=self.ui_manager, object_id="#number_entry_line", visible=False)
        self.settings_number_text_entry.allowed_characters = "0123456789"
        self.settings_number_text_entry.length_limit = 8

        self.instructions_buttons = pygame.sprite.Group(
            Button(x=10, y=10, w=300, h=75, heading_text="Movement", body_text="How to move and game hotkeys"),
            Button(x=10, y=95, w=300, h=75, heading_text="Settings", body_text="Using the settings and debug"),
            Button(x=10, y=180, w=300, h=75, heading_text="Platforms", body_text="Guide to playforms"),
            Button(x=10, y=265, w=300, h=75, heading_text="Keybinds", body_text="List of keybinds"),
            Button(x=10, y=350, w=300, h=75, heading_text="Level editor", body_text="Using tiled")
        )

    def update_str_selection_indexes(self):
        self.str_selection_current_index = self.settings_option_details[3].index(self.settings_option_details[0])
        self.str_selection_next_index = (self.str_selection_current_index+1) % len(self.settings_option_details[3])
        self.str_selection_previous_index = (self.str_selection_current_index-1) % len(self.settings_option_details[3])
        self.str_selection_next_option = self.settings_option_details[3][self.str_selection_next_index]
        self.str_selection_previous_option = self.settings_option_details[3][self.str_selection_previous_index]        

    def run(self):
        global front_surface, settings, button_cooldown_end

        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                
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
                        settings["Text"]["Label player game ends"][0] = not settings["Text"]["Label player game ends"][0]

                    if event.key == pygame.K_ESCAPE:
                        self.return_page()
                    elif event.key == pygame.K_DELETE and self.game_state == "game":
                        self.delete_counter += 1
                        if self.delete_counter == 5:
                            self.game_state = "menu"
                
                self.ui_manager.process_events(event)

            self.display_surface.fill(self.background_colour)
            
            if self.game_state == "menu":
                draw_text((640, 40), "AaronMisc - Leveldotpy", font=fonts["consolas title"], centred=True, surface=self.display_surface, return_size=True)
                self.menu_buttons.update()
                self.menu_buttons.draw(self.display_surface)

                if self.mouse_click:
                    if pygame.time.get_ticks() >= button_cooldown_end:
                        button_cooldown_end = 0

                    menu_button_sprites = self.menu_buttons.sprites()
                    if menu_button_sprites[0].is_clicked(): # Start
                        settings["Hidden"]["Game ended"] = False
                        self.game_level = Level(self.tmx_maps[settings["Game"]["Map"][0]])
                        self.delete_counter = 0
                        self.game_state = "game"
                    if menu_button_sprites[1].is_clicked(): # Settings
                        self.game_state = "settings"
                    if menu_button_sprites[2].is_clicked(): # Instructions
                        self.game_state = "instructions"
                    if menu_button_sprites[3].is_clicked(): # Credits
                        self.game_state = "credits"
                    if menu_button_sprites[4].is_clicked(): # Quit
                        if pygame.time.get_ticks() >= button_cooldown_end:
                            self.stop()
                
            elif self.game_state == "game":
                if dt < (1 / 20): # Don't run the game at less than 20 fps
                    self.game_level.run(dt)

                    if settings["Hidden"]["Game ended"] and self.game_level.players_stats_output is not None:
                        self.game_stats = self.game_level.players_stats_output
                        self.game_state = "game stats"
            
            elif self.game_state == "game stats":
                draw_text((10, 10), "Game stats", font=fonts["consolas bold"], surface=self.display_surface)
                draw_text((10, 50), self.game_stats, font=fonts["consolas small"], surface=self.display_surface)

                self.return_button.update()
                self.return_button.draw(self.display_surface)

            elif self.game_state == "settings":
                draw_text((10, 10), "Settings", font=fonts["consolas bold"], surface=self.display_surface)
                draw_text((230, 22), f"Change the settings. Current page: {self.settings_page} settings.", font=fonts["consolas"], surface=self.display_surface)
                
                # Draw buttons at the top for selection the settings page
                self.settings_selection_buttons.update()
                self.settings_selection_buttons.draw(self.display_surface)

                # Draw buttons on the left based on the settings page, for selecting the settings options
                self.settings_buttons[self.settings_page].update()
                self.settings_buttons[self.settings_page].draw(self.display_surface)

                draw_text((520, 155), self.settings_page, font=fonts["consolas bold medium"], surface=self.display_surface)
                draw_text((520, 189), self.settings_option, font=fonts["consolas medium"], surface=self.display_surface)

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
                                self.settings_option = list(settings[button.heading_text].items())[0][0] # Change the option
                            else: # If the button is a option selection button
                                self.settings_option = button.heading_text # Change option
                            
                            self.settings_option_details = settings[self.settings_page][self.settings_option] # Get the option details using settings

                            if self.settings_option_details[2] == int or self.settings_option_details[2] == float:
                                if self.settings_option_details[2] == float:
                                    self.settings_number_text_entry.allowed_characters = "0123456789."
                                else:
                                    self.settings_number_text_entry.allowed_characters = "0123456789"

                                self.settings_number_text_entry.visible = True
                                self.settings_number_text_entry.set_text(str(self.settings_option_details[0]))
                            else:
                                self.settings_number_text_entry.visible = False

                            if self.settings_option_details[2] == str:
                                self.update_str_selection_indexes()
                    
                self.settings_option_offset = draw_text((520, 224), self.settings_option_details[1], font=fonts["consolas small"], surface=self.display_surface, wrap_text=True, return_size=True)[1] + 224 + 10 # Offset is height + x + 10
                draw_text((520, self.settings_option_offset), f"Currently: {self.settings_option_details[0]}", font=fonts["consolas small"], surface=self.display_surface, wrap_text=True)
                
                # Warnings
                settings_option_warning = ""
                settings_option_valid = True
                if self.settings_option_details[2] == int or self.settings_option_details[2] == float:
                    if self.settings_option_details[2] == float:
                        if self.settings_number_text_entry.text.count(".") > 1:
                            settings_option_warning = "You can only have one decimal point."
                            settings_option_valid = False
                    elif self.settings_number_text_entry.text == "":
                        settings_option_warning = "You must enter a number."
                        settings_option_valid = False
                    elif float(self.settings_number_text_entry.text) < self.settings_option_details[3][0] or float(self.settings_number_text_entry.text) > self.settings_option_details[3][1]:
                        settings_option_warning = f"Number {"should" if not self.settings_option_details[4] else "must"} be between {self.settings_option_details[3][0]} and {self.settings_option_details[3][1]}."
                        if self.settings_option_details[4]:
                            settings_option_valid = False
                    elif float(self.settings_number_text_entry.text) < 1:
                        settings_option_warning = f"Number must be at least 1."
                        settings_option_valid = False
                
                if settings_option_warning != "": draw_text((520, self.settings_option_offset + 39), settings_option_warning, font=fonts["consolas small"], surface=self.display_surface, wrap_text=True)

                
                # Draw the option changing
                if self.settings_option_details[2] == bool: # Type of the option
                    self.bool_selection_buttons.update()
                    self.bool_selection_buttons.sprites()[0].body_text = f"Change {self.settings_option} from {self.settings_option_details[0]} to True"
                    self.bool_selection_buttons.sprites()[1].body_text = f"Change {self.settings_option} from {self.settings_option_details[0]} to False"
                    self.bool_selection_buttons.draw(self.display_surface)

                    if self.mouse_click:
                        if self.bool_selection_buttons.sprites()[0].is_clicked():
                            settings[self.settings_page][self.settings_option][0] = True
                        elif self.bool_selection_buttons.sprites()[1].is_clicked():
                            settings[self.settings_page][self.settings_option][0] = False
                
                elif self.settings_option_details[2] == int or self.settings_option_details[2] == float:
                    self.number_selection_buttons.update()
                    self.number_selection_buttons.sprites()[0].body_text = f"Change {self.settings_option} from {self.settings_option_details[0]} to {self.settings_number_text_entry.text}"
                    self.number_selection_buttons.draw(self.display_surface)

                    if self.mouse_click and settings_option_valid:
                        if self.number_selection_submit_button.is_clicked():
                            settings[self.settings_page][self.settings_option][0] = self.settings_option_details[2](self.settings_number_text_entry.text) # Set it and convert it to the correct type (int or float)
                
                elif self.settings_option_details[2] == str:
                    self.str_selection_buttons.update()
                    self.str_selection_buttons.sprites()[0].body_text = f"Change {self.settings_option} from {self.settings_option_details[0]} to {self.str_selection_next_option}"
                    self.str_selection_buttons.sprites()[1].body_text = f"Change {self.settings_option} from {self.settings_option_details[0]} to {self.str_selection_previous_option}"
                    self.str_selection_buttons.draw(self.display_surface)

                    if self.mouse_click:
                        if self.str_selection_buttons.sprites()[0].is_clicked():
                            settings[self.settings_page][self.settings_option][0] = self.str_selection_next_option
                            self.str_selection_current_index = self.str_selection_next_index
                            self.update_str_selection_indexes()
                        elif self.str_selection_buttons.sprites()[1].is_clicked():
                            settings[self.settings_page][self.settings_option][0] = self.str_selection_previous_option
                            self.str_selection_current_index = self.str_selection_previous_index
                            self.update_str_selection_indexes()
            
            elif self.game_state == "instructions":
                draw_text(pos=(320, 10), text=f"Instructions", font=fonts["consolas bold"], surface=self.display_surface)
                draw_text(pos=(650, 22), text=f"Current page: {self.instructions_page}.", font=fonts["consolas"], surface=self.display_surface)
                draw_text(pos=(320, 62), text=instructions_dict[self.instructions_page], font=fonts["consolas small"], surface=self.display_surface)

                self.instructions_buttons.update()
                self.instructions_buttons.draw(self.display_surface)

                self.return_button.update()
                self.return_button.draw(self.display_surface)

                if self.mouse_click:
                    instructions_buttons_sprites = self.instructions_buttons.sprites()
                    for instructions_buttons_sprite in instructions_buttons_sprites:
                        if instructions_buttons_sprite.is_clicked():
                            self.instructions_page = instructions_buttons_sprite.heading_text


            elif self.game_state == "credits":
                draw_text((10, 10), "Credits", font=fonts["consolas bold"], surface=self.display_surface)
                draw_text((10, 62), text=credits_text, font=fonts["consolas small"], surface=self.display_surface)
                
                self.return_button.update()
                self.return_button.draw(self.display_surface)

            self.mouse_click = False

            self.ui_manager.update(dt)
            
            # Return button check
            if self.return_button.sprite.is_clicked() and pygame.time.get_ticks() >= button_cooldown_end:
                self.return_page()
            
            if self.show_fps:
                draw_text((60, 60), f"FPS: {int(self.clock.get_fps())}", surface=self.display_surface)

            self.display_surface.blit(front_surface, (0, 0))

            self.ui_manager.draw_ui(self.display_surface)
            pygame.display.update()

            front_surface.fill((0, 0, 0, 0))
    
    def stop(self):
        pygame.quit()
        exit()
    
    def return_page(self):
        global button_cooldown_end
        if self.game_state != "menu" and self.game_state != "game":
            self.game_state = "menu"
            self.settings_page = "Text"
            self.settings_option = "Label player names"
            self.settings_option_details = settings[self.settings_page][self.settings_option]

            button_cooldown_end = pygame.time.get_ticks() + 500
        self.settings_number_text_entry.visible = False

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main() # runs the main code
