from Utils.Graphics import Graphic

import cv2

class ComposedWaste:

    def __init__(self, _name: str, _components, _speed, _sprite_path, size=75):
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
        self.sprite = Graphic(cv2.imread(_sprite_path, cv2.IMREAD_UNCHANGED))
        self.sprite.resize((size, size), cv2.INTER_NEAREST)
        self.sprite_path = _sprite_path
        self.radius = size/2
        self.speed = _speed
        self.isSliced = False
        self.position = [0, 0]

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