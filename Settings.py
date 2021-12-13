
class Settings:

    class GameOfLifeSettings:

        def __init__(self) -> None:
            self.tick_interval = 0.500
            self.grid_cells_screen = 80


    class BackgroundGridSettings:

        def __init__(self) -> None:
            self.background_colour = (240,240,240)



    


    def __init__(self) -> None:
        self.gol = Settings.GameOfLifeSettings()
        self.background = Settings.BackgroundGridSettings()