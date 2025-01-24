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
import threading

class Game:
    def __init__(self, player):
        self.player = Player(player)
        self.activeWasteList = []
        self.gameState = GameState.MainMenu
        self.indexPos = []

    def play(self):
        # Initialisation
        self.EPSILON = 1
        self.WIDTH =  int(480*12/9) # 640 
        self.HEIGHT = 480 # 480

        Main, Pause, Play, End = create_Menu_All(self.WIDTH, self.HEIGHT,
                                                 scores = [["10/10/1010/10/10/10","Sebastien",10000],["10/10/1010/10/10/10","Tom",20],["10/10/1010/10/10/10","Tom",30],["10/10/1010/10/10/10","Tom",40], ["10/10/1010/10/10/10","Tom", 50],["10/10/1010/10/10/10","Tom",10],["10/10/1010/10/10/10","Tom",20],["10/10/1010/10/10/10","Tom",30],["10/10/1010/10/10/10","Tom",40], ["10/10/1010/10/10/10","Tom", 50]],
                                                 stats = [["NbWaste in right bin :",150],["Nb recycled wastes :",100],["1234567890AZERTYUIOPQSDFGHJKLMWXCVBN12345678"],["Nb non-recycled wastes :",100]],
                                                player_score=1000)       #A ENLEVER
        cv2.namedWindow("Jeu", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Jeu", self.WIDTH, self.HEIGHT)
        cv2.setUseOptimized(True)
        cv2.setNumThreads(4)

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.HEIGHT)
        cap.set(cv2.CAP_PROP_FPS, 30)
        fps = FPSCounter()
        handSolution = mp.solutions.hands
        hands = handSolution.Hands()
        render = SceneRender((self.WIDTH, self.HEIGHT))
        self.bins = {
            "Recycling": Bin("Recycling", "recycling", self.HEIGHT),
            "Compost": Bin("Compost", "compost", self.HEIGHT),
            "Glass": Bin("Glass", "glass", self.HEIGHT),
            "Default": Bin("Default", "default", self.HEIGHT)
        }
        
        player_score = 1000
        while cap.isOpened():
            player_score += 1
            # Update image
            ret, img = cap.read()
            if not ret:
                break
            img = cv2.flip(img, 1)
            webcam = Graphic(img)

            output = render.get_image()
            render.clear()

            render.add_layer(webcam)
            
            self.treatPicture(hands, img)

            indexTrace = Graphic((self.WIDTH, self.HEIGHT))
            self.updateGameState(render, img, Main, Pause, Play, End, player_score) #A ENLEVER
            for pos in self.indexPos:
                indexTrace.draw_circle((pos[0], pos[1]), 2, (255, 0, 0), -1, alpha=pos[2])
                pos[2] -= 0.1
                if pos[2] <= 0:
                    self.indexPos.remove(pos)

            # Alls Update
            fps.update()

            # Render Update
            render.add_layer(indexTrace)

            # Display
            output = fps.display(output)

            output = cv2.resize(output, (self.WIDTH*2, self.HEIGHT*2), interpolation=cv2.INTER_LINEAR)
            
            if self.gameState == GameState.Playing:
                self.renderBins(render)

            # Affichage du jeu
            cv2.imshow("Jeu", output)

            # Temp : interruption du jeu
            key = cv2.waitKey(self.EPSILON) & 0xFF
            if key == ord("q") or key == 27:
                self.gameState = GameState.Stop

            if key == ord("e"):                         #A ENLEVER
                self.gameState = GameState.EndMenu      #A ENLEVER
            if key == ord("p"):                         #A ENLEVER
                self.gameState = GameState.Playing      #A ENLEVER
            
            if self.gameState == GameState.Stop:
                break

        cv2.destroyAllWindows()

    def updateGameState(self, render, img, Main, Pause, Play, End, player_score=0):
        menu_map = {
            GameState.PauseMenu: Pause,
            GameState.Playing: Play,
            GameState.EndMenu: End,
            GameState.MainMenu: Main
        }

        menu = menu_map.get(self.gameState, None)
        if menu:
            render.add_layer(img)
            if menu == Play:
                menu.change_score(player_score)
                menu.show_score()
            render.add_layer(menu.show_menu())

            if len(self.indexPos) > 0 and self.indexPos[-1][2] > 0.8:
                mouse_x, mouse_y = self.indexPos[0][0:2]
                for bu in menu.buttons:
                    if bu.isClicked(mouse_x, mouse_y):
                        self.gameState = bu.click()

    def renderBins(self, render):
        if self.player.leftHand:
            render.add_layer(self.player.leftHand.sprite, [self.player.leftHand.pos[0], self.player.leftHand.pos[1]])
        if self.player.rightHand:
            render.add_layer(self.player.rightHand.sprite, [self.player.rightHand.pos[0], self.player.rightHand.pos[1]])

    def treatPicture(self, hands, img):
        recHands = hands.process(img)
        if recHands.multi_hand_landmarks:
            for hand in recHands.multi_hand_landmarks:
                handArticulations = []
                for datapoint_id, point in enumerate(hand.landmark):
                    h, w, c = img.shape
                    x, y = int(point.x * w), int(point.y * h)
                    handArticulations.append([x, y])

                hand = Hand(handArticulations)
                gesture = hand.getHandGesture()
                x, y = hand.pos

                bin = self.getBinForGesture(gesture)

                if hand.getHandDirection() == Direction.LEFT and bin:
                    self.player.changeBin(Direction.LEFT, bin)
                    self.player.leftHand.pos = [x, self.HEIGHT - 75]
                elif bin:
                    self.player.changeBin(Direction.RIGHT, bin)
                    self.player.rightHand.pos = [x, self.HEIGHT - 75]
                else:
                    self.player.changeBin(hand.getHandDirection(), None)

                cv2.putText(img, f"{gesture.name} ", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

                if gesture == HandGesture.INDEX_RAISED:
                    self.indexPos.append([hand.index[3][0], hand.index[3][1], 1])

    def getBinForGesture(self, gesture):
        bin_map = {
            HandGesture.FIST_CLOSED: "Compost",
            HandGesture.HAND_OPEN: "Glass",
            HandGesture.OK_SIGN: "Default",
            HandGesture.ROCK_N_ROLL: "Recycling",
            HandGesture.NONE: None
        }
        return self.bins.get(bin_map.get(gesture, None), None)

if __name__ == "__main__":
    game = Game("Joueur")
    print("Game created")
    game.play()
