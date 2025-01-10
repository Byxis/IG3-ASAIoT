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

class Game:
    def __init__(self, player):
        self.player = player
        self.activeWasteList = []
        self.binList = []
        self.gameState = GameState.Playing
        self.indexPos = []
        self.player = [[0,0], [0,0]]
    
    def play(self):
        #Initialisation
        EPSILON = 1
        WIDTH, HEIGHT = 400, 300

        cap = cv2.VideoCapture(0)
        fps = FPSCounter()
        handSolution = mp.solutions.hands
        hands = handSolution.Hands()
        render = SceneRender((WIDTH, HEIGHT))

        Bins = [Bin("Plastic", "plastic", HEIGHT), Bin("Paper", "paper", HEIGHT), Bin("Glass", "glass", HEIGHT), Bin("Other", "other", HEIGHT)]

        while cap.isOpened():
            #Update image
            ret, img = cap.read()
            if not ret:
                break

            img = cv2.flip(img, 1)

            webcam = Graphic(img)
            webcam.resize((WIDTH, HEIGHT))
            output = render.get_image()

            if self.gameState == GameState.Playing:
                self.treatPicture(hands, output)

            indexTrace = Graphic((WIDTH, HEIGHT))
            for pos in self.indexPos:
                indexTrace.draw_circle((pos[0], pos[1]), 5, (255, 0, 0), -1, alpha=pos[2])
                pos[2] -= 0.1
                if(pos[2] <= 0):
                    self.indexPos.remove(pos)
            
            Bins[0].updatePos(self.player[0])
            Bins[1].updatePos(self.player[1])

            #Alls Update
            fps.update()   

            #Render Update  
            render.clear()
            render.add_layer(webcam)
            render.add_layer(indexTrace)
            render.add_layer(Bins[0].sprite, Bins[0].pos)
            render.add_layer(Bins[1].sprite, Bins[1].pos)

            #Display
            output = fps.display(output)


            output = cv2.resize(output, (800, 600))
            #Affichage du jeu
            cv2.imshow("Jeu", output)

            #Temp : interruption du jeu
            key = cv2.waitKey(EPSILON) & 0xFF
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
                if(i < 2):
                    self.player[i] = [x, y]
                #cv2.circle(img, (x, y), 1, (255, 0, 255), cv2.FILLED)
                cv2.putText(img, f"{gesture.name} ", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
                #cv2.putText(img, f"{distance.euclidean(hand.index[0], hand.index[3])} > {hand.scale}", (x, y+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                if(gesture == HandGesture.INDEX_RAISED):
                    self.indexPos.append([hand.index[3][0], hand.index[3][1], 1])
                    #cv2.circle(img, (x, y), 20, (255, 0, 0), cv2.FILLED)

            

if __name__ == "__main__":
    game = Game("Joueur")
    game.play()