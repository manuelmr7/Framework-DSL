# Puertos/PuertoOUT.py
from Puertos.Puerto import Puerto

class PuertoOUT(Puerto):
    """
    Puerto de salida del framework: el conector recoge con leer_mensaje()
    los mensajes que las tareas han dejado en el slot (None si no hay ninguno).
    """
    def leer_mensaje(self):
        return self._slot.leer_mensaje()