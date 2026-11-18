# Puertos/PuertoIN.py
from Puertos.Puerto import Puerto

class PuertoIN(Puerto):
    """
    Puerto de entrada al framework: el conector deja mensajes en el slot
    mediante mensaje_slot().
    """
    def mensaje_slot(self, mensaje):
        self._slot.escribir_mensaje(mensaje)