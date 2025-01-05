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
            1: load_pygame(convert_filename(["Maps", "Map1.tmx"])),
        }

        self.game_state = "menu"

        self.background_colour = colours["black"]
        self.show_fps = False
        self.display_fullscreen = False
        self.tag_cooldown_end = 0

        self.create_buttons()

    def create_buttons(self):
        # Menu
        self.menu_buttons = pygame.sprite.Group(
            Button(x=440, y=160, w=400, h=150, heading_text="Start", heading_text_font=fonts["consolas bold"], body_text="Start a new game", body_text_font=fonts["consolas"], body_text_offset=40),
            Button(x=10, y=10, w=300, h=75, heading_text="Settings", body_text="Change and view settings"),
            Button(x=10, y=110, w=300, h=75, heading_text="Instructions", body_text="How to play"),
            Button(x=10, y=210, w=300, h=75, heading_text="Credits", body_text="View credits"),
            Button(x=1070, y=635, w=200, h=75, heading_text="Quit", body_text="Quit the game")
        )

        self.return_buttons = pygame.sprite.Group()
    
    def run(self):
        global button_cooldown_end, front_surface

        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                
                if event.type == pygame.MOUSEBUTTONUP:
                    button_cooldown_end = 0
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F3:
                        self.show_fps = not self.show_fps
                    
                    if event.key == pygame.K_F11:
                        self.display_fullscreen = not self.display_fullscreen
                        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE if self.display_fullscreen else pygame.FULLSCREEN)
                    
                    if event.key == pygame.K_F7:
                        print(pygame.mouse.get_pos())

            self.display_surface.fill(self.background_colour)
            
            if self.game_state == "menu":
                mouse_click = pygame.mouse.get_pressed()[0]

                draw_text((360, 30), "AM - Tag", font=fonts["consolas title"], surface=self.display_surface)
                self.menu_buttons.update()
                self.menu_buttons.draw(self.display_surface)

                if mouse_click:
                    menu_button_sprites = self.menu_buttons.sprites()
                    if menu_button_sprites[0].is_clicked(): # Start
                        self.game_state = "game"
                        self.game_level = Level(self.tmx_maps[1])
                    if menu_button_sprites[1].is_clicked(): # Settings
                        self.game_state = "settings"
                    if menu_button_sprites[2].is_clicked(): # Instructions
                        self.game_state = "instructions"
                    if menu_button_sprites[3].is_clicked(): # Credits
                        self.game_state = "credits"
                    if menu_button_sprites[4].is_clicked(): # Quit
                        self.stop()
                

            elif self.game_state == "game":
                if dt < (1 / 60): # Don't run the game at less than 60 fps
                    self.game_level.run(dt)

            elif self.game_state == "settings":
                pass

            elif self.game_state == "instructions":
                pass

            elif self.game_state == "credits":
                pass

            if self.show_fps:
                draw_text((60, 60), f"FPS: {int(self.clock.get_fps())}", surface=self.display_surface)

            self.display_surface.blit(front_surface, (0, 0))
           
            pygame.display.update()

            front_surface.fill((0, 0, 0, 0))
    
    def stop(self):
        pygame.quit()
        exit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()