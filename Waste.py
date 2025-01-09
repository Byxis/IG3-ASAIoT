import WasteType
import cv2
from Graphics import Graphic, SceneRender
class Waste:
    def __init__(self, _name: str,_type: WasteType, _speed: float, _pos, _sprite_path: str):
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
        self.position = _pos
        self.sprite = Graphic(cv2.imread(_sprite_path, cv2.IMREAD_UNCHANGED))
        self.sprite_path = _sprite_path
        self.sprite.resize((150, 150), cv2.INTER_NEAREST)
        self.radius = 75
    
    def update(self, dt):
        self.position[0] += self.speed[0]
        self.position[1] += self.speed[1]
    
    def move(self, pos):
        self.position = pos
        return
    
    def get_graphic(self):
        return self.sprite