from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join

file_pre_path = ""
try:
    pygame.image.load(join("Images", "Player1.png"))
except:
    file_pre_path = "CU-Tag"

def convert_filename(path:list):
    if file_pre_path != "":
        path.insert(0, file_pre_path)
    return join(*path)

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

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            self.current_screen.run(dt)
            
            pygame.display.update()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()