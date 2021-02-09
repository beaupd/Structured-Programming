import pygame
import pygame.freetype
import sys

import scenes


if __name__ == "__main__":#prima
    pygame.init()
    pygame.freetype.init()
    surface = pygame.display.set_mode((500, 800))
    pygame.display.set_caption("Mastermind")
    FPS = pygame.time.Clock()

    director = scenes.Director()

    while True:
        FPS.tick(60)

        if pygame.event.get(pygame.QUIT):
            pygame.quit()
            sys.exit()

        director.scene.handle_events(pygame.event.get())
        director.scene.update()
        director.scene.render(surface)

        pygame.display.flip()
