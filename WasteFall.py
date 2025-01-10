import numpy as np
from Graphics import Graphic, SceneRender
import cv2
from Waste import Waste
from ComposedWaste import ComposedWaste
from WasteType import WasteType
from FPSCounter import FPSCounter


def wasteSpawn(wasteList, name, type, speed, pos, sprite_path):
    """
    Ajoute un dechet à la liste des dechets
    Entrée :
    wasteList : la liste des dechets
    name, type, speed, pos, sprite_path : voir spécif Waste
    """
    wasteList.append(Waste(name, type, speed, pos, sprite_path))


def compWasteSpawn(wasteList, name, component, speed, pos, sprite_path):
    """
    Ajoute un dechet composé à la liste des dechets
    Entrée : 
    wasteList : la liste des dechets
    name, type, speed, pos, sprite_path : voir spécif ComposedWaste
    """
    wasteList.append(ComposedWaste(name, component, pos, speed, sprite_path))

def createWastesFromSlice(wasteList, compWaste):
    """
    Fonction a appeler quand un dechet composé est slice
    Supprime le dechet composé de la liste de dechet et ajoute ses composants
    Entrée : 
    wasteList : la liste de dechets
    compWaste : le dechet qui est slice
    """
    components = compWaste.components
    i = -50*len(components)/2
    wasteList.remove(compWaste)
    for elt in components:
        if compWaste.position[0] + i - 75 < 0:
            i += 100
        if compWaste.position[0] + i*len(components)/2 > 800: #800 : width de la fenetre
            i -= 100*len(components)
        if type(elt) == Waste:
            wasteSpawn(wasteList, elt.name, elt.type, elt.speed, [compWaste.position[0] + i, compWaste.position[1]], elt.sprite_path)
            i += 100
        elif type(elt) == ComposedWaste:
            compWasteSpawn(wasteList, elt.name, elt.components, elt.speed, [compWaste.position[0] + i, compWaste.position[1]], elt.sprite_path)
            i +=100

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

                if (w.position[1] > HEIGHT - w.radius - 300): #A remplacer par l'évenement quand le joueur slice
                    createWastesFromSlice(wasteList, w)
                if w.position[1] < HEIGHT - w.radius:
                    render.add_layer(w.get_graphic(), (w.position[0], w.position[1]))
    return render

def main():
    EPSILON = 1
    WIDTH, HEIGHT = 800, 600
    
    wasteList = []
    #wasteSpawn(wasteList, "dechet", 'Recyclable',[0, 4], [250, 100], "output.png", WIDTH)
    #wasteSpawn(wasteList, "dechet", 'Recyclable',[0 ,3], [400, 100], "output.png", WIDTH)
    #wasteSpawn(wasteList, "dechet", 'Recyclable',[0 ,2], [550, 100], "output.png", WIDTH)
    #wasteSpawn(wasteList, "dechet", 'Recyclable',[0 ,1], [700, 100], "output.png", WIDTH)

    waste1 = Waste("dechet", 'Recyclable',[0 ,1], [700, 100], "Textures/Waste/output.png")
    compWaste1 = ComposedWaste("dechetcomp", [waste1, waste1, waste1], [0, 1], [100, 100], "Textures/Waste/output2.png")
    compWaste2 = ComposedWaste("dechetcomp2", [waste1, compWaste1], [0, 1], [100, 200], "Textures/Waste/output2.png")
    compWasteSpawn(wasteList, "dechetcomp", [waste1, waste1, waste1, waste1, waste1, waste1, waste1], [0, 2], [600, 100], "Textures/Waste/output2.png")
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



