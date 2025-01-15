from Utils.Graphics import Graphic
from Class.Button import Button
from Enums.GameState import GameState

class Menu:
    def __init__(self, name: str, buttons: list, WIDTH=400,HEIGHT=300):
        """
        Create a Menu instance

        Params:
        - name : str
            the name of the menu
        - buttons : [Button]
            the buttons of the menu
        - WIDTH = 400 : int
            the width of the menu
        - HEIGHT = 300 : int
            the height of the menu
        """
        self.name = name
        self.buttons = buttons
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.caneva = Graphic((WIDTH, HEIGHT))

    def draw_menu(self):
        """
        Draw the menu on the caneva
        """
        for button in self.buttons:
            button.draw_button(self.caneva)

    def show_menu(self):
        """
        Return the image of the menu

        Returns:
        - Graphic
            the image of the menu
        """
        return self.caneva.get_image()


def create_Menu_Main(WIDTH, HEIGHT):
    """
    Create the main menu

    Params:
    - WIDTH : int
        the width of the screen
    - HEIGHT : int
        the height of the screen
    """
    Play = Button("Play", 10, round(HEIGHT/6), round(WIDTH/8), round(HEIGHT/6), button_play)
    Quit = Button("Exit", round(6.9*WIDTH/8), round(HEIGHT/6), round(WIDTH/8), round(HEIGHT/6), button_quit)
    buttons = [Play, Quit]
    Main = Menu("Main", buttons)
    Main.draw_menu()
    return Main

def create_Menu_Pause(WIDTH, HEIGHT):
    """
    Create the pause menu

    Params:
    - WIDTH : int
        the width of the screen
    - HEIGHT : int
        the height of the screen
    """
    Resume = Button("Resume", 10, round(HEIGHT/6), round(WIDTH/8), round(HEIGHT/6), button_play)
    Quit = Button("Quit", 10, round(4*HEIGHT/6), round(WIDTH/8), round(HEIGHT/6), button_main)
    buttons = [Resume, Quit]
    Pause = Menu("Pause", buttons)
    Pause.draw_menu()
    return Pause

def create_Menu_Play(WIDTH, HEIGHT):
    """
    Create the play menu

    Params:
    - WIDTH : int
        the width of the screen
    - HEIGHT : int
        the height of the screen
    """
    Pause = Button("Pause", round(6.9*WIDTH/8), 10, round(WIDTH/8), round(HEIGHT/6), button_pause)
    buttons = [Pause]
    Play = Menu("Play", buttons)
    Play.draw_menu()
    return Play

def create_Menu_End(WIDTH, HEIGHT):
    """
    Create the end menu

    Params:
    - WIDTH : int
        the width of the screen
    - HEIGHT : int
        the height of the screen
    """
    Restart = Button("Restart", 10, round(4*HEIGHT/6), round(WIDTH/8), round(HEIGHT/6), button_play)
    Main = Button("Main", round(6.9*WIDTH/8), round(4*HEIGHT/6), round(WIDTH/8), round(HEIGHT/6), button_main)
    buttons = [Restart, Main]
    End = Menu("End", buttons)
    End.draw_menu()
    return End

def create_Menu_Leaderboard(WIDTH, HEIGHT):
    """
    Create the leaderboard menu

    Params:
    - WIDTH : int
        the width of the screen
    - HEIGHT : int
        the height of the screen
    """
    caneva = Graphic((WIDTH, HEIGHT))
    #caneva.draw_rectangle((x1, y1), (x2, y2), (200, 200, 200), 3)
    #caneva.draw_text(name, (((x1+x2)/2-(len(name))), ((y1+y2)/2-(len(name)))), 'Hollster.ttf', 30   , (200, 200, 200), 3, center = True)
  
    #return Leaderboard
    pass

def create_Menu_All(WIDTH, HEIGHT):
    """
    Create all the menus

    Params:
    - WIDTH : int
        the width of the screen
    - HEIGHT : int
        the height of the screen
    """
    Main = create_Menu_Main(WIDTH, HEIGHT)
    Pause = create_Menu_Pause(WIDTH, HEIGHT)
    Play = create_Menu_Play(WIDTH, HEIGHT)
    End = create_Menu_End(WIDTH, HEIGHT)
    return Main, Pause, Play, End


def button_main():
    """
    Action of the main button

    Returns:
    - GameState
        the new game state : MainMenu
    """
    print("main")    
    return GameState.MainMenu 


def button_pause():
    """
    Action of the pause button

    Returns:
    - GameState
        the new game state : PauseMenu
    """
    print("pause")
    return GameState.PauseMenu 
    
def button_play():
    """
    Action of the play button

    Returns:
    - GameState
        the new game state : Playing
    """
    print("play") 
    return GameState.Playing

def button_quit():
    """
    Action of the quit button

    Returns:
    - GameState
        the new game state : Stop
    """
    print('quit')
    return GameState.Stop
