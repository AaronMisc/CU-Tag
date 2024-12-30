from settings import *

pygame.init()

def draw_text(pos, text="Text", colour=colours["white"], font=fonts["consolas"], line_spacing=5, surface=pygame.display.get_surface()):
    if not isinstance(pos, list):
        pos = list(pos)

    lines = text.split("\n")
    for line in lines:
        text_surface = font.render(line, True, colour)
        text_rect = text_surface.get_rect(topleft=pos)
        surface.blit(text_surface, text_rect)
        pos[1] += text_surface.get_height() + line_spacing