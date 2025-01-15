import WasteType
import cv2
from Graphics import Graphic, SceneRender
class Waste:
    def __init__(self, _name: str,_type: WasteType, _speed: float, _sprite_path: str, size=75):
        """
        Crée une instance de Waste
        Entrée : 
        _name : str le nom du joueur
        _type : WasteType le type de dechet
        _speed : [Int] la vitesse de descente initiale du dechet
        _pos : [Int], len(_pos) = 2, la position initiale du dêchet dans l'image
        """
        self.name = _name
        self.type = _type
        self.speed = _speed
        self.position = [0, 0]
        self.sprite = Graphic(cv2.imread(""+_sprite_path, cv2.IMREAD_UNCHANGED))
        self.sprite_path = _sprite_path
        self.sprite.resize((size, size), cv2.INTER_NEAREST)
        self.radius = size/2
    
    def update(self):
        self.position[1] += int(self.speed)
    
    def move(self, pos):
        self.position = pos
    
    def get_graphic(self):
        return self.sprite