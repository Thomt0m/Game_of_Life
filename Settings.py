import pygame

class Settings:

    class GameLoopSettings:

        def __init__(self) -> None:
            self.tick_interval = 1000


    class BackgroundGridSettings:

        def __init__(self) -> None:
            self.background_colour = (240,240,240)
            self.line_density = 100