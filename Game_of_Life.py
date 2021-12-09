'''
Game of Life
Written by Thomas A.
Based on the Game of Life by John Conway


User Guide;

To start, run Game_of_Life.py
This will display the Game of Life, fullscreen

In the top left, you will see a pause-play button
You can click this, or press spacebar, to start and pause the running of the Game of Life
While paused, you can click on any cell in the grid to changed its state (alive of dead)

TODO continue




'''




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
        self.refresh_entire_display = True

        self._time0 = time.time()

        #self._bg_line_dist = max(self.screen_rect.width, self.screen_rect.height) / self.settings.gol.grid_cells_screen
        #self._bg_hor_dim = self.screen_rect.width / self._bg_line_dist
        #self._bg_vert_dim = self.screen_rect.height / self._bg_line_dist


        self.background = BackgroundGrid(self.screen_rect.size, self.settings.gol.grid_cells_screen)

        self.pause_symbol = PauseButton(self.screen_rect.size)
        self.pause_symbol.rect.topleft = self.pause_symbol.rect.center





        self.running = True
        self.playing = False










    def run_game(self):
        """Main loop"""


        while self.running:

            self.check_events()
            self.update_screen()


    def set_playing(self, playing:bool):
        """Set whether the game is playing, or paused"""
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
        """Update the elements of the screen, and draw the newly constructed screen"""
        self._screen_draw_all_elements()
        pygame.display.flip()


    def _screen_draw_all_elements(self):
        """Draw all elements onto the screen. In order of back-to-front"""
        # ORDER MATTERS, objects further down get drawn over(on top of) the ones before
        self._screen_draw_background()
        self._screen_draw_cells()
        self._screen_draw_pause_button()

    def _screen_draw_background(self):
        """Draw the background grid onto screen (covers whole screen)"""
        self.screen.blit(self.background.surface, self.background.rect)

    def _screen_draw_cells(self):
        """Draw the cells of the 'Game of Life' onto screen"""
        pass

    def _screen_draw_pause_button(self):
        """Draw the pause button onto screen"""
        self.screen.blit(self.pause_symbol.surface, self.pause_symbol.rect)
                    

            





    





















if __name__ == '__main__':
    GoL = GameOfLife()
    GoL.run_game()