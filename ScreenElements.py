import pygame
import numpy as np













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








class BackgroundGrid(ScreenElement):
    """Background grid"""

    # Settings
    background_colour = (220,220,220)
    line_colour = (60,60,60)


    def __init__(self, screen_size:tuple, grid_cells_m:float, grid_cells_n:float) -> None:
        super().__init__()

        self.screen_size = screen_size
        self._grid_cells_m:float = 0.0
        self._grid_cells_n:float = 0.0
        self.create_grid(grid_cells_m, grid_cells_n)


    def update(self):
        if self.dirty:
            # do someting, if desired (currently just a placeholder)
            pass


    def create_grid(self, grid_cells_m:float, grid_cells_n:float):
        """Create the background-grid surface"""
        self._grid_cells_m = grid_cells_m
        self._grid_cells_n = grid_cells_n

        self.surface = pygame.surface.Surface(self.screen_size)
        self.rect = self.surface.get_rect()

        self.surface.fill(self.background_colour)        
        
        #TODO remove, test, two diagonal lines which cross eachother in the center of the screen
        #pygame.draw.line(self.surface, (200, 40, 40), (0, 0), (self.rect.width, self.rect.height))
        #pygame.draw.line(self.surface, (200, 40, 40), (0, self.rect.height), (self.rect.width, 0))
                
        line_dist = self.rect.height / self._grid_cells_m

        # Draw the horizontal lines (rows, left-right)
        hor_edge = self._grid_cells_m % 1
        if hor_edge < 0.5: hor_edge += 1
        hor_edge *= 0.5 * line_dist
        for i in range(0, int(self._grid_cells_m) + 1):
            hor_coor = (line_dist * i) + hor_edge
            pygame.draw.line(self.surface, self.line_colour, (0, hor_coor), (self.rect.width, hor_coor))

        # Draw the vertical lines (columns, up-down)
        vert_edge = self._grid_cells_n % 1
        if vert_edge < 0.5: vert_edge += 1
        vert_edge *= 0.5 * line_dist
        for i in range(0, int(self._grid_cells_n) + 1):
            vert_coor = (line_dist * i) + vert_edge
            pygame.draw.line(self.surface, self.line_colour, (vert_coor, 0), (vert_coor, self.rect.height))

        self.dirty = True

    def get_dimensions(self) -> tuple:
        """Get the total number of cells in each dimension of the current grid, (m, n)"""
        return (self._grid_cells_n, self._grid_cells_m)

    def get_dimensions_int(self) -> tuple:
        """Get the total number of cells in each dimension of the current grid, (m, n)"""
        return (int(self._grid_cells_m), int(self._grid_cells_n))

            
    # TODO determine if this is a desired feature or more hassle than it is worth
    def resize_grid(self, size_increase:int):
        """Resize the grid, NOT IMPLEMENTED"""
        pass


class ScreenGrid:    

    class Background(ScreenElement):
        """Background grid"""

        _line_dist:float = 0.0
        _screen_edge_m:float = 0.0
        _screen_edge_n:float = 0.0

        def __init__(self, screen_size:tuple, grid_cells_m:float, grid_cells_n:float, line_dist:float, background_colour, line_colour) -> None:
            super().__init__()
            self._grid_cells_m = grid_cells_m
            self._grid_cells_n = grid_cells_n
            self._line_dist = line_dist
            self._create_grid(screen_size, background_colour, line_colour)


        def _create_grid(self, screen_size:tuple, background_colour, line_colour):
            """Create the background-grid surface"""

            self.surface = pygame.surface.Surface(screen_size)
            self.rect = self.surface.get_rect()

            self.surface.fill(background_colour)
            
            #TODO remove, test, two diagonal lines which cross eachother in the center of the screen
            #pygame.draw.line(self.surface, (200, 40, 40), (0, 0), (self.rect.width, self.rect.height))
            #pygame.draw.line(self.surface, (200, 40, 40), (0, self.rect.height), (self.rect.width, 0))                    

            # Draw the horizontal lines (rows, left-right)
            self._screen_edge_m = self._grid_cells_m % 1
            if self._screen_edge_m < 0.5: self._screen_edge_m += 1
            self._screen_edge_m *= 0.5 * self._line_dist
            for i in range(0, int(self._grid_cells_m) + 1):
                hor_coor = (self._line_dist * i) + self._screen_edge_m
                pygame.draw.line(self.surface, line_colour, (0, hor_coor), (self.rect.width, hor_coor))

            # Draw the vertical lines (columns, up-down)
            self._screen_edge_n = self._grid_cells_n % 1
            if self._screen_edge_n < 0.5: self._screen_edge_n += 1
            self._screen_edge_n *= 0.5 * self._line_dist
            for i in range(0, int(self._grid_cells_n) + 1):
                vert_coor = (self._line_dist * i) + self._screen_edge_n
                pygame.draw.line(self.surface, line_colour, (vert_coor, 0), (vert_coor, self.rect.height))

            self.dirty = True

        def get_dimensions_float(self) -> tuple:
            """Get the total number of cells in each dimension of the current grid, (m, n)"""
            return (self._grid_cells_n, self._grid_cells_m)

        def get_dimensions(self) -> tuple:
            """Get the total number of cells in each dimension of the current grid, (m, n)"""
            return (int(self._grid_cells_m), int(self._grid_cells_n))

        def get_screen_offset(self) ->tuple:
            """Get the screen 'buffer' edges of the grid. (offset)"""
            return (self._screen_edge_m, self._screen_edge_n)



    class Cells(ScreenElement):
        """Screen image of cells in Game of Life"""

        _line_dist:float = 0.0
        _screen_offset:float = 0.0
        _cell:pygame.surface.Surface = None
        _cell_rect:pygame.rect.Rect = None
        _cell_clear:pygame.surface.Surface = None


        def __init__(self, screen_size:tuple, grid_cells_m:float, grid_cells_n:float, line_dist:float, screen_offset:tuple, background_colour, cell_colour) -> None:
            super().__init__()

            self._line_dist = line_dist
            self._screen_offset = screen_offset
            self._background_colour = background_colour

            self.surface = pygame.surface.Surface(screen_size)
            self.surface.fill(self._background_colour)
            self.rect = self.surface.get_rect()

            self._create_cell(background_colour, cell_colour)


        def _create_cell(self, background_colour, cell_colour):
            self._cell = pygame.surface.Surface((self._line_dist, self._line_dist), pygame.SRCALPHA)
            self._cell_rect = self._cell.get_rect()
            
            cell_size = self._line_dist * 0.8
            cell = pygame.surface.Surface((cell_size, cell_size), pygame.SRCALPHA)
            cell.fill(cell_colour)
            cell_rect = cell.get_rect()
            cell_rect.center = self._cell_rect.center
            self._cell.blit(cell, cell_rect)
            
            cell_clear_size = self._line_dist * 0.95
            self._cell_clear = pygame.surface.Surface((cell_clear_size, cell_clear_size))
            self._cell_clear.fill(background_colour)
            self._cell_clear.get_rect().center = self._cell_rect.center


        def _clear_surface(self):
            self.surface = pygame.surface.Surface(self.rect.size)
            self.surface.fill(self._background_colour)
            

        def set_cell(self, coor:tuple, alive:bool):
            rect = self._cell_rect.copy()
            rect.topleft = (coor[1] * self._line_dist - self._screen_offset[1], coor[0] * self._line_dist - self._screen_offset[0])
            if alive:
                self.surface.blit(self._cell, rect)
            else:
                self.surface.blit(self._cell_clear, rect)

        def set_cell_life(self, coor:tuple):
            rect = self._cell_rect.copy()
            rect.topleft = (coor[1] * self._line_dist - self._screen_offset[1], coor[0] * self._line_dist - self._screen_offset[0])
            self.surface.blit(self._cell, rect)


        def set_cells_array(self, cells:np.ndarray):
            if cells.ndim < 2: return

            self._clear_surface()
            for m in range(cells.shape[0]):
                for n in range(cells.shape[1]):
                    if cells[m,n]:
                        self.set_cell_life((m,n))


        def set_cells_list(self, life_cells:list[tuple], offset = (0,0), alive:bool = True):
            self._clear_surface()

            for coor in life_cells:
                rect = self._cell_rect.copy()
                rect.topleft = (coor[1] * self._line_dist - self._screen_offset[1] + offset[1], coor[0] * self._line_dist - self._screen_offset[0] + offset[0])                
                if alive:
                    self.surface.blit(self._cell, rect)
                else:
                    self.surface.blit(self._cell_clear, rect)


        def set_cells_centered(self, life_cells:list[tuple]):

            # Find the smallest and largest cell-coordinates, ie coordinates of top-left and bottom-right cells
            coor_min = [self.rect.height / self._line_dist + 1, self.rect.width / self._line_dist + 1]
            coor_max = [0,0]
            for coor in life_cells:
                if coor_min[0] > coor[0]:
                    coor_min[0] = coor[0]
                if coor_min[1] > coor[1]:
                    coor_min[1] = coor[1]
                if coor_max[0] < coor[0]:
                    coor_max[0] = coor[0]
                if coor_max[1] < coor[1]:
                    coor_max[1] = coor[1]

            # Get the required offset for life_cells to be in the center of the screen
            coor_center = (int((coor_min[0] + coor_max[0])/2), int((coor_min[1] + coor_max[1])/2))
            offset = (self.rect.centery - (coor_center[0] - 0.5) * self._line_dist, self.rect.centerx - coor_center[1] * self._line_dist)
            
            self.set_cells_list(life_cells, offset)


        def load_prefab_cell_pattern(self, prefab:list[list[int]]):
            coor_list = []
            for m in range(len(prefab)):
                for n in range(len(prefab[m])):
                    if prefab[m][n]:
                        coor_list.append((m,n))
            self.set_cells_centered(coor_list)

        
        def set_cells_changed(self, changed_cells:list[tuple]):
            for cell in changed_cells:
                self.set_cell((cell[0],cell[1]), cell[2] > 0)

        def set_cells_changed_2(self, life_cells:list[tuple]):
            self._clear_surface()
            for cell in life_cells:
                self.set_cell((cell[0], cell[1]))








    class Grid(ScreenElement):
        """Background grid"""

        _line_dist:float = 0.0
        _screen_edge_m:float = 0.0
        _screen_edge_n:float = 0.0

        def __init__(self, screen_size:tuple, grid_cells_m:float, grid_cells_n:float, line_dist:float, line_colour) -> None:
            super().__init__()
            self._grid_cells_m = grid_cells_m
            self._grid_cells_n = grid_cells_n
            self._line_dist = line_dist
            self._create_grid(screen_size, line_colour)


        def _create_grid(self, screen_size:tuple, line_colour):
            """Create the background-grid surface"""

            self.surface = pygame.surface.Surface(screen_size, pygame.SRCALPHA)
            self.rect = self.surface.get_rect()
            
            #TODO remove, test, two diagonal lines which cross eachother in the center of the screen
            #pygame.draw.line(self.surface, (200, 40, 40), (0, 0), (self.rect.width, self.rect.height))
            #pygame.draw.line(self.surface, (200, 40, 40), (0, self.rect.height), (self.rect.width, 0))

            # Draw the horizontal lines (rows, left-right)
            self._screen_edge_m = self._grid_cells_m % 1
            if self._screen_edge_m < 0.5: self._screen_edge_m += 1
            self._screen_edge_m *= 0.5 * self._line_dist
            for i in range(0, int(self._grid_cells_m) + 1):
                hor_coor = (self._line_dist * i) + self._screen_edge_m
                pygame.draw.line(self.surface, line_colour, (0, hor_coor), (self.rect.width, hor_coor))

            # Draw the vertical lines (columns, up-down)
            self._screen_edge_n = self._grid_cells_n % 1
            if self._screen_edge_n < 0.5: self._screen_edge_n += 1
            self._screen_edge_n *= 0.5 * self._line_dist
            for i in range(0, int(self._grid_cells_n) + 1):
                vert_coor = (self._line_dist * i) + self._screen_edge_n
                pygame.draw.line(self.surface, line_colour, (vert_coor, 0), (vert_coor, self.rect.height))

            self.dirty = True

        def get_dimensions_float(self) -> tuple:
            """Get the total number of cells in each dimension of the current grid, (m, n)"""
            return (self._grid_cells_n, self._grid_cells_m)

        def get_dimensions(self) -> tuple:
            """Get the total number of cells in each dimension of the current grid, (m, n)"""
            return (int(self._grid_cells_m), int(self._grid_cells_n))

        def get_screen_offset(self) ->tuple:
            """Get the screen 'buffer' edges of the grid. (offset)"""
            return (self._screen_edge_m, self._screen_edge_n)

        def _draw_diagonal_center_lines(self):
            """Debug function. Draws two lines, one top-left to bottom right, one top-right to bottom left, resulting in them crossing at the center of the screen"""
            pygame.draw.line(self.surface, (200, 40, 40), (0, 0), (self.rect.width, self.rect.height))
            pygame.draw.line(self.surface, (200, 40, 40), (0, self.rect.height), (self.rect.width, 0))



            


    

    # Settings
    background_colour = (220,220,220)
    line_colour = (60,60,60)
    cell_colour = (30,128,30)

    _grid_cells_m:float = 0.0
    _grid_cells_n:float = 0.0
    _line_dist:float = 0.0
    

    def __init__(self, screen_size:tuple, grid_cells_m:float, grid_cells_n:float, line_dist:float) -> None:
        
            self.screen_size = screen_size
            self._grid_cells_m = grid_cells_m
            self._grid_cells_n = grid_cells_n
            self._line_dist = line_dist

            self.grid = self.Grid(self.screen_size, grid_cells_m, grid_cells_n, line_dist, self.line_colour)
            self.cells = self.Cells(self.screen_size, grid_cells_m, grid_cells_n, line_dist, self.grid.get_screen_offset(), self.background_colour, self.cell_colour)


    def set_cells(self, cells:np.ndarray):
        self.cells.set_cells_array(cells)
    



    





class CellElement(ScreenElement):
    """Cell in the game of life, screen element"""

    def __init__(self, screen_size:tuple, grid_cells_m:int, grid_cells_n:int) -> None:
        super().__init__()

        self.screen_size = screen_size
        self._grid_cells_m:float = 0.0
        self._grid_cells_n:float = 0.0








class PauseButton(ScreenElement):
    """Pause button"""

    # Settings
    size_relative_to_screen_size = 1/24
    background_colour = (160,160,160)
    background_alpha_pause = 128
    background_alpha_play = 255
    foreground_colour = (80,80,80)
    foreground_alpha = 255
    
    # surface_play represents 'click here to begin playing', and dislays a play symbol
    surface_play:pygame.surface.Surface = None
    # surface_pause represents 'click here to pause', and displays a pause symbol
    surface_pause:pygame.surface.Surface = None


    def __init__(self, screen_size:tuple, pos = (0,0)) -> None:
        super().__init__()
        
        self.screen_size = screen_size
        self.size_scaled = max(self.screen_size[0], self.screen_size[1]) * self.size_relative_to_screen_size
        self.rect = pygame.rect.Rect(0, 0, self.size_scaled, self.size_scaled)

        self.surface_pause = self._build_surface([self._create_background_pause(), self._create_symbol_pause()])
        self.surface_play = self._build_surface([self._create_background_play(), self._create_symbol_play()])

        self.playing = True
        self.set_surface(not self.playing)

        

    def set_surface(self, playing:bool):
        if self.playing != playing:
            if playing:
                self.surface = self.surface_pause
            else:
                self.surface = self.surface_play
            self.playing = playing
            self.dirty = True


    def _build_surface(self, surfaces:list[pygame.surface.Surface]) -> pygame.surface.Surface:
        r_surface = self._get_surface_transparent()
        for i in range(len(surfaces)):
            r_surface.blit(surfaces[i], surfaces[i].get_rect())
        return r_surface

        
    def _get_surface_transparent(self, size:tuple = None) -> pygame.surface.Surface:
        if size == None: size = self.rect.size
        r_surface = pygame.surface.Surface(size, pygame.SRCALPHA)
        return r_surface


    def _create_background_play(self) -> pygame.surface.Surface:
        background_play = self._get_surface_transparent()
        pygame.draw.circle(background_play, self.foreground_colour, self.rect.center, min(self.rect.centerx, self.rect.centery))
        background_play.set_alpha(self.background_alpha_play)
        return background_play


    def _create_background_pause(self) -> pygame.surface.Surface:
        background_pause = self._get_surface_transparent()
        pygame.draw.circle(background_pause, self.background_colour, self.rect.center, min(self.rect.centerx, self.rect.centery))
        background_pause.set_alpha(self.background_alpha_pause)
        return background_pause


    def _create_symbol_play(self) -> pygame.surface.Surface:
        symbol_play = self._get_surface_transparent()

        # symbol settings
        width = 1/2
        height = 1/2

        width *= self.rect.width * 0.5
        height *= self.rect.height * 0.5
        pygame.draw.polygon(
            symbol_play,
            self.background_colour,
            [
                (self.rect.centerx - (width * 0.5), self.rect.centery - (height * 0.866)),
                (self.rect.centerx + width, self.rect.centery),
                (self.rect.centerx - (width * 0.5), self.rect.centery + (height * 0.866))
            ]
        )
        return symbol_play


    def _create_symbol_pause(self) -> pygame.surface.Surface:
        symbol_pause = self._get_surface_transparent()
        
        # symbol settings
        line_height = 1/2
        line_spacing = 1/4
        line_thickness = 1/12

        line_height *= self.rect.height * 0.5
        line_spacing *= self.rect.width * 0.5
        line_thickness *= self.rect.width * 0.5
        pygame.draw.line(
            symbol_pause,
            self.foreground_colour,
            (self.rect.centerx - line_spacing, self.rect.centery - line_height),
            (self.rect.centerx - line_spacing, self.rect.centery + line_height),
            int(line_thickness * 2)
        )
        pygame.draw.line(
            symbol_pause,
            self.foreground_colour,
            (self.rect.centerx + line_spacing, self.rect.centery - line_height),
            (self.rect.centerx + line_spacing, self.rect.centery + line_height),
            int(line_thickness * 2)
        )
        symbol_pause.set_alpha(self.foreground_alpha)
        return symbol_pause

    
    
    



    # old version, no longer used
    def create_surface(self, size_scale:float):
        
        size = max(self.screen_size[0], self.screen_size[1]) * size_scale

        self.surface = pygame.surface.Surface((size, size), pygame.SRCALPHA)
        #self.surface.convert_alpha()
        if self.rect == None:
            self.rect = self.surface.get_rect()
        else:
            self.rect.size = self.surface.get_rect().size

        #TODO remove, test, center lines
        #pygame.draw.line(self.surface, (200,40,40), self.rect.midleft, self.rect.midright)
        #pygame.draw.line(self.surface, (200,40,40), self.rect.midtop, self.rect.midbottom)

        # Background circle
        background_circle = pygame.surface.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.circle(background_circle, self.background_colour, self.rect.center, self.rect.centerx)
        background_circle.set_alpha(self.background_alpha)

        # Pause symbol
        pause_line_height = 1/2
        pause_line_spacing = 1/4
        pause_line_thickness = 1/12
        pause_symbol = pygame.surface.Surface(self.rect.size, pygame.SRCALPHA)
        pause_symbol.fill((255,0,255))
        pause_symbol.set_colorkey((255,0,255))
        pause_line_height *= self.rect.height * 0.5
        pause_line_spacing *= self.rect.width * 0.5
        pause_line_thickness *= self.rect.width * 0.5
        pygame.draw.line(
            pause_symbol,
            self.foreground_colour,
            (self.rect.centerx - pause_line_spacing, self.rect.centery - pause_line_height),
            (self.rect.centerx - pause_line_spacing, self.rect.centery + pause_line_height),
            int(pause_line_thickness * 2)
        )
        pygame.draw.line(
            pause_symbol,
            self.foreground_colour,
            (self.rect.centerx + pause_line_spacing, self.rect.centery - pause_line_height),
            (self.rect.centerx + pause_line_spacing, self.rect.centery + pause_line_height),
            int(pause_line_thickness * 2)
        )
        pause_symbol.set_alpha(self.foreground_alpha)

        self.surface.blit(background_circle, (0,0))
        self.surface.blit(pause_symbol, (0,0))

        self.dirty = True

        





