class Puerto:
    """
    Clase abstracta. Punto de unión entre un conector y un slot.
    Guarda el slot al que está asociado; cada hijo define en qué dirección se usa.
    """
    def __init__(self):
        # Puertos/Puerto.py
        from abc import ABC

        class Puerto(ABC):
            def __init__(self, slot):
                self._slot = slot

            def get_slot(self):
                return self._slot