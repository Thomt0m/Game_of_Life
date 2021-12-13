# General settings

class Settings:



    class GameOfLifeSettings:

        def __init__(self) -> None:
            self.tick_interval = 0.500
            self.grid_cells_screen = 80




    


    def __init__(self) -> None:
        self.gol = Settings.GameOfLifeSettings()