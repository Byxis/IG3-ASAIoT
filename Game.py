import cv2
import numpy as np
from FPSCounter import FPSCounter
from GameState import GameState
import mediapipe as mp
from Hand import Hand
from HandGesture import HandGesture
from scipy.spatial import distance
from Graphics import Graphic, SceneRender
from Bin import Bin
from Menus import *
from Player import Player
from Direction import Direction

class Game:
    def __init__(self, player):
        self.player = player
        self.activeWasteList = []
        self.gameState = GameState.MainMenu
        self.indexPos = []
        self.bins = {}
        self.player = Player(player)
    
    def play(self):
        #Initialisation
        self.EPSILON = 1
        self.WIDTH = 400
        self.HEIGHT = 300
        
        Main, Pause, Play, End = create_Menu_All(self.WIDTH, self.HEIGHT)
        cap = cv2.VideoCapture(0)
        fps = FPSCounter()
        handSolution = mp.solutions.hands
        hands = handSolution.Hands()
        render = SceneRender((self.WIDTH, self.HEIGHT))
        self.bins = {"Recycling":Bin("Recycling", "recycling", self.HEIGHT), "Compost":Bin("Compost", "compost", self.HEIGHT), "Glass":Bin("Glass", "glass", self.HEIGHT), "Default":Bin("Default", "default", self.HEIGHT)}

        while cap.isOpened():
            #Update image
            ret, img = cap.read()
            if not ret:
                break
            img = cv2.flip(img, 1)
            img = cv2.resize(img, (self.WIDTH, self.HEIGHT))
            
            webcam = Graphic(img)
            webcam.resize((self.WIDTH, self.HEIGHT))
            output = render.get_image()

            render.clear()
            self.treatPicture(hands, img)

            if self.gameState == GameState.PauseMenu:
                render.add_layer(img)            
                render.add_layer(Pause.show_menu())
                
                if(len(self.indexPos) > 0):
                    if(self.indexPos[-1][2] > .8):
                        mouse_x, mouse_y = self.indexPos[0][0:2]
                    for bu in Pause.buttons:
                        if bu.isClicked(mouse_x, mouse_y): #Changer x, y
                            self.gameState = bu.click()

            elif self.gameState == GameState.Playing:
                render.add_layer(img)            
                render.add_layer(Play.show_menu())

                if(len(self.indexPos) > 0):
                    if(self.indexPos[-1][2] > .8):
                        mouse_x, mouse_y = self.indexPos[0][0:2]
                    for bu in Play.buttons:
                        if bu.isClicked(mouse_x, mouse_y): #Changer x, y
                            self.gameState = bu.click()

            elif self.gameState == GameState.EndMenu:
                render.add_layer(img)            
                render.add_layer(End.show_menu())

                if(len(self.indexPos) > 0):
                    if(self.indexPos[-1][2] > .8):
                        mouse_x, mouse_y = self.indexPos[0][0:2]
                    for bu in End.buttons:
                        if bu.isClicked(mouse_x, mouse_y): #Changer x, y
                            self.gameState = bu.click()
                            

            elif self.gameState == GameState.MainMenu:
                render.add_layer(img)
                render.add_layer(Main.show_menu())

                if(len(self.indexPos) > 0):
                    if(self.indexPos[-1][2] > 0.8):
                        mouse_x, mouse_y = self.indexPos[0][0:2]         
                    for bu in Main.buttons:
                        if bu.isClicked(mouse_x, mouse_y): #Changer x, y
                            self.gameState = bu.click()

            indexTrace = Graphic((self.WIDTH, self.HEIGHT))
            for pos in self.indexPos:
                indexTrace.draw_circle((pos[0], pos[1]), 5, (255, 0, 0), -1, alpha=pos[2])
                pos[2] -= 0.1
                if(pos[2] <= 0):
                    self.indexPos.remove(pos)

            #Alls Update
            fps.update()   

            #Render Update  
            render.add_layer(indexTrace)

            #Display
            output = fps.display(output)


            if(self.player.leftHand != None):
                render.add_layer(self.player.leftHand.sprite, [self.player.leftHand.pos[0], self.player.leftHand.pos[1]])
            if(self.player.rightHand != None):
                render.add_layer(self.player.rightHand.sprite, [self.player.rightHand.pos[0], self.player.rightHand.pos[1]])

            output = cv2.resize(output, (800, 600), interpolation=cv2.INTER_LANCZOS4)

            #Affichage du jeu
            cv2.imshow("Jeu", output)

            #Temp : interruption du jeu
            key = cv2.waitKey(self.EPSILON) & 0xFF
            if key == ord("q") or key == 27:
                break

        cv2.destroyAllWindows()
    
    def displayPlayerBins():
        pass

    def displayActiveWastes():
        pass

    def displayScore():
        pass

    def displayMainMenu():
        pass

    def displayPauseMenu():
        pass

    def displayEndMenu():
        pass

    def HandDetection():
        pass

    def treatPicture(self, hands, img):
        recHands = hands.process(img)
        handsList = []
        if recHands.multi_hand_landmarks:
            for hand in recHands.multi_hand_landmarks:
                handArticulations = []
                for datapoint_id, point in enumerate(hand.landmark):
                    h, w, c = img.shape
                    x, y = int(point.x * w), int(point.y * h)
                    handArticulations.append([x, y])
                    #cv2.circle(img, (x, y), 10, (255, 0, 255), cv2.FILLED)
                handsList.append(Hand(handArticulations))
            
            for i in range(0, len(handsList)):
                hand = handsList[i]
                # Détecter le geste de la main
                gesture = hand.getHandGesture()
                
                # Dessiner le geste reconnu
                x = hand.pos[0]
                y = hand.pos[1]
                
                bin = None
                if(gesture == HandGesture.FIST_CLOSED):
                    bin = self.bins["Compost"]
                elif(gesture == HandGesture.HAND_OPEN):
                    bin = self.bins["Glass"]
                elif(gesture == HandGesture.OK_SIGN):
                    bin = self.bins["Default"]
                elif(gesture == HandGesture.ROCK_N_ROLL):
                    bin = self.bins["Recycling"]
                elif(gesture == HandGesture.NONE):
                    bin = None


                if(hand.getHandDirection() == Direction.LEFT and bin != None):
                    self.player.changeBin(Direction.LEFT, bin)
                    self.player.leftHand.pos = [x, self.HEIGHT - 75]
                elif (bin != None):
                    self.player.changeBin(Direction.RIGHT, bin)
                    self.player.rightHand.pos = [x, self.HEIGHT - 75]
                else :
                    self.player.changeBin(hand.getHandDirection(), None)
                


                #cv2.circle(img, (x, y), 1, (255, 0, 255), cv2.FILLED)
                cv2.putText(img, f"{gesture.name} ", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
                #cv2.putText(img, f"{distance.euclidean(hand.index[0], hand.index[3])} > {hand.scale}", (x, y+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                if(gesture == HandGesture.INDEX_RAISED):
                    self.indexPos.append([hand.index[3][0], hand.index[3][1], 1])
                    #cv2.circle(img, (x, y), 20, (255, 0, 0), cv2.FILLED)

            

if __name__ == "__main__":
    game = Game("Joueur")
    print("Game created")
    game.play()