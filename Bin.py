class Bin:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.content = []
    
    def addWasteToBin(self, waste):
        self.content.put(waste)
    
    def isCompatible(self, waste):
        if isinstance(waste, ComposedWaste):
            return False
        else :
            return self.type == waste.type