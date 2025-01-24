
import cv2
from Graphics import Graphic, SceneRender
from Button import Button
from Frame import Frame
from GameState import GameState

class Menu:
    def __init__(self, name: str = "Guest", buttons: list = None, frames: list = None, player_score:int = None, WIDTH=400, HEIGHT=300):
        self.name = name
        self.buttons = buttons
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.caneva = Graphic((WIDTH, HEIGHT))
        self.frames = frames
        self.player_score = player_score

    def draw_menu(self):
        if self.buttons :
            for button in self.buttons:
                button.draw_button(self.caneva)
        if self.frames :
            for frame in self.frames :
                frame.draw_title(self.caneva)
                frame.draw_frame(self.caneva)
        
    def show_menu(self):
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
    Play = Button("PLAY", 10, round(HEIGHT/6), round(2*WIDTH/8), round(HEIGHT/6), (0,255,0), button_play)
    Quit = Button("EXIT", round(5.9*WIDTH/8), round(HEIGHT/6), round(2*WIDTH/8), round(HEIGHT/6), (0,0,255), button_quit)
    buttons = [Play, Quit]
    LbFrame = Frame("Leaderboard",scores[:5], round(5.9*WIDTH/8), round((0.95*HEIGHT/2)-HEIGHT/11), round(2*WIDTH/8), round(HEIGHT/2))
    frames = [LbFrame]
    Main = Menu("Main", buttons=buttons, frames=frames, WIDTH=WIDTH, HEIGHT=HEIGHT)
    Main.draw_menu()
    return Main

def create_Menu_Pause(WIDTH, HEIGHT):
    Resume = Button("RESUME", 10, round(HEIGHT/6), round(2*WIDTH/8), round(HEIGHT/6), (0,255,0), button_play)
    Quit = Button("QUIT", 10, round(4*HEIGHT/6), round(2*WIDTH/8), round(HEIGHT/6), (0,0,255), button_main)
    buttons = [Resume, Quit]
    Pause = Menu("Pause", buttons=buttons, WIDTH=WIDTH, HEIGHT=HEIGHT)
    Pause.draw_menu()
    return Pause

def create_Menu_Play(WIDTH, HEIGHT, player_score):
    Pause = Button("PAUSE", round(6.9*WIDTH/8), 10, round(WIDTH/8), round(HEIGHT/6), (0,255,255), button_pause)
    buttons = [Pause]
    Play = Menu("Play", buttons=buttons, player_score=player_score, WIDTH=WIDTH, HEIGHT=HEIGHT)
    Play.draw_menu()
    return Play

def create_Menu_End(WIDTH, HEIGHT, scores, stats):
    Restart = Button("RESTART", round(5.9*WIDTH/8), round(HEIGHT/6), round(2*WIDTH/8), round(HEIGHT/6), (0,255,0), button_play)
    Main = Button("MAIN", round(5.9*WIDTH/8), round(4*HEIGHT/6), round(2*WIDTH/8), round(HEIGHT/6), (0,0,255), button_main)
    buttons = [Restart, Main]
    LbFrame = Frame("Leaderboard",scores[:5], 10, round(HEIGHT/6), round(2*WIDTH/8), round(4*HEIGHT/6))
    StatFrame = Frame("Statistics",stats, round(2*WIDTH/6), round(HEIGHT/2), round(2*WIDTH/6), round(0.95*HEIGHT/2))
    frames = [LbFrame, StatFrame]
    End = Menu("End", buttons=buttons, frames=frames, WIDTH=WIDTH, HEIGHT=HEIGHT)
    End.draw_menu()
    return End

def create_Menu_All(WIDTH, HEIGHT, scores,  stats, player_score):
    Main = create_Menu_Main(WIDTH, HEIGHT, scores)
    Pause = create_Menu_Pause(WIDTH, HEIGHT)
    Play = create_Menu_Play(WIDTH, HEIGHT, player_score)
    End = create_Menu_End(WIDTH, HEIGHT, scores, stats)
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
    return GameState.Stop
