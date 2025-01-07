import cv2
#from Game import Game
#from GameState import GameState
#from Hand import Hand

class Menu:
    
    def __init__(self,name:str,buttons:list,img):
        self.name = name
        self.buttons=buttons
        self.img = img


    def show_menu(self):
        for button in self.buttons :
            button.show_button()

        cv2.imshow(self.name,self.img)
    
class Button:

    def __init__(self,x1,y1,x2,y2,img):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.img = img

    def isClicked(self,pos_x,pos_y):
        if self.x1<=pos_x<=self.x2 and self.y1<=pos_y<=self.y2 :
            return True
        return False
    
    def show_button(self):
        cv2.rectangle(self.img, (self.x1, self.y1), (self.x2, self.y2), (200, 200, 200), 2)
        

def camera():
    EPSILON = 1
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
        img = cv2.resize(img, (800, 600))
        img = cv2.flip(img, 1)
        key = cv2.waitKey(EPSILON) & 0xFF

        #x,y = Hand(x), Hand(y)
        #if isClicked(x,y) :
            #Game()

        if key == ord("q") or key == 27:
            break
    cv2.destroyAllWindows()
    
if __name__ == "__Menus__":
    camera()
    
