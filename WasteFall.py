import numpy as np
from Graphics import Graphic, SceneRender
import cv2
from Waste import Waste
from ComposedWaste import ComposedWaste
from WasteType import WasteType
from FPSCounter import FPSCounter
from random import randint
import csv



def wasteSpawn(WIDTH, wasteList, name, type, speed, sprite_path):
    """
    Ajoute un déchet à la liste des déchets.
    Entrée :
    wasteList : la liste des déchets
    name, type, speed, pos, sprite_path : spécifications du Waste
    """
    positions = []
    for i in range(0, 800, 80):
        positions.append([i, -75])
    
    isOccupied = True
    while isOccupied:
        isOccupied = False
        i = randint(0, 9)
        for elt in wasteList:
            if elt.position == positions[i]:
                isOccupied = True
    
    wasteList.append(Waste(name, type, speed, positions[i], sprite_path))
    print(elt.name for elt in wasteList)




def addWasteToWasteList(wasteList, name, type, speed, position, sprite_path):
    positions = []
    for i in range(0, 800, 80):
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
    print(elt.name for elt in wasteList)






def compWasteSpawn(WIDTH, wasteList, name, component, speed, sprite_path):
    """
    Ajoute un dechet composé à la liste des dechets
    Entrée : 
    wasteList : la liste des dechets
    name, type, speed, pos, sprite_path : voir spécif ComposedWaste
    """
    positions = []
    for i in range(0, 800, 80):
        positions.append([i, -75])
    
    isOccupied = True
    while isOccupied:
        isOccupied = False
        i = randint(0, 9)
        for elt in wasteList:
            if elt.position == positions[i]:
                isOccupied = True
    wasteList.append(ComposedWaste(name, component, positions[i], speed, sprite_path))







def addCompWasteToWasteList(wasteList, name, component, position, speed, sprite_path):
    """
    Ajoute un dechet composé à la liste des dechets lorsqu'il provient d'un slice
    Entrée : 
    wasteList : la liste des dechets
    name, type, speed, pos, sprite_path : voir spécif ComposedWaste
    """
    positions = []
    for i in range(0, 800, 80):
        positions.append([i, -75])
    for elt in wasteList:
        isOccupied = True
        while isOccupied:
            isOccupied = False
            i = randint(0, 9)
            for elt in wasteList:
                if elt.position == positions[i]:
                    isOccupied = True
    wasteList.append(ComposedWaste(name, type, speed, position, sprite_path))
    print(elt.name for elt in wasteList)




def createWastesFromSlice(wasteList, compWaste):
    """
    Fonction a appeler quand un dechet composé est slice
    Supprime le dechet composé de la liste de dechet et ajoute ses composants
    Entrée : 
    wasteList : la liste de dechets
    compWaste : le dechet qui est slice
    """
    positions = []
    h = compWaste.position[1]
    for i in range(0, 800, 80):
        positions.append([i, -75])
    components = compWaste.components
    wasteList.remove(compWaste)
    for elt in components:
        isOccupied = True
        while isOccupied:
            isOccupied = False
            i = randint(0, 9)
            for elt in wasteList:
                if elt.position == positions[i]:
                    isOccupied = True
        if type(elt) == Waste:
            addWasteToWasteList(wasteList, elt.name, elt.type, elt.speed, [positions[i][0], h], elt.sprite_path)
        elif type(elt) == ComposedWaste:
            addCompWasteToWasteList(wasteList, elt.name, elt.components, elt.speed, [positions[i][0], h], elt.sprite_path)







def updateAllWaste(render, wasteList, HEIGHT):
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
                    createWastesFromSlice(wasteList, w)
                if w.position[1] < HEIGHT - w.radius:
                    render.add_layer(w.get_graphic(), (w.position[0], w.position[1]))
    return render





def createWasteCatalog(WIDTH):
    with open('Wastes.csv', mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        l = list(csv_reader)
        wasteCatalog = []
        for line in l:
            if line[5] == 'None':
                wasteSpawn(WIDTH, wasteCatalog, line[0], line[1], line[4], line[2])
            else:
                if line[7] != 'None':     
                    compWasteSpawn(WIDTH, wasteCatalog, line[0], [line[5], line[6], line[7]], line[4], line[2])
                elif line[7] == 'None' and line[6] != 'None':
                    compWasteSpawn(WIDTH, wasteCatalog, line[0], [line[5], line[6]], line[4], line[2])
    return wasteCatalog


def main():
    EPSILON = 1
    WIDTH, HEIGHT = 800, 600
    
    wasteList = []
    wasteSpawn(WIDTH, wasteList, "dechet", 'Recyclable',[0 ,1], "Textures/Waste/output.png")
    wasteSpawn(WIDTH, wasteList, "dechet", 'Recyclable',[0 ,1], "Textures/Waste/output.png")
    wasteSpawn(WIDTH, wasteList, "dechet", 'Recyclable',[0 ,1], "Textures/Waste/output.png")
    wasteSpawn(WIDTH, wasteList, "dechet", 'Recyclable',[0 ,1], "Textures/Waste/output.png")

    waste1 = Waste("dechet", 'Recyclable',[0 ,1], [700, 100], "Textures/Waste/output.png")
    compWaste1 = ComposedWaste("dechetcomp", [waste1, waste1, waste1], [0, 1], [100, 100], "Textures/Waste/output2.png")
    compWaste2 = ComposedWaste("dechetcomp2", [waste1, compWaste1], [0, 1], [100, 200], "Textures/Waste/output2.png")
    compWasteSpawn(WIDTH, wasteList, "dechetcomp", [waste1, waste1, waste1, waste1, waste1, waste1, waste1], [0, 2], "Textures/Waste/output2.png")
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
        render = updateAllWaste(render, wasteList, HEIGHT)

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



