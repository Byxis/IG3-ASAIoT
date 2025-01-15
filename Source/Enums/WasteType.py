from enum import Enum

class WasteType(Enum):
    """
    Enum for all the waste types
    """
    RECYCLABLE = 'Recyclable'
    BIODEGRADABLE = 'Biodegradable'
    NON_RECYCLABLE = 'Non-Recyclable'
    GLASS = "Glass"
    COMPOSED = "Composed"

