from Utils.Graphics import Graphic
from Class.ComposedWaste import ComposedWaste
from Enums.WasteType import WasteType

import cv2
import os

class Bin:
    def __init__(self, _name, _type, _height):
        """
        Create a Bin instance

        Params:
        - _name : str
            the name of the bin
        - _type : str
            the type of the bin
        - _height : int
            the height of the screen
        """
        self.name = _name
        self.type = _type
        self.content = []
        sprite_path = None
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Ressources', 'Textures', 'Bins'))
        
        if _type == WasteType.Recycling:
            sprite_path = os.path.join(base_path, 'recycling.png')
        elif _type == WasteType.Glass:
            sprite_path = os.path.join(base_path, 'glass.png')
        elif _type == WasteType.NonRecycling:
            sprite_path = os.path.join(base_path, 'default.png')
        elif _type == WasteType.Compost:
            sprite_path = os.path.join(base_path, 'compost.png')
        elif _type == WasteType.Floor:
            sprite_path = os.path.join(base_path, 'default.png')
                
        if sprite_path is None or not os.path.exists(sprite_path):
            raise FileNotFoundError(f"Image for bin type {_type} not found at path: {sprite_path}")
        
        sprite = cv2.imread(sprite_path, cv2.IMREAD_UNCHANGED)
        if sprite is None:
            raise FileNotFoundError(f"Failed to load image for bin type {_type} from path: {sprite_path}")
        
        graphic_sprite = Graphic(sprite)
        size = 1
        self.sprite = graphic_sprite.resize((50 * size, 75 * size), interpolation=cv2.INTER_AREA)
        self.pos = [0, _height - 50]
    
    def updatePos(self, pos):
        """
        Update the position of the bin

        Params:
        - pos : [int] 
            the new position of the bin
        """

        self.pos[0] = pos[0]

    def addWasteToBin(self, waste):
        """
        Add a waste to the bin

        Params:
        - waste : Waste
            the waste to add to the bin
        """
        self.content.append(waste)
    
    def isCompatible(self, waste):
        """
        Return if the waste is compatible with the bin. If the waste is a ComposedWaste, it's never compatible with the bin.

        Params:
        - waste : Waste
            the waste to check compatibility with
        
        Returns:
        - bool
            True if the waste is compatible with the bin, False otherwise
        """
        if type(waste) is ComposedWaste:
            return False
        else :
            return self.type == waste.type