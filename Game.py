import cv2
import numpy as np
from FPSCounter import FPSCounter
from GameState import GameState
import mediapipe as mp
from Hand import Hand
from HandGesture import HandGesture

class Game:
    def __init__(self, player):
        self.player = player
        self.activeWasteList = []
        self.binList = []
        self.gameState = GameState.Playing
    
    def play(self):
        #Initialisation
        EPSILON = 30
        cap = cv2.VideoCapture(0)
        fps = FPSCounter()
        handSolution = mp.solutions.hands
        hands = handSolution.Hands()

        while cap.isOpened():
            #Update image
            ret, img = cap.read()
            if not ret:
                break

            fps.update()        
            
            #Modification obligatoire
            img = cv2.resize(img, (800, 600))
            img = cv2.flip(img, 1)
            img = fps.display(img)

            if self.gameState == GameState.Playing:
                self.treatPicture(hands, img)

            #Affichage du jeu
            cv2.imshow("Jeu", img)

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
                handsList.append(Hand(handArticulations))
            
            for hand in handsList:
                # Détecter le geste de la main
                gesture = hand.getHandGesture()
                
                # Dessiner le geste reconnu
                x = hand.pos[0]
                y = hand.pos[1]
                cv2.circle(img, (x, y), 1, (255, 0, 255), cv2.FILLED)
                cv2.putText(img, f"{gesture.name}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                if(gesture == HandGesture.INDEX_RAISED):
                    x = hand.index[3][0]
                    y = hand.index[3][1]
                    cv2.circle(img, (x, y), 20, (255, 0, 0), cv2.FILLED)

            

if __name__ == "__main__":
    game = Game("Joueur")
    game.play()