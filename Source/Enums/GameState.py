from enum import Enum

class GameState(Enum):
    """
    Enum for the game state
    """
    MainMenu = 0
    Playing = 1
    PauseMenu = 2
    EndMenu = 3
    Stop = -1