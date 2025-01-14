import WasteType
import cv2
from Graphics import Graphic, SceneRender
from Waste import Waste
class ComposedWaste:

    def __init__(self, _name: str, _components, _speed, _sprite_path, size=150):
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
        self.sprite.resize((size, size), cv2.INTER_NEAREST)
        self.sprite_path = _sprite_path
        self.radius = size/2
        self.speed = _speed
        self.isSliced = False
        self.position = [0, 0]

    def slice(self, wasteList):
        return self.components
    
    def update(self):
        self.position[1] += int(self.speed)

    def move(self, pos):
        self.position = pos
        
    
    def get_graphic(self):
        return self.sprite