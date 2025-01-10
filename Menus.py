
import cv2
from Graphics import Graphic, SceneRender
from Button import Button
from GameState import GameState

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

def create_Menu_Main():
    Play = Button("Play", 10, 100, 260, 200, button_play)
    Quit = Button("Exit", 10, 400, 260, 500, button_quit)
    buttons = [Play, Quit]
    Main = Menu("Main", buttons)
    Main.draw_menu()
    return Main

def create_Menu_Pause():
    Resume = Button("Resume", 500, 50, 700, 150, button_play)
    Quit = Button("Quit", 500, 450, 700, 550, button_main)
    buttons = [Resume, Quit]
    Pause = Menu("Pause", buttons)
    Pause.draw_menu()
    return Pause

def create_Menu_Play():
    Pause = Button("Pause", 0, 0, 100, 100, button_pause)
    buttons = [Pause]
    Play = Menu("Play", buttons)
    Play.draw_menu()
    return Play

def create_Menu_End():
    Restart = Button("Restart", 10, 100, 260, 200, button_play)
    Main = Button("Main", 10, 400, 260, 500, button_main)
    buttons = [Restart, Main]
    End = Menu("End", buttons)
    End.draw_menu()
    return End

def create_Menu_All():
    Main = create_Menu_Main()
    Pause = create_Menu_Pause()
    Play = create_Menu_Play()
    End = create_Menu_End()
    return Main, Pause, Play, End


def button_main():
    global gameState
    print("main")    
    gameState = GameState.MainMenu 
    return

def button_pause():
    global gameState
    print("pause")
    gameState = GameState.PauseMenu 
    return

def button_play():
    global gameState
    print("play")
    gameState = GameState.Playing 
    return

def button_quit():
    global gameState
    print('quit')
    gameState = GameState.MainMenu
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

Main, Pause, Play, End = create_Menu_All()

def camera():
    global mouse_x, mouse_y
    global gameState
    EPSILON = 1
    gameState = GameState.MainMenu
 
    # Initialisation des coordonnées de la souris
    mouse_x, mouse_y = -1, -1
    
    cap = cv2.VideoCapture(0)
    
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
        img = cv2.resize(img, (WIDTH, HEIGHT))
        img = cv2.flip(img, 1)
        key = cv2.waitKey(EPSILON) & 0xFF
        
        render.clear()

        if gameState == GameState.PauseMenu:
            render.add_layer(img)            
            render.add_layer(Pause.show_menu())

            for bu in Pause.buttons:
                if bu.isClicked(mouse_x, mouse_y): #Changer x, y
                    bu.click()

        elif gameState == GameState.Playing:
            render.add_layer(img)            
            render.add_layer(Play.show_menu())

            for bu in Play.buttons:
                if bu.isClicked(mouse_x, mouse_y): #Changer x, y
                    bu.click()

        elif gameState == GameState.EndMenu:
            render.add_layer(img)            
            render.add_layer(End.show_menu())

            for bu in End.buttons:
                if bu.isClicked(mouse_x, mouse_y): #Changer x, y
                    bu.click()

        elif gameState == GameState.MainMenu:
            render.add_layer(img)
            render.add_layer(Main.show_menu())

            for bu in Main.buttons:
                if bu.isClicked(mouse_x, mouse_y): #Changer x, y
                    bu.click()

        if key == ord("q") or key == 27:
            break
      
        output = render.get_image()
        cv2.imshow("Main", output)
        
        if mouse_x == -1 and mouse_y == -1:  
            cv2.setMouseCallback("Main", mouse_callback)


    cv2.destroyAllWindows()

if __name__ == "__main__":
    camera()