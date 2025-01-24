from Graphics import Graphic
from ComposedWaste import ComposedWaste
from WasteType import WasteType
import cv2
from ComposedWaste import ComposedWaste

class Bin:
    def __init__(self, _name, _type, _height):
        self.name = _name
        self.type = _type
        self.content = []
        sprite = Graphic()
        if _type == WasteType.Recycling:
            sprite = Graphic(cv2.imread("Textures/Bins/recycling.png", cv2.IMREAD_UNCHANGED))
        elif _type == WasteType.Glass:
            sprite = Graphic(cv2.imread("Textures/Bins/glass.png", cv2.IMREAD_UNCHANGED))
        elif _type == WasteType.NonRecycling:
            sprite = Graphic(cv2.imread("Textures/Bins/default.png", cv2.IMREAD_UNCHANGED))
        elif _type == WasteType.Compost:
            sprite = Graphic(cv2.imread("Textures/Bins/compost.png", cv2.IMREAD_UNCHANGED))
        size = 1
        if _type != WasteType.Floor :
            self.sprite = sprite.resize((50*size, 75*size), interpolation=cv2.INTER_AREA)
        self.pos = [0,_height-50]
    
    def updatePos(self, pos):
        self.pos[0] = pos[0]

    def addWasteToBin(self, waste):
        self.content.put(waste)
    
    def isCompatible(self, waste):
        if type(waste) == ComposedWaste:
            return False
        else :
            return self.type == waste.type
