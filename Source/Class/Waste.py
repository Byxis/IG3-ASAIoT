import Enums.WasteType as WasteType
from Utils.Graphics import Graphic

import cv2

class Waste:
    def __init__(self, _name: str,_type: WasteType, _speed: float, _sprite_path: str, size=75):
        """
        Create a Waste instance

        Params : 
        - _name : str
            the name of the waste
        - _type : WasteType
            the type of the waste
        - _speed : float
            the speed of the waste
        - _sprite_path : str
            the path to the sprite of the waste
        - size = 75 : int
            the size of the waste
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
        """
        Update the position of the waste
        """
        self.position[1] += int(self.speed)
    
    def move(self, pos):
        """
        Move the waste to a new position

        Params:
        - pos : [int]
            the new position of the waste
        """
        self.position = pos
    
    def get_graphic(self):
        """
        Return the sprite of the waste

        Returns:
        - Graphic
            the sprite of the waste
        """
        return self.sprite