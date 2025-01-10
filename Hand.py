from scipy.spatial import distance
from HandGesture import HandGesture

class Hand:
    def __init__(self, list):
        self.pos = list[0]
        self.thumb = list[1:5]
        self.index = list[5:9]
        self.middle = list[9:13]
        self.ring = list[13:17]
        self.little = list[17:21]
        self.scale = self.calculateScale()
    
    def calculateScale(self):
        moy = 0
        count = 0
        # Boucle sur tous les segments de la main (chaque articulation à l'articulation suivante)
        for i in range(0, len(self.thumb)-1):
            moy += distance.euclidean(self.thumb[i], self.thumb[i+1])
            count += 1
        for i in range(0, len(self.index)-1):
            moy += distance.euclidean(self.index[i], self.index[i+1])
            count += 1
        for i in range(0, len(self.middle)-1):
            moy += distance.euclidean(self.middle[i], self.middle[i+1])
            count += 1
        for i in range(0, len(self.ring)-1):
            moy += distance.euclidean(self.ring[i], self.ring[i+1])
            count += 1
        for i in range(0, len(self.little)-1):
            moy += distance.euclidean(self.little[i], self.little[i+1])
            count += 1

        # Utilisation de la moyenne des distances
        return moy / count
    
    def getHandGesture(self):
        # Vérifier si seul l'index est levé
        if self.isIndexRaised():
            return HandGesture.INDEX_RAISED

        # Vérifier si le poing est fermé
        elif self.isFistClosed():
            return HandGesture.FIST_CLOSED

        # Vérifier si la main est ouverte
        elif self.isHandOpen():
            return HandGesture.HAND_OPEN

        # Vérifier si c'est un geste "OK"
        elif self.isOkSign():
            return HandGesture.OK_SIGN

        # Si aucun geste connu n'est détecté
        return HandGesture.NONE
    
    def isIndexRaised(self):
        # L'index est levé si la deuxième articulation de l'index est plus haute que les autres doigts
        index_raised = self.index[2][1] < self.index[1][1]  # La base de l'index est plus basse que la deuxième articulation
        
        # Vérifier que les autres doigts sont repliés
        other_fingers = all([
            (self.index[0][1] > self.index[3][1]) or (not(self.index[0][1] > self.index[3][1]) and distance.euclidean(self.index[0], self.index[3]) > self.scale),  # L'index est déplié
            self.middle[0][1] < self.middle[3][1],  # Le majeur est replié
            self.ring[0][1] < self.ring[3][1],  # L'annulaire est replié
            self.little[0][1] < self.little[3][1]  # L'auriculaire est replié
        ])
        return index_raised and other_fingers
    
    def isFistClosed(self):
        # Un poing est fermé si les dernières articulations de chaque doigt sont proches de la base des doigts
        fist = all([
            self.thumb[0][1] > self.thumb[2][1],  # Le pouce est replié
            self.index[0][1] < self.index[2][1],  # L'index est replié
            self.middle[0][1] < self.middle[2][1],  # Le majeur est replié
            self.ring[0][1] < self.ring[2][1],  # L'annulaire est replié
            self.little[0][1] < self.little[2][1]  # L'auriculaire est replié
        ])

        return fist

    
    def isHandOpen(self):
        # Une main ouverte signifie que les articulations sont suffisamment éloignées les unes des autres
        hand_open = all([self.thumb[1][1] < self.thumb[0][1],
                        self.index[2][1] < self.index[1][1],
                        self.middle[2][1] < self.middle[1][1],
                        self.ring[2][1] < self.ring[1][1],
                        self.little[2][1] < self.little[1][1]])
        return hand_open
    
    def isOkSign(self):
        # Un geste "OK" signifie que le pouce et l'index se touchent, et les autres doigts sont pliés
        ok_sign = all([
                distance.euclidean(self.thumb[3], self.index[3]) < self.scale,  # Pouce et index proches 18 < 30/2
                self.middle[3][1] < self.middle[0][1],
                self.ring[3][1] < self.ring[0][1],
                self.little[3][1] < self.little[0][1]])
        return ok_sign