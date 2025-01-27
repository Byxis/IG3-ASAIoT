from Utils.Graphics import Graphic

import cv2
import os

class ComposedWaste:

    def __init__(self, _name: str, _components, _speed, _sprite_path, _score, size=75):
        """
        Create a ComposedWaste instance

        Params :
        - _name : str
            the name of the waste
        - _components : [Waste]
            the components of the waste
        - _speed : float
            the speed of the waste
        - _sprite_path : str
            the path to the sprite of the waste
        - size = 75 : int
            the size of the waste
        """
        self.components = _components
        self.name = _name 
        self.sprite_path = os.path.abspath(os.path.join(os.path.dirname(__file__), _sprite_path))
        
        if self.sprite_path is None or not os.path.exists(self.sprite_path):
            raise FileNotFoundError(f"Image for composed waste not found at path: {self.sprite_path}")
        
        sprite = cv2.imread(self.sprite_path, cv2.IMREAD_UNCHANGED)
        if sprite is None:
            raise FileNotFoundError(f"Failed to load image for composed waste from path: {self.sprite_path}")
        
        self.sprite = Graphic(sprite)
        self.sprite.resize((size, size), cv2.INTER_NEAREST)
        
        self.radius = size/2
        self.speed = _speed
        self.isSliced = False
        self.position = [0, 0]
        self.score = _score

    def slice(self):
        """
        Return the components of the waste

        Returns:
        - [Waste]
            the components of the waste
        """
        return self.components
    
    def update(self):
        """
        Move the waste with gravity depending on its speed
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