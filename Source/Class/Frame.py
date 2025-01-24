import cv2
from Utils.Graphics import Graphic


class Frame:
    def __init__(self, name : str, scores : list, x1, y1, width, height, score=None):
        self.name = name
        self.scores = scores
        self.x1 = x1
        self.y1 = y1
        self.width = width  
        self.height = height
        self.x2 = x1 + width
        self.y2 = y1 + height
        self.score = score

    def draw_title(self,caneva):
        caneva.draw_rectangle((self.x1, self.y1), (self.x2, self.y1+round(2*self.height/11)), (200, 200, 200), 3)
        caneva.draw_text(self.name, (round((self.x1+self.x2)/2), round((self.y1+self.y1+round(2*self.height/11))/2-3*self.height/110)), 'Hollster.ttf', round((((self.width/len(self.name))**2+(0.75*2*self.height/11)**2)**0.5)), (200, 200, 200), 3, center = True)
                                                                                                                                          
    def draw_frame(self,caneva):
        caneva.draw_rectangle((self.x1, self.y1+round(2*self.height/11)), (self.x2, self.y1+round(2*self.height/11)+round(self.height/11*(len(self.scores)+1))), (200, 200, 200), 3)
        for i in range(len(self.scores)) :
            score = self.scores[i]
            score_text = str()
            for e in score :
                score_text += str(e)
                score_text += " "
            caneva.draw_text(score_text, (round((self.x1+self.x2)/2+5), round(self.y1+(i+3)*(self.height/11))), 'Hollster.ttf', round((((2.9*self.width/len(str(score)))**2+((1.3*self.height)/len(str(score)))**2)**0.5)), (200, 200, 200), 3, center = True)
  