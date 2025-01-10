from Graphics import Graphic
import cv2
class Bin:
    def __init__(self, _name, _type, _height):
        self.name = _name
        self.type = _type
        self.content = []
        sprite = Graphic()
        if _type == "recycling":
            sprite = Graphic(cv2.imread("Textures/recycling.png", cv2.IMREAD_UNCHANGED))
        elif _type == "glass":
            sprite = Graphic(cv2.imread("Textures/glass.png", cv2.IMREAD_UNCHANGED))
        elif _type == "default":
            sprite = Graphic(cv2.imread("Textures/default.png", cv2.IMREAD_UNCHANGED))
        elif _type == "compost":
            sprite = Graphic(cv2.imread("Textures/compost.png", cv2.IMREAD_UNCHANGED))
        size = 1
        sprite.resize((50*size, 75*size))
        self.sprite = sprite
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