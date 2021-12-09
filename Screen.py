import pygame







class Screen:

    

    def __init__(self) -> None:

        pygame.display.set_caption("Game of Life")
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.rect = self.screen.get_rect()

        self.dirty_rects = []
        self.refresh_entire_display = True


        
        # Background
        self.screen.fill((240,240,40))


        






        


    def update(self):
        """Update the elements of the screen, and draw the updated version"""

        if self.refresh_entire_display:
            pygame.display.flip()
            self.refresh_entire_display = False
        else:
            pygame.display.update(self.dirty_rects)
        
        self.dirty_rects.clear()


    def add_dirty_rect(self, rect:pygame.rect.Rect):
        self.dirty_rects.append(rect)

    def add_dirty_rects(self, rect1:pygame.rect.Rect, rect2:pygame.rect.Rect):
        
        if not rect2:
            self.dirty_rects.append(rect1)
        elif rect1.colliderect(rect2):
            self.dirty_rects.append(rect1.union(rect2))
        else:
            self.dirty_rects.append(rect1)
            self.dirty_rects.append(rect2)
            
        









    











        