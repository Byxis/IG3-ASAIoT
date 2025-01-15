import numpy as np
from Graphics import Graphic, SceneRender
import cv2
from Waste import Waste
from ComposedWaste import ComposedWaste
from WasteType import WasteType
from FPSCounter import FPSCounter
from random import randint
import csv
from copy import copy

def getRandomPosition(WIDTH, wasteList):
    positions = []
    for i in range(0, WIDTH, 70):
        if(not isSpawnPositionOccupied([i, -75], wasteList)):
            positions.append([i, -75])
    if(len(positions) == 0):
        return [randint(0, WIDTH), -75]
    elif len(positions) == 1:
        return positions[0]
    return positions[randint(0, len(positions)-1)]

def isSpawnPositionOccupied(position, wasteList):
    for elt in wasteList:
        if (elt.position[0] - position[0])**2  <= 50**2 and (elt.position[1] - position[1]) <= (75*3)**2:
            return True
    return False

def wasteSpawn(WIDTH, wasteList, wasteCatalog):
    """
    Ajoute un déchet à la liste des déchets.
    Entrée :
    wasteList : la liste des déchets
    name, type, speed, pos, sprite_path : spécifications du Waste
    """
    position = getRandomPosition(WIDTH, wasteList)

    a = copy(wasteCatalog[randint(0, len(wasteCatalog)-1)])

    wasteList.append(a)
    wasteList[-1].move(position)

def checkCollision(x, y, waste):
    if waste.position[0] <= x <= waste.position[0] + waste.radius*2 and waste.position[1] <= y <= waste.position[1] + waste.radius*2:
        return True
    return False

def createWastesFromSlice(WIDTH, wasteList, compWaste, wasteCatalog):
    """
    Fonction a appeler quand un dechet composé est slice
    Supprime le dechet composé de la liste de dechet et ajoute ses composants
    Entrée : 
    wasteList : la liste de dechets sur le jeu
    compWaste : le dechet qui est slice
    wasteCatalog : la liste de tous les dechets
    """
    components = compWaste.components
    wasteList.remove(compWaste)
    for elt in components:
        for i in range(len(wasteCatalog)):
            if elt == wasteCatalog[i].name:
                waste = copy(wasteCatalog[i])
                position = getRandomPosition(WIDTH, wasteList)
                waste.move([position[0], position[1]])
                wasteList.append(waste)
                break

def updateAllWaste(render, wasteList, HEIGHT, WIDTH, wasteCatalog, wasteCurrentDelay, indexPos, player):
    """
    Fonction de mise à jour de la position et de l'etat de tous les dechets.
    Entrée:
    render : le rendu à mettre à jour
    wasteList : la liste de tous les dechets
    HEIGHT : la hauteur de la fenêtre
    """
    if(len(wasteList) < 4 and wasteCurrentDelay <= 0):
        wasteSpawn(WIDTH, wasteList, wasteCatalog)
    for w in wasteList:
        render.add_layer(w.get_graphic(), (w.position[0], w.position[1]))
        w.update()
        if w.position[1] > HEIGHT - w.radius:
            wasteList.remove(w)
            player.score -= 1
            print("Score : ", player.score)
        if type(w) == Waste:
            if player.leftHand != None:
                if player.leftHand.isCompatible(w) and (player.leftHand.pos[0] - w.position[0])**2  <= 30**2 :
                    #Boost speed
                    w.update()

                if checkCollision(player.leftHand.pos[0], player.leftHand.pos[1], w) and w in wasteList:
                    player.score += 1
                    wasteList.remove(w)
                    print("Score : ", player.score)
            
            if player.rightHand != None:
                if player.rightHand.isCompatible(w) and (player.rightHand.pos[0] - w.position[0])**2  <= 30**2 :
                    #Boost speed
                    w.update()

                if checkCollision(player.rightHand.pos[0], player.rightHand.pos[1], w) and w in wasteList:
                    if(player.rightHand.isCompatible(w)):
                        player.score += 1
                        print("Score : ", player.score)
                    else:
                        player.score -= 1
                        print("Score : ", player.score)
                    wasteList.remove(w)
        if type(w) == ComposedWaste:
            if checkCollision(indexPos[0], indexPos[1], w):
                createWastesFromSlice(WIDTH, wasteList, w, wasteCatalog)
    return render

def createWasteCatalog():
    with open('CSV/wastes.csv', mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        l = list(csv_reader)
        wasteCatalog = []
        for line in l[1:]:
            if(len(line) > 0):
                if line[5] == 'None':
                    print(line[1])
                    print(WasteType[line[1]])
                    wasteCatalog.append(Waste(line[0], WasteType[line[1]], line[4], line[2]))
                else:
                    if line[7] != 'None':     
                        wasteCatalog.append(ComposedWaste(line[0], [line[5], line[6], line[7]], line[4], line[2]))
                    elif line[7] == 'None' and line[6] != 'None':
                        wasteCatalog.append(ComposedWaste(line[0], [line[5], line[6]], line[4], line[2]))
    return wasteCatalog

def main():
    EPSILON = 1
    WIDTH, HEIGHT = 800, 600
    wasteList = []
    a = createWasteCatalog(WIDTH)
    
    wasteSpawn(WIDTH, wasteList, a)
    wasteSpawn(WIDTH, wasteList, a)
    wasteSpawn(WIDTH, wasteList, a)
    wasteSpawn(WIDTH, wasteList, a)
    
    #compWasteSpawn(wasteList, "dechetcomp2", [waste1, compWaste1], [0, 1], [100, 200], "output2.png")
    # Utilisation de la webcam
    cap = cv2.VideoCapture(0)

    # Instancie le "moteur de rendu"
    render = SceneRender((WIDTH, HEIGHT))
    fps = FPSCounter()


    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
        img = cv2.flip(img, 1)
        # On transforme "img" en un élément graphique manipulable
        webcam = Graphic(img)
        webcam.resize((WIDTH, HEIGHT))
        # webcam.fill((0, 0, 0)) 
            
        
        """
        mask = np.zeros((HEIGHT, WIDTH))
        for i in range(HEIGHT):
            for j in range(WIDTH):
                mask[i, j] = abs(10 - (i + j) % 20) / 10.0 if 50 < i < 100 else 0
        """

        render.clear()
        # On place en fond le caneva
        render.add_layer(webcam)
        render = updateAllWaste(render, wasteList, HEIGHT, WIDTH, a)

        output = render.get_image()
        
        fps.update()
        ouput = fps.display(output)
        cv2.imshow("Resultat", output)

        key = cv2.waitKey(EPSILON) & 0xFF
        if key == ord("q") or key == 27:
            break

        """
        if key != 0xFF:
            if key == ord("1"):
                print("La touche '1' est appuyée")
                # Faire des actions
            if key == ord("2"):
                print("La touche '2' est appuyée")
                # Faire des actions
        """
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()



