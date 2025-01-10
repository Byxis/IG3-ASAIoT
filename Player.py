from Direction import Direction
#from Bin import Bin

class Player:

    def __init__(self, n : str):
        self.name = n
        self.score = 0.0
        self.lives = 3
        self.leftHand = None
        self.rightHand = None

    def addToScore(self, p):
        self.score += p
        return self.score
    
    def changeBin(self, direction, bin):
        if direction == Direction.LEFT :
            self.leftHand = bin
        elif direction == Direction.RIGHT :
            self.rightHand = bin

        return direction
    
    def heal(self):
        self.lives+=1
        return self.lives

    def damage(self):
        self.lives-=1
        return self.lives

def testPlayer():
    J1=Player("Tom")

    assert(J1.name!=None)
    assert(J1.addToScore(100))
    assert(J1.score!=None)
    assert(J1.heal)
    assert(J1.damage)
    assert(J1.lives!=None)

testPlayer()