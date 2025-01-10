
import cv2
from Graphics import Graphic, SceneRender
from Button import Button
from GameState import GameState

class Menu:
    def __init__(self, name: str, buttons: list, WIDTH=400,HEIGHT=300):
        self.name = name
        self.buttons = buttons
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.caneva = Graphic((WIDTH, HEIGHT))

    def draw_menu(self):
        for button in self.buttons:
            button.draw_button(self.caneva)

    def show_menu(self):
        return self.caneva.get_image()

def create_Menu_Main(WIDTH, HEIGHT):
    Play = Button("Play", 10, round(HEIGHT/6), round(WIDTH/8), round(HEIGHT/6), button_play)
    Quit = Button("Exit", round(6.9*WIDTH/8), round(HEIGHT/6), round(WIDTH/8), round(HEIGHT/6), button_quit)
    buttons = [Play, Quit]
    Main = Menu("Main", buttons)
    Main.draw_menu()
    return Main

def create_Menu_Pause(WIDTH, HEIGHT):
    Resume = Button("Resume", 10, round(HEIGHT/6), round(WIDTH/8), round(HEIGHT/6), button_play)
    Quit = Button("Quit", 10, round(4*HEIGHT/6), round(WIDTH/8), round(HEIGHT/6), button_main)
    buttons = [Resume, Quit]
    Pause = Menu("Pause", buttons)
    Pause.draw_menu()
    return Pause

def create_Menu_Play(WIDTH, HEIGHT):
    Pause = Button("Pause", round(6.9*WIDTH/8), 10, round(WIDTH/8), round(HEIGHT/6), button_pause)
    buttons = [Pause]
    Play = Menu("Play", buttons)
    Play.draw_menu()
    return Play

def create_Menu_End(WIDTH, HEIGHT):
    Restart = Button("Restart", 10, round(4*HEIGHT/6), round(WIDTH/8), round(HEIGHT/6), button_play)
    Main = Button("Main", round(6.9*WIDTH/8), round(4*HEIGHT/6), round(WIDTH/8), round(HEIGHT/6), button_main)
    buttons = [Restart, Main]
    End = Menu("End", buttons)
    End.draw_menu()
    return End

def create_Menu_Leaderboard(WIDTH, HEIGHT):
    caneva = Graphic((WIDTH, HEIGHT))
    #caneva.draw_rectangle((x1, y1), (x2, y2), (200, 200, 200), 3)
    #caneva.draw_text(name, (((x1+x2)/2-(len(name))), ((y1+y2)/2-(len(name)))), 'Hollster.ttf', 30   , (200, 200, 200), 3, center = True)
  
    #return Leaderboard
    pass

def create_Menu_All(WIDTH, HEIGHT):
    Main = create_Menu_Main(WIDTH, HEIGHT)
    Pause = create_Menu_Pause(WIDTH, HEIGHT)
    Play = create_Menu_Play(WIDTH, HEIGHT)
    End = create_Menu_End(WIDTH, HEIGHT)
    return Main, Pause, Play, End


def button_main():
    print("main")    
    return GameState.MainMenu 
def button_pause():
    print("pause")
    return GameState.PauseMenu 
    
def button_play():
    print("play") 
    return GameState.Playing

def button_quit():
    print('quit')
    return GameState.MainMenu
