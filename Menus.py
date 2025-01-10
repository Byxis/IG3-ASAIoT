
import cv2
from Graphics import Graphic, SceneRender
import numpy as np

class Menu:
    def __init__(self, name: str, buttons: list, WIDTH=800,HEIGHT=600):
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

class Button:
    def __init__(self, name: str, x1, y1, x2, y2, action=None):
        self.name = name
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.action = action

    def isClicked(self, pos_x=-1, pos_y=-1):
        return self.x1 <= pos_x <= self.x2 and self.y1 <= pos_y <= self.y2

    def click(self):
        if self.action:
            self.action()

    def draw_button(self,caneva):
        caneva.draw_rectangle((self.x1, self.y1), (self.x2, self.y2), (200, 200, 200), 3)
        caneva.draw_text(self.name, (((self.x1+self.x2)/2-(len(self.name))), ((self.y1+self.y2)/2-(len(self.name)))), 'Hollster.ttf', 30   , (200, 200, 200), 3, center = True)
  

def create_Home():
    Play = Button("Play", 10, 100, 260, 200, play)
    Quit = Button("Exit", 10, 400, 260, 500, quit)
    buttons = [Play, Quit]
    Home = Menu("Home", buttons)
    return Home

def create_Pause():
    Resume = Button("Resume", 500, 50, 700, 150, resume)
    Quit = Button("Quit", 500, 450, 700, 550, quit)
    buttons = [Resume, Quit]
    Pause = Menu("Pause", buttons)
    return Pause

def create_Game():
    Pause = Button("Pause", 0, 0, 100, 100, pause)
    buttons = [Pause]
    Game = Menu("Game", buttons)
    return Game

def create_End():
    Restart = Button("Restart", 10, 100, 260, 200, restart)
    Main = Button("Main", 10, 400, 260, 500, main)
    buttons = [Restart, Main]
    End = Menu("End", buttons)
    return End

def resume():
    print('resume')
    return

def quit():
    print('savequit')
    return

def play():
    print("play")
    return

def pause():
    print("pause")
    return

def restart():
    print("restart")
    return

def main():
    print("main")
    return

# Fonction de rappel pour la souris
def mouse_callback(event, x, y, flags, param):
    global mouse_x, mouse_y
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_x, mouse_y = x, y

WIDTH, HEIGHT = 800, 600

caneva = Graphic((WIDTH, HEIGHT))
render = SceneRender((WIDTH, HEIGHT))
render.clear()

render.add_layer(caneva.get_image())
Home = create_Home()
Pause = create_Pause()
Game = create_Game()
End = create_End()


Home.draw_menu()
Pause.draw_menu()
Game.draw_menu()
End.draw_menu()

def camera():
    global mouse_x, mouse_y
    EPSILON = 1
 
    # Initialisation des coordonnées de la souris
    mouse_x, mouse_y = -1, -1

    pause_mode = False  # Contrôleur pour savoir si nous sommes dans le mode Pause
    game_mode = False
    end_mode = False
    
    
    cap = cv2.VideoCapture(0)
    
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
        img = cv2.resize(img, (WIDTH, HEIGHT))
        img = cv2.flip(img, 1)
        key = cv2.waitKey(EPSILON) & 0xFF

        
        render.clear()

        if pause_mode:
            render.add_layer(img)            
            render.add_layer(Pause.show_menu())

            for bu in Pause.buttons:
                if bu.isClicked(mouse_x, mouse_y): #Changer x, y
                    bu.click()

        elif game_mode:
            render.add_layer(img)            
            render.add_layer(Game.show_menu())

            for bu in Game.buttons:
                if bu.isClicked(mouse_x, mouse_y): #Changer x, y
                    bu.click()

        elif end_mode:
            render.add_layer(img)            
            render.add_layer(End.show_menu())

            for bu in End.buttons:
                if bu.isClicked(mouse_x, mouse_y): #Changer x, y
                    bu.click()

        else :
            render.add_layer(img)
            render.add_layer(Home.show_menu())

            for bu in Home.buttons:
                if bu.isClicked(mouse_x, mouse_y): #Changer x, y
                    bu.click()

            if key == ord("p"):     #Game State
                pause_mode = not pause_mode 

            if key == ord("g"):     #Game State
                game_mode = not game_mode

            if key == ord("e"):     #Game State
                end_mode = not end_mode

        if key == ord("q") or key == 27:
            break
      
        output = render.get_image()
        cv2.imshow("Home", output)
        
        if mouse_x == -1 and mouse_y == -1:  
            cv2.setMouseCallback("Home", mouse_callback)


    cv2.destroyAllWindows()

if __name__ == "__main__":
    camera()