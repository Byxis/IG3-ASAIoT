import WasteType
import cv2
from Graphics import Graphic, SceneRender
from Waste import Waste
from WasteFall import *

class ComposedWaste:
    def __init__(self, _name: str, _components, _pos, _speed, _sprite_path):
        """
        Crée une instance de ComposedWaste
        Entrée :
        _name : str nom du déchet
        _component : [] une liste contenant des dechets ou des dechets composé
        _pos : [int] position initial du dechet
        _speed : [int] la vitesse horizontale et verticale de l'objet
        """
        self.components = _components
        self.name = _name
        self.sprite = Graphic(cv2.imread(_sprite_path, cv2.IMREAD_UNCHANGED))
        self.sprite.resize((150, 150), cv2.INTER_NEAREST)
        self.sprite_path = _sprite_path
        self.radius = 50
        self.position = _pos
        self.speed = _speed

    def slice(self, wasteList):
        i = -50*len(self.components)/2
        wasteList.remove(self)
        for elt in self.components:
            if type(elt) == Waste:
                wasteSpawn(wasteList, elt.name, elt.type, elt.speed, elt.position + i, elt.sprite_path)
                i += 50
            elif type(elt) == ComposedWaste:
                compWasteSpawn(wasteList, elt.name, elt.components, elt.speed, elt.position + i, elt.sprite_path)
                i +=50
    
    def update(self, dt):
        self.position[0] += self.speed[0]
        self.position[1] += self.speed[1]

    def move(self, pos):
        self.position = pos
        return
    
    def get_graphic(self):
        return self.sprite