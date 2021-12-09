import pygame
from pygame import surface















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


    def __init__(self, screen_size:tuple, line_density:int) -> None:
        super().__init__()

        self.screen_size = screen_size
        self.create_grid(line_density)


    def update(self):
        if self.dirty:
            # do someting, if desired (currently just a placeholder)
            pass


    def create_grid(self, line_density:int):
        """Create the background-grid surface"""
        self.surface = pygame.surface.Surface(self.screen_size)
        self.rect = self.surface.get_rect()
        
        self.surface.fill(self.background_colour)
        
        #TODO remove, test, two diagonal lines which cross eachother in the center of the screen
        #pygame.draw.line(self.surface, (200, 40, 40), (0, 0), (self.rect.width, self.rect.height))
        #pygame.draw.line(self.surface, (200, 40, 40), (0, self.rect.height), (self.rect.width, 0))

        if line_density < 1 or line_density == None: line_density = 80

        if (self.rect.width > self.rect.height):
            line_dist = self.rect.height / line_density
        else:
            line_dist = self.rect.width / line_density
        print("line_dist = " + str(line_dist))

        # Draw the horizontal lines
        hor_lines_float = self.rect.height / line_dist
        hor_lines = int(hor_lines_float)
        hor_edge = hor_lines_float - hor_lines
        if hor_edge < 0.5: hor_edge += 1
        hor_edge *= 0.5 * line_dist
        for i in range(0, hor_lines + 1):
            hor_coor = (line_dist * i) + hor_edge
            pygame.draw.line(self.surface, self.line_colour, (0, hor_coor), (self.rect.width, hor_coor))

        # Draw the vertical lines
        vert_lines_float = self.rect.width / line_dist
        vert_lines = int(vert_lines_float)
        vert_edge = vert_lines_float - vert_lines
        if vert_edge < 0.5: vert_edge += 1
        vert_edge *= 0.5 * line_dist
        for i in range(0, vert_lines + 1):
            vert_coor = (line_dist * i) + vert_edge
            pygame.draw.line(self.surface, self.line_colour, (vert_coor, 0), (vert_coor, self.rect.height))

        self.dirty = True

            
    # TODO determine if this is a desired feature or more hassle than it is worth
    def resize_grid(self, size_increase:int):
        """Resize the grid, NOT IMPLEMENTED"""
        pass








class CellElement(ScreenElement):
    """Cell in the game of life, screen element"""

    # Settings
    colour = (40, 200, 200)

    def __init__(self, size:int) -> None:
        super().__init__()








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
        
        debug_message = 'play'
        if self.playing: debug_message = 'pause'
        print('changing surface to ' + debug_message)



    

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

        








class Layer:

    name:str = ""
    elements:list[ScreenElement] = []

    def __init__(self, name:str, elements:list[ScreenElement] = []):
        self.name = name
        self.elements = elements.copy()