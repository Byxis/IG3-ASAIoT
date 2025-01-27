from Class.Player import Player
from Class.Waste import Waste
from Class.Bin import Bin
from Class.ComposedWaste import ComposedWaste
from Enums.WasteType import WasteType

class Stats:
    def __init__(self, _bins):
        self.bins = _bins

    def getTotalCorrectSortingNumber(self):
        count = 0
        for bin in self.bins.values():
            for waste in bin.content:
                if bin.isCompatible(waste):
                    count += 1
        return count
    
    def getTotalWrongSortingNumber(self):
        count = 0
        for bin in self.bins.values():
            for waste in bin.content:
                if not bin.isCompatible(waste):
                    count += 1
        return count

    def getMissedWasteNumber(self):
        countW = 0
        countCW = 0
        for waste in self.bins["Floor"].content:
            if type(waste) == Waste:
                countW += 1
            elif type(waste) == ComposedWaste:
                countCW += 1
        return countW, countCW
    
    def getCorrectWasteNumberForEachBin(self):
        stat_dic = {}
        for elt in self.bins.items():
            stat_dic[elt[0]] = 0
            for waste in elt[1].content:
                if elt[1].isCompatible(waste):
                         stat_dic[elt[0]] += 1
        return stat_dic
    
    def getWrongWasteNumberForEachBin(self):
        stat_dic = {}
        for elt in self.bins.items():
            stat_dic[elt[0]] = 0
            for waste in elt[1].content:
                if not elt[1].isCompatible(waste):
                         stat_dic[elt[0]] += 1
        return stat_dic
    
    def getTotalWasteInBins(self):
        total_waste = 0
        for bin_obj in self.bins.values():
            total_waste += len(bin_obj.content)
        return total_waste
    
    def getCorrectSortingPercentage(self):
        total_waste = self.getTotalWasteInBins()
        total_correct = self.getTotalCorrectSortingNumber()
        if total_waste == 0:
            return 0
        else:
            return total_correct/total_waste * 100

    def WrongSortingPercentage(self):
        total_waste = self.getTotalWasteInBins()
        total_wrong = self.getTotalWrongSortingNumber()
        if total_waste == 0:
            return 0
        else:
            return total_wrong/total_waste * 100

    def getAllStats(self):
        return [
            ["Nombre de déchets correctement triés :", self.getTotalCorrectSortingNumber()],
            ["Nombre de déchets mal triés :", self.getTotalWrongSortingNumber()],
            ["Nombre de déchets tombés au sol :", self.getMissedWasteNumber()],
            ["Pourcentage de déchets correctement triés :", self.getCorrectSortingPercentage()],
            ["Pourcentage de déchets mal triés :", self.WrongSortingPercentage()],
            ["Nombre de déchets correctement triés par poubelle :", self.getCorrectWasteNumberForEachBin()],
            ["Nombre de déchets mal triés par poubelle :", self.getWrongWasteNumberForEachBin()],
            ["Nombre total de déchets :", self.getTotalWasteInBins()]        
        ]
    
bins = {
    "Recycling": Bin("Recycling", WasteType.Recycling, 480),
    "Compost": Bin("Compost", WasteType.Compost, 480),
    "Glass": Bin("Glass", WasteType.Glass, 480),
    "Default": Bin("Default", WasteType.NonRecycling, 480),
    "Floor": Bin("Floor", WasteType.Floor, 480)
}
