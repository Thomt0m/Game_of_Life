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








    def __init__(self) -> None:

        pygame.init()
        self._set_prefab_patterns()
        self.settings = Settings()


        # SCREEN
        pygame.display.set_caption("Game of Life")
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()        


        # GRID
        self._screen_grid_line_dist = max(self.screen_rect.width, self.screen_rect.height) / self.settings.gol.grid_cells_screen
        self._grid_m = self.screen_rect.height / self._screen_grid_line_dist
        self._grid_n = self.screen_rect.width / self._screen_grid_line_dist

        self.grid = np.full((int(self._grid_m) + 1, int(self._grid_n) + 1), False)
        self.grid_m = self.grid.shape[0]
        self.grid_n = self.grid.shape[1]


        # SCREEEN ELEMENTS
        self.screen_grid = ScreenGrid(self.screen_rect.size, self._grid_m, self._grid_n, self._screen_grid_line_dist)
        self.pause_symbol = PauseButton(self.screen_rect.size)
        self.pause_symbol.rect.topleft = self.pause_symbol.rect.center



        # GENERAL
        self._time0 = time.time()
        self.running = True
        self.playing = False


        # Starting grid
        self.set_grid(self.pattern_pulsar)










    def run_game(self):
        """Main loop"""


        while self.running:

            self.check_events()

            self.check_game_update()

            self.update_screen()


    def set_playing(self, playing:bool):
        """Set whether the game is playing, or paused"""
        self.playing = playing
        self.pause_symbol.set_surface(playing)
        
        if playing: self._time0 = time.time() - max(0.1, self.settings.gol.tick_interval - 0.1)



    
    def timer_interval(self) -> bool:
        isIntervalElapsed = False
        if self._time0 + self.settings.gol.tick_interval <= time.time():
            isIntervalElapsed = True
            self._time0 = time.time()
        return isIntervalElapsed




    def check_game_update(self):
        if self.playing and self.timer_interval():
            self.iterate_game_of_life()



    def set_grid(self, cells:list[list[int]]):

        self.grid.fill(False)

        # Find the length of the dimensions of 'cells'
        input_m = len(cells)
        input_n = 0
        for i in range(input_m):
            input_n = max(input_n, len(cells[i]))

        input_m = min(input_m, self.grid_m)
        input_n = min(input_n, self.grid_n)

        input_offset = (int(self.grid_m/2 - input_m/2), int(self.grid_n/2 - input_n/2))

        for m in range(input_m):
            for n in range(input_n):
                self.grid[m + input_offset[0], n + input_offset[1]] = cells[m][n] > 0
                

        self.screen_grid.set_cells(self.grid)

            



        
        


    def iterate_game_of_life(self):
        
        # list containing all cells that are life at the end of this iteration
        changed_cells = []

        # new grid
        new_grid = self.grid.copy()

        for m in range(1,self.grid_m-1):
            for n in range(1,self.grid_n-1):

                neighbours = 0
                for m1 in range(-1, 2):
                    for n1 in range(-1, 2):
                        if m1 != 0 or n1 != 0:
                            neighbours += self.grid[m + m1, n + n1]

                # If cell is alive
                if self.grid[m,n]:
                    # Less than 2 live neighbours, or more than 3, cell dies
                    if neighbours < 2 or neighbours > 3:
                        new_grid[m,n] = False
                        changed_cells.append((m,n,0))
                # If cell is dead, and has exactly 3 neighbours, create a new live cell
                elif neighbours == 3:
                    new_grid[m,n] = True
                    changed_cells.append((m,n,1))

        self.grid = new_grid.copy()

        #self.screen_grid.cells.set_cells_changed(changed_cells)
        self.screen_grid.set_cells(self.grid)

        


                    


            









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

            case pygame.K_RETURN:
                self.set_grid(self.pattern_toad)

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
        self._screen_draw_cells()
        self._screen_draw_grid()
        self._screen_draw_pause_button()

    def _screen_draw_cells(self):
        """Draw the cells of the 'Game of Life' onto screen"""
        self.screen.blit(self.screen_grid.cells.surface, self.screen_grid.cells.rect)

    def _screen_draw_grid(self):
        """Draw the background grid onto screen (covers whole screen)"""
        self.screen.blit(self.screen_grid.grid.surface, self.screen_grid.grid.rect)

    def _screen_draw_pause_button(self):
        """Draw the pause button onto screen"""
        self.screen.blit(self.pause_symbol.surface, self.pause_symbol.rect)







    def _set_prefab_patterns(self):
        ''' BLINKER
          O
          O
          O
        '''
        self.pattern_blinker = [
            [0,1,0],
            [0,1,0],
            [0,1,0],
        ]

        ''' TOAD
         O
         OO
         OO
          O
        '''
        self.pattern_toad = [
            [0,0,0,0],
            [0,1,1,1],
            [1,1,1,0],
            [0,0,0,0]
        ]


        ''' PULSAR
          OOO   OOO  
                     
        O    O O    O
        O    O O    O
        O    O O    O
          OOO   OOO  
                     
          OOO   OOO  
        O    O O    O
        O    O O    O
        O    O O    O
                     
          OOO   OOO  
        '''
        self.pattern_pulsar = [
            [0,0,1,1,1,0,0,0,1,1,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [0,0,1,1,1,0,0,0,1,1,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,1,1,0,0,0,1,1,1,0,0],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [1,0,0,0,0,1,0,1,0,0,0,0,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,1,1,0,0,0,1,1,1,0,0]
        ]






    



























                    

            





    





















if __name__ == '__main__':
    GoL = GameOfLife()
    GoL.run_game()