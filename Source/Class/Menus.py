from Utils.Graphics import Graphic
from Class.Button import Button
from Class.Frame import Frame
from Enums.GameState import GameState

class Menu:
    def __init__(self, name: str = "Guest", buttons: list = None, frames: list = None, player_score:int = None, WIDTH=400, HEIGHT=300):
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
        self.frames = frames
        self.player_score = player_score

    def draw_menu(self):
        """
        Draw the menu on the caneva
        """
        if self.buttons :
            for button in self.buttons:
                button.draw_button(self.caneva)
        if self.frames :
            for frame in self.frames :
                frame.draw_title(self.caneva)
                frame.draw_frame(self.caneva)

    def show_menu(self):
        """
        Return the image of the menu

        Returns:
        - Graphic
            the image of the menu
        """
        return self.caneva.get_image()
    
    def show_score(self):
        self.caneva.draw_text(text = "Score : "+str(self.player_score), position= (round(self.WIDTH/2), round(self.HEIGHT/20)), font_path = 'Hollster.ttf', font_size = round((((self.WIDTH/64*len("Score : "+str(self.player_score)))**2+(self.HEIGHT/48)**2)**0.5)/2), color = (255,255,255), center = True)
    
    def change_score(self, player_score):
        self.player_score = player_score
        self.reset_menu()
    
    def clear_menu(self):
        self.caneva.reset_image()
        
    def reset_menu(self):
        self.clear_menu()
        self.draw_menu()


def create_Menu_Main(WIDTH, HEIGHT, scores):
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
    LbFrame = Frame("Leaderboard",scores[:5], round(5.9*WIDTH/8), round((0.95*HEIGHT/2)-HEIGHT/11), round(2*WIDTH/8), round(HEIGHT/2))
    frames = [LbFrame]
    Main = Menu("Main", buttons=buttons, frames=frames, WIDTH=WIDTH, HEIGHT=HEIGHT)
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

def create_Menu_Play(WIDTH, HEIGHT, player_score):
    """
    Create the play menu

    Params:
    - WIDTH : int
        the width of the screen
    - HEIGHT : int
        the height of the screen
    """
    Pause = Button("PAUSE", round(6.9*WIDTH/8), 10, round(WIDTH/8), round(HEIGHT/6), (0,255,255), button_pause)
    buttons = [Pause]
    Play = Menu("Play", buttons=buttons, player_score=player_score, WIDTH=WIDTH, HEIGHT=HEIGHT)
    Play.draw_menu()
    return Play

def create_Menu_End(WIDTH, HEIGHT, scores, stats):
    """
    Create the end menu

    Params:
    - WIDTH : int
        the width of the screen
    - HEIGHT : int
        the height of the screen
    """
    Restart = Button("RESTART", round(5.9*WIDTH/8), round(HEIGHT/6), round(2*WIDTH/8), round(HEIGHT/6), (0,255,0), button_play)
    Main = Button("MAIN", round(5.9*WIDTH/8), round(4*HEIGHT/6), round(2*WIDTH/8), round(HEIGHT/6), (0,0,255), button_main)
    buttons = [Restart, Main]
    LbFrame = Frame("Leaderboard",scores[:5], 10, round(HEIGHT/6), round(2*WIDTH/8), round(4*HEIGHT/6))
    StatFrame = Frame("Statistics",stats, round(2*WIDTH/6), round(HEIGHT/2), round(2*WIDTH/6), round(0.95*HEIGHT/2))
    frames = [LbFrame, StatFrame]
    End = Menu("End", buttons=buttons, frames=frames, WIDTH=WIDTH, HEIGHT=HEIGHT)
    End.draw_menu()
    return End

def create_Menu_All(WIDTH, HEIGHT, scores, stats, player_score):
    """
    Create all the menus

    Params:
    - WIDTH : int
        the width of the screen
    - HEIGHT : int
        the height of the screen
    """
    Main = create_Menu_Main(WIDTH, HEIGHT, scores)
    Pause = create_Menu_Pause(WIDTH, HEIGHT)
    Play = create_Menu_Play(WIDTH, HEIGHT, player_score)
    End = create_Menu_End(WIDTH, HEIGHT, scores, stats)
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
