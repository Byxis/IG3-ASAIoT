from Enums.Direction import Direction

class Player:

    def __init__(self, n : str):
        """
        Create a Player instance

        Params:
        - n : str
            the name of the player
        """
        self.name = n
        self.score = 0.0
        self.lives = 3
        self.leftHand = None
        self.rightHand = None

    def addToScore(self, p):
        """
        Add points to the score

        Params:
        - p : float
            the points to add to the score

        Returns:
        - float
            the new player's score
        """
        self.score += p
        return self.score
    
    def changeBin(self, direction, bin):
        """
        Change the bin in the hand of the player in the given direction

        Params:
        - direction : Direction
            the direction to change the bin
        - bin : Bin
            the new bin to put in the hand
        """
        if direction == Direction.LEFT :
            self.leftHand = bin
        elif direction == Direction.RIGHT :
            self.rightHand = bin
    
    def heal(self):
        """
        Heal the player by adding 1 life

        Returns:
        - int
            the new number of lives of the player
        """
        self.lives+=1
        return self.lives

    def damage(self):
        """
        Damage the player by removing 1 life

        Returns:
        - int
            the new number of lives of the player
        """
        self.lives-=1
        return self.lives

def testPlayer():
    """
    Test the Player class
    """
    J1=Player("Tom")

    assert(J1.name!=None)
    assert(J1.addToScore(100))
    assert(J1.score!=None)
    assert(J1.heal)
    assert(J1.damage)
    assert(J1.lives!=None)

testPlayer()