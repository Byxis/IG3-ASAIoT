import cv2
from Graphics import Graphic, SceneRender


class Button:
    def __init__(self, name: str, x1, y1, width, height, color, action=None):
        self.name = name
        self.x1 = x1
        self.y1 = y1
        self.width = width  
        self.height = height
        self.x2 = x1 + width
        self.y2 = y1 + height
        self.color = color
        self.color2 = tuple(color[len(color)-1-i] for i in range(len(color)))
        self.action = action

    def isClicked(self, pos_x=-1, pos_y=-1):
        return self.x1 <= pos_x <= self.x2 and self.y1 <= pos_y <= self.y2

    def click(self):
        if self.action:
            return self.action()

    def draw_button(self,caneva):
        caneva.draw_rectangle((self.x1, self.y1), (self.x2, self.y2), self.color, 3)
        caneva.draw_text(self.name, (round((self.x1+self.x2)/2), round((self.y1+self.y2)/2-self.height/20)), 'Hollster.ttf', round((((self.width/len(self.name))**2+(self.height)**2)**0.5)/2), self.color2, 3, center = True)
  