from Graphics import Graphic
import cv2
class Bin:
    def __init__(self, _name, _type, _height):
        self.name = _name
        self.type = _type
        self.content = []
        sprite = Graphic()
        if _type == "plastic":
            sprite = Graphic(cv2.imread("Textures/Bin.png", cv2.IMREAD_UNCHANGED))
        elif _type == "paper":
            sprite = Graphic(cv2.imread("Textures/Bin.png", cv2.IMREAD_UNCHANGED))
        elif _type == "glass":
            sprite = Graphic(cv2.imread("Textures/Bin.png", cv2.IMREAD_UNCHANGED))
        else:
            sprite = Graphic(cv2.imread("Textures/Bin.png", cv2.IMREAD_UNCHANGED))
        sprite.resize((50, 50))
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