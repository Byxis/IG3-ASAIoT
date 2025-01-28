import cv2
import os
from Utils.Graphics import Graphic


class Frame:
    def __init__(self, name : str, loadedlist : list, x1, y1, width, height, score=None):
        self.name = name
        self.loadedlist = loadedlist
        self.x1 = x1
        self.y1 = y1
        self.width = width  
        self.height = height
        self.x2 = x1 + width
        self.y2 = y1 + height
        self.score = score

    def draw_title(self,caneva):
        font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Ressources', 'Fonts', 'Hollster.ttf'))
        caneva.draw_rectangle((self.x1, self.y1), (self.x2, self.y1+round(2*self.height/11)), (200, 200, 200), 3)
        caneva.draw_text(self.name, (round((self.x1+self.x2)/2), round((self.y1+self.y1+round(2*self.height/11))/2-3*self.height/110)), font_path, round((((self.width/len(self.name))**2+(0.75*2*self.height/11)**2)**0.5)), (200, 200, 200), 3, center = True)
                                                                                                                                          
    def draw_frame(self,caneva):
        font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Ressources', 'Fonts', 'Hollster.ttf'))
        caneva.draw_rectangle((self.x1, self.y1+round(2*self.height/11)), (self.x2, self.y1+round(2*self.height/11)+round(self.height/11*(len(self.loadedlist)+1))), (200, 200, 200), 3)
        for i in range(len(self.loadedlist)) :
            score = self.loadedlist[i]
            score_text = str()
            for e in score :
                score_text += str(e)
                score_text += " "
            caneva.draw_text(score_text, (round((self.x1+self.x2)/2+5), round(self.y1+(i+3)*(self.height/11))), font_path, round((((2.9*self.width/len(str(score)))**2+((1.3*self.height)/len(str(score)))**2)**0.5)*1.2), (200, 200, 200), 3, center = True)
  
    def reset_loadedlist(self, loadedliste):
        self.loadedlist = loadedliste