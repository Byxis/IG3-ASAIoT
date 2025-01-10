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
from Player import Player
from Direction import Direction

class Game:
    def __init__(self, player):
        self.player = player
        self.activeWasteList = []
        self.bins = {}
        self.gameState = GameState.Playing
        self.indexPos = []
        self.player = Player(player)
    
    def play(self):
        #Initialisation
        self.EPSILON = 1
        self.WIDTH = 400
        self.HEIGHT = 300

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

            webcam = Graphic(img)
            webcam.resize((self.WIDTH, self.HEIGHT))
            output = render.get_image()

            if self.gameState == GameState.Playing:
                self.treatPicture(hands, output)

            indexTrace = Graphic((self.WIDTH, self.HEIGHT))
            for pos in self.indexPos:
                indexTrace.draw_circle((pos[0], pos[1]), 5, (255, 0, 0), -1, alpha=pos[2])
                pos[2] -= 0.1
                if(pos[2] <= 0):
                    self.indexPos.remove(pos)

            #Alls Update
            fps.update()   

            #Render Update  
            render.clear()
            render.add_layer(webcam)
            render.add_layer(indexTrace)
            if(self.player.leftHand != None):
                render.add_layer(self.player.leftHand.sprite, self.player.leftHand.pos)
            if(self.player.rightHand != None):
                render.add_layer(self.player.rightHand.sprite, self.player.rightHand.pos)

            #Display
            output = fps.display(output)


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