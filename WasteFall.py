import numpy as np
from Graphics import Graphic, SceneRender
import cv2
from Waste import Waste
from ComposedWaste import ComposedWaste
from WasteType import WasteType
from FPSCounter import FPSCounter


def wasteSpawn(wasteList, name, type, speed, pos, sprite_path):
    wasteList.append(Waste(name, type, speed, pos, sprite_path))

def compWasteSpawn(wasteList, name, component, speed, pos, sprite_path):
    wasteList.append(ComposedWaste(name, component, pos, speed, sprite_path))

def updateAllWaste(render, wasteList, HEIGHT, EPSILON):
    for w in wasteList:
            w.update(EPSILON)
            if w.position[1] < HEIGHT - w.radius:
                render.add_layer(w.get_graphic, (w.position[0], w.position[1]))
            if (w.position[1] < HEIGHT - w.radius - 300) and type(w) == ComposedWaste:
                w.slice
    return render

def main():
    EPSILON = 1
    WIDTH, HEIGHT = 800, 600

    wasteList = []
    wasteSpawn(wasteList, "dechet i", 'Recyclable',[0, 4], [250, 100], "output.png")
    wasteSpawn(wasteList, "dechet", 'Recyclable',[0 ,3], [400, 100], "output.png")
    wasteSpawn(wasteList, "dechet", 'Recyclable',[0 ,2], [550, 100], "output.png")
    wasteSpawn(wasteList, "dechet", 'Recyclable',[0 ,1], [700, 100], "output.png")

    waste1 = Waste("dechet", 'Recyclable',[0 ,1], [700, 100], "output.png")
    compWaste1 = ComposedWaste("dechetcomp", [waste1, waste1], [100, 100], [0, 1], "output2.png")
    compWaste2 = ComposedWaste("dechetcomp2", [waste1, compWaste1], [100, 200], [0, 1], "output2.png")
    compWasteSpawn(wasteList, "dechetcomp", [waste1, waste1], [100, 100], [0, 1], "output2.png")
    compWasteSpawn(wasteList, "dechetcomp2", [waste1, compWaste1], [100, 200], [0, 1], "output2.png")
    # Utilisation de la webcam
    cap = cv2.VideoCapture(0)

    # Instancie le "moteur de rendu"
    render = SceneRender((WIDTH, HEIGHT))
    fps = FPSCounter()


    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
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
        render = updateAllWaste(render, wasteList, HEIGHT, EPSILON)

        output = render.get_image()
        
        fps.update()
        ouput = fps.display(output)
        cv2.imshow("Resultat", output)

        key = cv2.waitKey(EPSILON) & 0xFF
        if key == ord("q") or key == 27:
            break


        if key != 0xFF:
            if key == ord("1"):
                print("La touche '1' est appuyée")
                # Faire des actions
            if key == ord("2"):
                print("La touche '2' est appuyée")
                # Faire des actions

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()



