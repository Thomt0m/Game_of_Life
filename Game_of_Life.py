import sys
import time
import pygame
import numpy as np


from Settings import Settings


from ScreenElements import *




class GameOfLife:

    # Settings
    grid_dim_length = 80







    def __init__(self) -> None:
        pygame.init()
        
        self.settings = Settings()

        pygame.display.set_caption("Game of Life")
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.dirty_rects = []
        self.refresh_entire_display = True

        self._time0 = time.time()
        self.running = True
        self.playing = False


        self.background = BackgroundGrid(self.screen_rect.size, self.grid_dim_length)

        self.pause_symbol = PauseButton(self.screen_rect.size)
        self.pause_symbol.rect.topleft = self.pause_symbol.rect.center

        self.layers:list[Layer] = []
        self.layers.append(Layer('Background', [self.background]))
        self.layers.append(Layer('Cells'))
        self.layers.append(Layer('UI', [self.pause_symbol]))










    def run_game(self):
        """Main loop"""


        while self.running:

            self.check_events()
            self.update_screen()


    def set_playing(self, playing:bool):
        self.playing = playing
        self.pause_symbol.set_surface(playing)



    
    def timer_interval(self) -> bool:
        isIntervalElapsed = False
        if self._time0 + self.settings.tick_interval <= time.time():
            isIntervalElapsed = True
            self._time0 = time.time() 
        return isIntervalElapsed





    def TEST(self):
        if self.timer_interval():
            match self.test_screen_counter:
                case 0:
                    pass









    def check_events(self):
        """Check for events from pygame"""
        for event in pygame.event.get():
            match event.type:

                case pygame.QUIT:
                    sys.exit()
                case pygame.KEYDOWN:
                    self._handle_keydown_event(event)
                case pygame.KEYUP:
                    self._handle_keyup_event(event)

    def _handle_keydown_event(self, event: pygame.event.Event):
        """Handle events of kind 'key down'"""
        match event.key:

            # On escape, quit game
            case pygame.K_ESCAPE:
                sys.exit()
            # On backspace, quit game
            case pygame.K_BACKSPACE:
                sys.exit()

            # Trigger pause
            case pygame.K_SPACE:
                self.set_playing(not self.playing)

    def _handle_keyup_event(self, event: pygame.event.Event):
        """Handle events of kind 'key up'"""
        pass

    def _handle_mousebuttondown_event(self, event: pygame.event.Event):
        """Handle the specified MouseButtonDown event. Acts based on mouse position"""
        mouse_pos = pygame.mouse.get_pos()
        # ... do something with mouse_pos




    






    def update_screen(self):
        """Update the elements of the screen, and draw the updated version"""

        if self.refresh_entire_display:
            self._screen_redraw_all()
            pygame.display.flip()
            self.refresh_entire_display = False
        else:
            self._find_dirty_rects()
            pygame.display.update(self.dirty_rects)
        
        self.dirty_rects.clear()

    def _screen_redraw_all(self):
        self._screen_draw_background()
        self._screen_draw_cells()
        self._screen_draw_pause_button()

    def _screen_draw_background(self):
        """Draw the background grid onto screen (covers whole screen)"""
        self.dirty_rects.append(self.screen.blit(self.background.surface, self.background.rect))

    def _screen_draw_cells(self):
        """Draw the cells of the 'Game of Life' onto screen"""
        pass

    def _screen_draw_pause_button(self):
        """Draw the pause button onto screen"""
        self.dirty_rects.append(self.screen.blit(self.pause_symbol.surface, self.pause_symbol.rect))


    def _find_dirty_rects(self):
        for layer in range(len(self.layers)):
            for element in range(len(self.layers[layer].elements)):
                if self.layers[layer].elements[element].dirty:
                    self._redraw_element(layer, element)
                    self.layers[layer].elements[element].dirty = False

    def _redraw_element(self, l0:int='layer', e0:int='element'):
        """Redraw the element on screen, first drawing all elements behind this one. Can not handle movement of element"""
        for l1 in range(min(len(self.layers), l0)):
            for e1 in range(min(len(self.layers[l1].elements), e0)):
                if self.layers[l0].elements[e0].collide(self.layers[l1].elements[e1].rect):
                    print('_redraw_elements() trying to redraw')
                    # Redraw everything that was behind the specified element
                    rect1 = self.screen.blit(self.layers[l1].elements[e1].surface, self.layers[l0].elements[e0].rect)
                    if self.layers[l0].elements[e0].draw:
                        rect0 = self.screen.blit(self.layers[l0].elements[e0].surface, self.layers[l0].elements[e0].rect)
                        rect1.union_ip(rect0)
                    self.dirty_rects.append(rect1)
                    

            





    





















if __name__ == '__main__':
    GoL = GameOfLife()
    GoL.run_game()