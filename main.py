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
        self.current_screen = Level(self.tmx_maps[1])
        self.game_settings = {
            "Player speed": 200,
            "Tagged player speed": 200,
            "Player jump height": 600,
            "Tagged player jump height": 600,
            "Gravity": 1200,
            "Tagged player gravity": 1200
        }

        self.background_colour = colours["black"]
        self.show_fps = False
        self.display_fullscreen = False

        self.create_buttons()

    def create_buttons(self):
        # Menu
        self.menu_buttons = pygame.sprite.Group(
            Button(x=10, y=120, w=200, h=75, heading_text="Start", body_text="Start a new game"),
            Button(x=10, y=240, w=200, h=75, heading_text="Settings", body_text="Change and view settings"),
            Button(x=10, y=360, w=200, h=75, heading_text="Instructions", body_text="How to play"),
            Button(x=10, y=480, w=200, h=75, heading_text="Credits", body_text="View credits"),
            Button(x=10, y=600, w=200, h=75, heading_text="Quit", body_text="Quit the game")
        )

        self.return_buttons = pygame.sprite.Group()
    
    def run(self):
        global button_cooldown_end

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
                    
                    if event.key == pygame.K_F1:
                        self.display_fullscreen = not self.display_fullscreen
                        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE if self.display_fullscreen else pygame.FULLSCREEN)

            self.display_surface.fill(self.background_colour)
            
            if self.game_state == "menu":
                mouse_click = pygame.mouse.get_pressed()[0]

                draw_text((10, 10), "Tag", font=fonts["consolas bold"], surface=self.display_surface)
                self.menu_buttons.update()
                self.menu_buttons.draw(self.display_surface)

                if mouse_click:
                    print("checking buttons")
                    menu_button_sprites = self.menu_buttons.sprites()
                    if menu_button_sprites[0].is_clicked(): # Start
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
                if dt < (1 / 60): # Don't run the game at less than 60 fps
                    self.current_screen.run(dt)

            elif self.game_state == "settings":
                pass

            elif self.game_state == "instructions":
                pass

            elif self.game_state == "credits":
                pass

            if self.show_fps:
                draw_text((60, 60), f"FPS: {int(self.clock.get_fps())}", surface=self.display_surface)
           
            pygame.display.update()
    
    def stop(self):
        pygame.quit()
        exit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()