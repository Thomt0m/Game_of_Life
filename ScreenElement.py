import pygame

class ScreenElement:
    """Base class for screen elements"""

    def __init__(self) -> None:
        
        self.surface:pygame.surface.Surface = None
        self.rect:pygame.rect.Rect = None
        self.draw:bool = True
        self.dirty:bool = True

    def collide(self, rect:pygame.rect.Rect) -> bool:
        return self.rect.colliderect(rect)

    def union(self, rect:pygame.rect.Rect) -> pygame.rect.Rect:
        return self.rect.union(rect)