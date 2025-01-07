import WasteType
class Waste:
    def __init__(self, _name: str,_type: WasteType, _speed: float):
        """
        Crée une instance de Waste
        Entrée : 
        _name : str le nom du joueur
        _type : WasteType le type de dechet
        _speed : float la vitesse de descente initiale du dechet
        """
        self.name = _name
        self.type = _type
        self.speed = _speed