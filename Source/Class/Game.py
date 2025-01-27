
from Enums.GameState import GameState
from Enums.HandGesture import HandGesture
from Enums.Direction import Direction
from Enums.WasteType import WasteType

from Utils.FPSCounter import FPSCounter
from Utils.Graphics import Graphic, SceneRender
from Utils.API_Raspberry import RaspberryAPI

from Class.Player import Player
from Class.Menus import *
from Class.WasteFall import *
from Class.Hand import Hand
from Class.Bin import Bin

import cv2
import numpy as np
import mediapipe as mp
from scipy.spatial import distance

class Game:
    def __init__(self, player):
        self.player = Player(player)
        self.activeWasteList = []
        self.gameState = GameState.MainMenu
        self.indexPos = []
        self.mouse = [-100, -100]
        self.mouseDelay = 0.5
        self.mouseCurrentDelay = 0
        self.raspberryApi = RaspberryAPI()

    def play(self):
        # Initialisation
        self.EPSILON = 1 # Waiting time for the next frame
        self.WIDTH =  int(480*12/9) # Width of the window
        self.HEIGHT = 480 # height of the window

        if(not self.raspberryApi.isLoaded):
            answer = input("Do you want to continue with a Raspberry ? If yes, please connect the Raspberry and type the url. If no,type 'enter' : ")
            if answer != "":
                self.raspberryApi.actualizeUrl(answer)

        # Creation of the window
        cv2.namedWindow("Jeu", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Jeu", self.WIDTH, self.HEIGHT)
        cv2.setUseOptimized(True)
        cv2.setNumThreads(4)

        # Crreation of the webcam
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.HEIGHT)
        cap.set(cv2.CAP_PROP_FPS, 30)

        # Initialisation of all the objects needed
        fps = FPSCounter() # FPS counter (to remove later)
        handSolution = mp.solutions.hands # Solution for hand detection
        hands = handSolution.Hands() # Hand detection object
        render = SceneRender((self.WIDTH, self.HEIGHT)) # Render engine

        # Creation of the bins
        self.bins = {
            "Recycling": Bin("Recycling",  WasteType.Recycling, self.HEIGHT),
            "Compost": Bin("Compost", WasteType.Compost, self.HEIGHT),
            "Glass": Bin("Glass", WasteType.Glass, self.HEIGHT),
            "Non Recycling": Bin("Non Recycling", WasteType.NonRecycling, self.HEIGHT),
            "Floor" : Bin("Floor", WasteType.Floor, self.HEIGHT)
        }

        # Creation of the menus
        Main, Pause, Play, End = create_Menu_All(
            self.WIDTH, self.HEIGHT,
            scores = [["10/10/1010/10/10/10","Sebastien",10000],
                      ["10/10/1010/10/10/10","Tom",20],
                      ["10/10/1010/10/10/10","Tom",30],
                      ["10/10/1010/10/10/10","Tom",40], 
                      ["10/10/1010/10/10/10","Tom",50],
                      ["10/10/1010/10/10/10","Tom",10],
                      ["10/10/1010/10/10/10","Tom",20],
                      ["10/10/1010/10/10/10","Tom",30],
                      ["10/10/1010/10/10/10","Tom",40], 
                      ["10/10/1010/10/10/10","Tom", 50]
                    ],
            stats = [
                ["NbWaste in right bin :",150],
                ["Nb recycled wastes :",100],
                ["1234567890AZERTYUIOPQSDFGHJKLMWXCVBN12345678"],
                ["Nb non-recycled wastes :",100]],
            player_score=0
        )  

        # Delay between waste spawn
        wasteDefaultDelay = 2
        wasteCurrentDelay = 0
        
        # Creation of the waste catalog and current waste list
        wasteCatalog = createWasteCatalog()
        wasteList = []
        
        while cap.isOpened():
            # Update image
            ret, img = cap.read()
            if not ret:
                break
            
            # Render and graphic initialization
            img = cv2.flip(img, 1)
            webcam = Graphic(img)

            output = render.get_image()
            render.clear()

            render.add_layer(webcam)
            
            # Hand detection
            self.treatPicture(hands, img)

            #Addind the index trace
            indexTrace = Graphic((self.WIDTH, self.HEIGHT))
            for pos in self.indexPos:
                indexTrace.draw_circle((pos[0], pos[1]), 2, (255, 0, 0), -1, alpha=pos[2])
                pos[2] -= 0.1
                if pos[2] <= 0:
                    self.indexPos.remove(pos)
            
            # Alls Update
            self.updateGameState(render, img, Main, Pause, Play, End, self.player.score)
            fps.update()
            if self.gameState == GameState.Playing:
                # Add bins to screen
                self.renderBins(render)
                
                # Handle waste spawn and collision
                size = len(wasteList)
                indexPos = [-100, -100]
                render = updateAllWaste(render, wasteList, self.HEIGHT, self.WIDTH, wasteCatalog, wasteCurrentDelay, self.mouse, self.player, self.raspberryApi)
                if size < len(wasteList):
                    wasteCurrentDelay = wasteDefaultDelay
                if(wasteCurrentDelay >= 0):
                    wasteCurrentDelay -= fps.dt*0.5


            # Display / Render Update
            render.add_layer(indexTrace)
            output = fps.display(output)
            output = cv2.resize(output, (self.WIDTH*2, self.HEIGHT*2), interpolation=cv2.INTER_LINEAR)
        
            # Affichage du jeu
            cv2.imshow("Jeu", output)

            # Stoping the game if the user touch the button for, or press "q" or "esc" 
            key = cv2.waitKey(self.EPSILON) & 0xFF
            if key == ord("q") or key == 27:
                self.gameState = GameState.Stop
            if self.gameState == GameState.Stop:
                break

        cv2.destroyAllWindows()

    def updateGameState(self, render, img, Main, Pause, Play, End, player_score = 0):
        """
        Update the game state and the menus

        Parameters:
        - render : SceneRender
            The render engine
        - img : np.array
            The image to treat
        - Main : Menu
            The main menu
        - Pause : Menu
            The pause menu
        - Play : Menu
            The play menu
        - End : Menu
            The end menu
        """
        menu_map = {
            GameState.PauseMenu: Pause,
            GameState.Playing: Play,
            GameState.EndMenu: End,
            GameState.MainMenu: Main
        }

        menu = menu_map.get(self.gameState, None)
        if menu:
            render.add_layer(img)
            if menu == Play and self.raspberryApi.isLoaded:
                menu.change_score(player_score)
                menu.show_score()
            render.add_layer(menu.show_menu())

            for bu in menu.buttons:
                if bu.isClicked(self.mouse[0], self.mouse[1]):
                    self.gameState = bu.click()

    def renderBins(self, render):
        """
        Add the bins to the render engine

        Parameters:
        - render : SceneRender
            The render engine
        """
        if self.player.leftHand:
            render.add_layer(self.player.leftHand.sprite, [self.player.leftHand.pos[0], self.player.leftHand.pos[1]])
        if self.player.rightHand:
            render.add_layer(self.player.rightHand.sprite, [self.player.rightHand.pos[0], self.player.rightHand.pos[1]])

    def treatPicture(self, hands, img):
        """
        Treat the picture to get the hand gesture and the mouse position

        Parameters:
        - hands : mediapipe.solutions.hands.Hands
            The hand detection object
        - img : np.array
            The image to treat
        """
        recHands = hands.process(img)
        if recHands.multi_hand_landmarks:
            for hand in recHands.multi_hand_landmarks:
                handArticulations = []
                # Get all the articulations of the hand
                for datapoint_id, point in enumerate(hand.landmark):
                    h, w, c = img.shape
                    x, y = int(point.x * w), int(point.y * h)
                    handArticulations.append([x, y])
                # Create a hand object
                hand = Hand(handArticulations)
                gesture = hand.getHandGesture()
                x, y = hand.pos

                bin = self.getBinForGesture(gesture)
                # Change the bin of the player
                if hand.getHandDirection() == Direction.LEFT and bin:
                    self.player.changeBin(Direction.LEFT, bin)
                    self.player.leftHand.pos = [x, self.HEIGHT - 75]
                elif bin:
                    self.player.changeBin(Direction.RIGHT, bin)
                    self.player.rightHand.pos = [x, self.HEIGHT - 75]
                else:
                    self.player.changeBin(hand.getHandDirection(), None)

                # Temp: Display the gesture on the screen
                cv2.putText(img, f"{gesture.name} ", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
                
                # Creating the index trace and the mouse
                if gesture == HandGesture.INDEX_RAISED:
                    self.indexPos.append([hand.index[3][0], hand.index[3][1], 1])
                    self.mouse = hand.index[3]
                    self.mouseCurrentDelay = self.mouseDelay

        # Update the mouse position, if the mouse is not moving, the mouse is set to -100, -100            
        if(self.mouseCurrentDelay > 0):
            self.mouseCurrentDelay -= 0.1
            if self.mouseCurrentDelay <= 0:
                self.mouse = [-100, -100]
                

    def getBinForGesture(self, gesture):
        bin_map = {
            HandGesture.FIST_CLOSED: "Compost",
            HandGesture.HAND_OPEN: "Glass",
            HandGesture.OK_SIGN: "Non Recycling",
            HandGesture.ROCK_N_ROLL: "Recycling",
            HandGesture.NONE: None
        }
        return self.bins.get(bin_map.get(gesture, None), None)

if __name__ == "__main__":
    game = Game("Joueur")
    print("Game created")
    game.play()
