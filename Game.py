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
from WasteType import WasteType
import threading
from WasteFall import *

class Game:
    def __init__(self, player):
        self.player = Player(player)
        self.activeWasteList = []
        self.gameState = GameState.MainMenu
        self.indexPos = []
        self.mouse = [-100, -100]
        self.mouseDelay = 0.5
        self.mouseCurrentDelay = 0

    def play(self):
        # Initialisation
        self.EPSILON = 1
        self.WIDTH =  int(480*12/9) # 640 
        self.HEIGHT = 480 # 480

        Main, Pause, Play, End = create_Menu_All(self.WIDTH, self.HEIGHT)
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
            "Recycling": Bin("Recycling", WasteType.Recycling, self.HEIGHT),
            "Compost": Bin("Compost", WasteType.Compost, self.HEIGHT),
            "Glass": Bin("Glass", WasteType.Glass, self.HEIGHT),
            "Default": Bin("Default", WasteType.NonRecycling, self.HEIGHT),
            "Floor": Bin("Floor", WasteType.Floor, self.HEIGHT)
        }

        wasteDefaultDelay = 2
        wasteCurrentDelay = 0
        
        wasteCatalog = createWasteCatalog()
        wasteList = []
        
        while cap.isOpened():
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
            self.updateGameState(render, img, Main, Pause, Play, End)
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
                
                size = len(wasteList)
                indexPos = [-100, -100]
                render = updateAllWaste(render, wasteList, self.HEIGHT, self.WIDTH, wasteCatalog, wasteCurrentDelay, self.mouse, self.player)
                if size < len(wasteList):
                    wasteCurrentDelay = wasteDefaultDelay
                if(wasteCurrentDelay >= 0):
                    wasteCurrentDelay -= fps.dt*0.5
            # Affichage du jeu
            cv2.imshow("Jeu", output)

            # Temp : interruption du jeu
            key = cv2.waitKey(self.EPSILON) & 0xFF
            if key == ord("q") or key == 27:
                self.gameState = GameState.Stop
            
            if self.gameState == GameState.Stop:
                break

        cv2.destroyAllWindows()

    def updateGameState(self, render, img, Main, Pause, Play, End):
        menu_map = {
            GameState.PauseMenu: Pause,
            GameState.Playing: Play,
            GameState.EndMenu: End,
            GameState.MainMenu: Main
        }

        menu = menu_map.get(self.gameState, None)
        if menu:
            render.add_layer(img)
            render.add_layer(menu.show_menu())

            for bu in menu.buttons:
                    if bu.isClicked(self.mouse[0], self.mouse[1]):
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
                    self.mouse = hand.index[3]
                    self.mouseCurrentDelay = self.mouseDelay
        if(self.mouseCurrentDelay > 0):
            self.mouseCurrentDelay -= 0.1
            if self.mouseCurrentDelay <= 0:
                self.mouse = [-100, -100]
                

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
