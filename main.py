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

        self.current_screen = Level(self.tmx_maps[1])

        self.show_fps = False
        self.display_fullscreen = False

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F3:
                        self.show_fps = not self.show_fps
                    
                    if event.key == pygame.K_F1:
                        self.display_fullscreen = not self.display_fullscreen
                        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE if self.display_fullscreen else pygame.FULLSCREEN)

            self.current_screen.run(dt)

            if self.show_fps:
                draw_text((60, 60), f"FPS: {int(self.clock.get_fps())}", surface=self.display_surface)
           
            pygame.display.update()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()