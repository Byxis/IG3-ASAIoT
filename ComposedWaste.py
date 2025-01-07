class ComposedWaste:
    def __init__(self, _name: str, _components):
        """
        Crée une instance de ComposedWaste
        Entrée :
        _name : str nom du déchet
        _component : [] une liste contenant des dechets ou des dechets composé
        """
        self.components = _components
        self.name = _name
    
    def slice(self):
        return tuple(self.components)
