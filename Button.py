import cv2
from Graphics import Graphic, SceneRender


class Button:
    def __init__(self, name: str, x1, y1, x2, y2, action=None):
        self.name = name
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.action = action

    def isClicked(self, pos_x=-1, pos_y=-1):
        return self.x1 <= pos_x <= self.x2 and self.y1 <= pos_y <= self.y2

    def click(self):
        if self.action:
            self.action()

    def draw_button(self,caneva):
        caneva.draw_rectangle((self.x1, self.y1), (self.x2, self.y2), (200, 200, 200), 3)
        caneva.draw_text(self.name, (((self.x1+self.x2)/2-(len(self.name))), ((self.y1+self.y2)/2-(len(self.name)))), 'Hollster.ttf', 30   , (200, 200, 200), 3, center = True)
  