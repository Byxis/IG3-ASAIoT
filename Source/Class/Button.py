from Utils.Graphics import Graphic, SceneRender

class Button:
    def __init__(self, name: str, x1, y1, width, height, action=None):
        """
        Create a Button instance

        Params:
        - name : str
            the name of the button
        - x1 : int
            the x position of the button
        - y1 : int
            the y position of the button
        - width : int
            the width of the button
        - height : int
            the height of the button
        - action : function
            the action to do when the button is clicked
        """
        self.name = name
        self.x1 = x1
        self.y1 = y1
        self.width = width  
        self.height = height
        self.x2 = x1 + width
        self.y2 = y1 + height
        self.action = action

    def isClicked(self, pos_x=-1, pos_y=-1):
        """
        Check if the button is clicked

        Params:
        - pos_x = -1 : int
            the x position of the click
        - pos_y = -1 : int
            the y position of the click

        Returns:
        - bool
            True if the button is clicked, False otherwise
        """
        return self.x1 <= pos_x <= self.x2 and self.y1 <= pos_y <= self.y2

    def click(self):
        """
        Call the action of the button

        Returns:
        - any
            the return of the action
        """
        if self.action:
            return self.action()

    def draw_button(self,caneva):
        """
        Draw the button on the caneva

        Params:
        - caneva : Graphic
            the caneva to draw on
        """
        caneva.draw_rectangle((self.x1, self.y1), (self.x2, self.y2), (200, 200, 200), 3)
        caneva.draw_text(self.name, (((self.x1+self.x2)/2-(len(self.name))), ((self.y1+self.y2)/2-(len(self.name)))), '../Ressources/Fonts/Hollster.ttf', 30   , (200, 200, 200), 3, center = True)
  