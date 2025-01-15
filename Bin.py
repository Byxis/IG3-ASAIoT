from Graphics import Graphic
import cv2
class Bin:
    def __init__(self, _name, _type, _height):
        self.name = _name
        self.type = _type
        self.content = []
        sprite = Graphic()
        if _type == "recycling":
            sprite = Graphic(cv2.imread("Textures/Bins/recycling.png", cv2.IMREAD_UNCHANGED))
        elif _type == "glass":
            sprite = Graphic(cv2.imread("Textures/Bins/glass.png", cv2.IMREAD_UNCHANGED))
        elif _type == "default":
            sprite = Graphic(cv2.imread("Textures/Bins/default.png", cv2.IMREAD_UNCHANGED))
        elif _type == "compost":
            sprite = Graphic(cv2.imread("Textures/Bins/compost.png", cv2.IMREAD_UNCHANGED))
        size = 1
        self.sprite = sprite.resize((50*size, 75*size), interpolation=cv2.INTER_AREA)
        self.pos = [0,_height-50]
    
    def updatePos(self, pos):
        self.pos[0] = pos[0]

    def addWasteToBin(self, waste):
        self.content.put(waste)
    
    def isCompatible(self, waste):
        if isinstance(waste, ComposedWaste):
            return False
        else :
            return self.type == waste.type