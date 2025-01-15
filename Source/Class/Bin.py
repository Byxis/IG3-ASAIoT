from Utils.Graphics import Graphic
from Class.ComposedWaste import ComposedWaste

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
        sprite = Graphic()
        if _type == "recycling":
            print(os.path.abspath("../Ressources/Textures/Bins/recycling.png"))
            sprite = Graphic(cv2.imread("../Ressources/Textures/Bins/recycling.png", cv2.IMREAD_UNCHANGED))
        elif _type == "glass":
            sprite = Graphic(cv2.imread("../Ressources/Textures/Bins/glass.png", cv2.IMREAD_UNCHANGED))
        elif _type == "default":
            sprite = Graphic(cv2.imread("../Ressources/Textures/Bins/default.png", cv2.IMREAD_UNCHANGED))
        elif _type == "compost":
            sprite = Graphic(cv2.imread("../Ressources/Textures/Bins/compost.png", cv2.IMREAD_UNCHANGED))
        size = 1
        self.sprite = sprite.resize((50*size, 75*size), interpolation=cv2.INTER_AREA)
        self.pos = [0,_height-50]
    
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
        self.content.put(waste)
    
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
        if type(waste) == ComposedWaste:
            return False
        else :
            return self.type == waste.type