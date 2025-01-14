import numpy as np
from Graphics import Graphic, SceneRender
import cv2
from Waste import Waste
from ComposedWaste import ComposedWaste
from WasteType import WasteType
from FPSCounter import FPSCounter
from random import randint
import csv



def wasteSpawn(WIDTH, wasteList, wasteCatalog):
    """
    Ajoute un déchet à la liste des déchets.
    Entrée :
    wasteList : la liste des déchets
    name, type, speed, pos, sprite_path : spécifications du Waste
    """
    positions = []
    for i in range(0, 700, 70):
        positions.append([i, -75])
    
    isOccupied = True
    while isOccupied:
        isOccupied = False
        i = randint(0, 9)
        for elt in wasteList:
            if elt.position == positions[i]:
                isOccupied = True
    
    wasteList.append(wasteCatalog[randint(0, len(wasteCatalog))])
    wasteList[-1].move(positions[i])




def addWasteToWasteList(wasteList, name, type, speed, position, sprite_path):
    positions = []
    for i in range(0, 700, 70):
        positions.append([i, -75])
    for elt in wasteList:
        isOccupied = True
        while isOccupied:
            isOccupied = False
            i = randint(0, 9)
            for elt in wasteList:
                if elt.position == positions[i]:
                    isOccupied = True
    wasteList.append(Waste(name, type, speed, position, sprite_path))






def compWasteSpawn(WIDTH, wasteList, name, component, speed, sprite_path):
    """
    Ajoute un dechet composé à la liste des dechets
    Entrée : 
    wasteList : la liste des dechets
    name, type, speed, pos, sprite_path : voir spécif ComposedWaste
    """
    positions = []
    for i in range(0, 700, 70):
        positions.append([i, -75])
    
    isOccupied = True
    while isOccupied:
        isOccupied = False
        i = randint(0, 9)
        for elt in wasteList:
            if elt.position == positions[i]:
                isOccupied = True
    
    cwaste = ComposedWaste(name, component, speed, sprite_path)
    cwaste.move(positions[i])
    wasteList.append()








def addCompWasteToWasteList(wasteList, name, component, position, speed, sprite_path):
    """
    Ajoute un dechet composé à la liste des dechets lorsqu'il provient d'un slice
    Entrée : 
    wasteList : la liste des dechets
    name, type, speed, pos, sprite_path : voir spécif ComposedWaste
    """
    positions = []
    for i in range(0, 700, 70):
        positions.append([i, -75])
    for elt in wasteList:
        isOccupied = True
        while isOccupied:
            isOccupied = False
            i = randint(0, 9)
            for elt in wasteList:
                if elt.position == positions[i]:
                    isOccupied = True
    wasteList.append(ComposedWaste(name, type, speed, position[i], sprite_path))
    print(elt.name for elt in wasteList)




def createWastesFromSlice(wasteList, compWaste, wasteCatalog):
    """
    Fonction a appeler quand un dechet composé est slice
    Supprime le dechet composé de la liste de dechet et ajoute ses composants
    Entrée : 
    wasteList : la liste de dechets
    compWaste : le dechet qui est slice
    """
    positions = []
    h = compWaste.position[1]
    for i in range(0, 700, 70):
        positions.append([i, -75])
    comp = compWaste
    wasteList.remove(compWaste)
    for elt in comp.components:
        isOccupied = True
        while isOccupied:
            isOccupied = False
            i = randint(0, 9)
            for elt in wasteList:
                if elt.position == positions[i]:
                    isOccupied = True
        for i in range(len(wasteCatalog)):
            if wasteCatalog[i].name == elt:
                a = wasteCatalog[i]
                a.move([positions[i][0], comp.position[1]])
                wasteList.append(wasteCatalog[i])






def updateAllWaste(render, wasteList, HEIGHT, WIDTH, wasteCatalog):
    """
    Fonction de mise à jour de la position et de l'etat de tous les dechets.
    Entrée:
    render : le rendu à mettre à jour
    wasteList : la liste de tous les dechets
    HEIGHT : la hauteur de la fenêtre
    """
    
    for w in wasteList:
        if type(w) == Waste:
            w.update()
            if w.position[1] < HEIGHT - w.radius:
                render.add_layer(w.get_graphic(), (w.position[0], w.position[1]))
        if type(w) == ComposedWaste:
            w.update()

            
            #if (w.position[1] > HEIGHT - w.radius - 300): #A remplacer par l'évenement quand le joueur slice
                #createWastesFromSlice(wasteList, w)
            
            if w.position[1] > HEIGHT - w.radius - 300:
                w.isSliced = True
            if w.isSliced:
                createWastesFromSlice(wasteList, w, wasteCatalog)
            if w.position[1] < HEIGHT - w.radius:
                render.add_layer(w.get_graphic(), (w.position[0], w.position[1]))
            else:
                wasteList.remove(w)
    if(len(wasteList) < 4):
        wasteSpawn(WIDTH, wasteList, wasteCatalog)
    return render





def createWasteCatalog(WIDTH):
    with open('wastes.csv', mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        l = list(csv_reader)
        wasteCatalog = []
        for line in l[1:]:
            if line[5] == 'None':
                wasteCatalog.append(Waste(line[0], line[1], line[4], "Textures/Waste/output.png"))
            else:
                if line[7] != 'None':     
                    wasteCatalog.append(ComposedWaste(line[0], [line[5], line[6], line[7]], line[4], "Textures/Waste/output2.png"))
                elif line[7] == 'None' and line[6] != 'None':
                    wasteCatalog.append(ComposedWaste(line[0], [line[5], line[6]], line[4], "Textures/Waste/output2.png"))
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



