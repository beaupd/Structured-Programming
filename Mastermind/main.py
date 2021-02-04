import pygame
import scenes


if __name__ == "__main__":
    pygame.init()
    surface = pygame.display.set_mode((200, 500))
    pygame.display.set_caption("Trainyard")
    FPS = pygame.time.Clock()

    while True:
        events = pygame.event.get()

        if events
