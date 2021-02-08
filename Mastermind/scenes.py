import pygame
import sys
import random


# Help Classes, functions, etc.
pygame.freetype.init()
regularfont = pygame.freetype.SysFont('Mono', 20)
titlefont = pygame.freetype.SysFont('Mono', 60)


class Button:                           # Class representing a clickable button
    def __init__(self, rect, text, funcs, args):
        self.rect = rect
        self.text = text
        self.color = 220
        self.funcs = funcs
        self.args = args

    # Change color on hover
    def hover(self, mousepos):
        if self.rect.collidepoint(mousepos):
            # Become darker when mouse is hovering over button
            self.color = self.color - 2 if self.color > 190 else self.color
        else:
            # Become lighter when no mouse is hovering over button
            self.color = self.color + 2 if self.color < 220 else self.color

    # Draw the button
    def render(self):
        surface = pygame.Surface(self.rect.size)

        # Background and border
        pygame.draw.rect(surface, tuple([self.color] * 3), pygame.Rect(0, 0, 300, 30), 0)
        pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(1, 1, 298, 28), 2)

        # Text
        text, rect = regularfont.render(self.text, (0, 0, 0))
        surface.blit(text, (surface.get_width() // 2 - rect.width // 2, 10))

        return surface


class ColorPicker:                      # Class representing a clickable color picker
    def __init__(self):
        self.colors = "RGBYPO"
        self.selectedtile = 0
        self.rect = pygame.Rect(0, 650, 500, 150)

    def click(self, mousepos):
        # Switch colors
        tilewidth = self.rect.width // 6
        for t in range(6):
            if pygame.Rect(tilewidth * t, 700, tilewidth, 100).collidepoint(mousepos):
                self.selectedtile = t

    def selected(self):
        return self.colors[self.selectedtile]

    def render(self):
        surface = pygame.Surface(self.rect.size)
        surface.fill((220, 220, 220))

        tilewidth = self.rect.width // 6
        for t in range(6):
            pygame.draw.rect(surface, get_colors(self.colors[t])[0], pygame.Rect(tilewidth * t, 50, tilewidth + 3, 100))

        pygame.draw.circle(surface, (0, 0, 0), ((self.selectedtile * tilewidth) + tilewidth//2, 100), 15)

        return surface


def get_colors(colorlst):
    colors = {                              # For converting characters to colors
        "R": (255, 0, 0),
        "G": (0, 255, 0),
        "B": (0, 0, 255),
        "Y": (255, 255, 0),
        "P": (255, 0, 255),
        "O": (255, 125, 0),
        "X": (100, 100, 100),
        "b": (0, 0, 0),
        "w": (255, 255, 255)
    }
    return [colors[c] for c in colorlst]


# Main Classes
class Director:                         # Controls the scenes and handles transitions between them
    def __init__(self):
        self.scene = None
        self.switch(MenuScene())

    def switch(self, scene):
        self.scene = scene
        self.scene.director = self


class Scene:                            # Scene base class
    def __init__(self):
        self.director = None

    def handle_events(self, events):
        mousepos = pygame.mouse.get_pos()

        # Each scene is dealing with buttons, so the button handling is done here
        # Handle mouse hover over buttons
        for button in self.buttons:
            button.hover(mousepos)

        # Handle button click
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                for button in self.buttons:
                    if button.rect.collidepoint(mousepos):
                        for func in button.funcs:
                            func(*button.args)

    def update(self):
        pass

    def render(self, surface):
        # Clear screen
        surface.fill((220, 220, 220))

        # Button rendering
        for button in self.buttons:
            surface.blit(button.render(), button.rect.topleft)

    # Used for switching to another scene, can be called by buttons.
    def switch(self, scene):
        self.director.switch(Fader(self, scene()))


class GameScene(Scene):                 # The class representing the game played by the user
    def __init__(self):
        super().__init__()
        self.info = "Guess a code"
        self.code = "".join(["RGBYPO"[random.randint(0, 5)] for _ in range(4)])  # Generate a code
        print(self.code)
        self.buttons = []
        self.guesses = [
            ("RGBY", (1, 2)),
            ("POPO", (2, 0))
        ]

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def render(self, surface):
        super().render(surface)

        # Title
        text, rect = regularfont.render("Mastermind", (0, 0, 0))
        surface.blit(text, (surface.get_width() // 2 - rect.width // 2, 40))

        # Grid
        pygame.draw.line(surface, (110, 110, 110), (50, 70), (50, 610))
        pygame.draw.line(surface, (110, 110, 110), (382.5, 70), (382.5, 610))
        pygame.draw.line(surface, (110, 110, 110), (450, 70), (450, 610))
        for i in range(9):
            pygame.draw.line(surface, (110, 110, 110), (50, 70 + (67.5 * i)), (450, 70 + (67.5 * i)))

        # The guesses and their responses
        for i in range(8):
            if i < len(self.guesses):
                guesscolors = get_colors(self.guesses[i][0])
                response = ("b" * self.guesses[i][1][0]) + ("w" * self.guesses[i][1][1]) + ("X" * (4 - sum(self.guesses[i][1])))
                responsecolors = get_colors(response)
            else:
                guesscolors = get_colors("XXXX")
                responsecolors = get_colors("XXXX")

            for j in range(4):
                pygame.draw.circle(surface, guesscolors[j], (50 + (66.5 * (j + 1)), 103.75 + (67.5 * (7 - i))), 15)


class BotScene(Scene):                  # The class representing the game played by an ai
    def __init__(self):
        super().__init__()
        pass

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def render(self, surface):
        pass


class BotSelectScene(Scene):
    def __init__(self):
        super().__init__()
        self.buttons = [
            Button(pygame.Rect(100, 600, 300, 30), "Back", [self.switch], [MenuScene])
        ]
        self.colorpicker = ColorPicker()

    def handle_events(self, events):
        super().handle_events(events)

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                self.colorpicker.click(pygame.mouse.get_pos())

    def update(self):
        pass

    def render(self, surface):
        super().render(surface)
        surface.blit(self.colorpicker.render(), self.colorpicker.rect.topleft)


class MenuScene(Scene):                 # The class representing the main menu
    def __init__(self):
        super().__init__()
        self.buttons = [
            Button(pygame.Rect(100, 400, 300, 30), "Crack the Code", [self.switch], [GameScene]),
            Button(pygame.Rect(100, 500, 300, 30), "Test an AI", [self.switch], [BotSelectScene]),
            Button(pygame.Rect(100, 600, 300, 30), "Quit", [pygame.quit, sys.exit], [])
        ]

    def handle_events(self, events):
        super().handle_events(events)

    def render(self, surface):
        super().render(surface)

        # Title text
        text, rect = titlefont.render("Mastermind", (0, 0, 0))
        surface.blit(text, (surface.get_width() // 2 - rect.width // 2, 40))
        text, rect = regularfont.render("by Jonathan Williams", (0, 0, 0))
        surface.blit(text, (surface.get_width() // 2 - rect.width // 2, 100))


class Fader(Scene):                         # Handles fading in and out between scenes
    def __init__(self, prv, nxt):
        super().__init__()
        self.cur = prv  # The previous scene
        self.nxt = nxt  # The next scene
        self.fadein = True
        self.fade = 0
        sr = pygame.display.get_surface().get_rect()
        self.veil = pygame.Surface(sr.size)

    def handle_events(self, events):
        # The fader is meant to go uninterrupted, so event handling is disabled.
        pass

    def update(self):
        self.fade = self.fade + 15 if self.fadein else self.fade - 15
        if self.fade >= 255:
            self.fadein = False
            self.cur = self.nxt
        if self.fade <= 0:
            self.director.switch(self.nxt)

    def render(self, surface):
        self.cur.render(surface)
        pygame.draw.rect(self.veil, (220, 220, 220), surface.get_rect())
        self.veil.set_alpha(self.fade)
        surface.blit(self.veil, (0, 0))
