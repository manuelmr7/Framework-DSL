# Puertos/PuertoSOL.py
from Puertos.Puerto import Puerto

class PuertoSOL(Puerto):
    """
    Puerto de solicitud-respuesta. Usa dos slots:
    - slot de salida: peticiones que deja el framework; el conector las lee con leer_mensaje().
    - slot de entrada: respuestas que el conector escribe con mensaje_slot().
    """
    def __init__(self, entrada, salida):
        super().__init__(entrada)      # self._slot = slot de entrada (respuestas)
        self._slot_out = salida        # slot de salida (peticiones)

    def mensaje_slot(self, mensaje):   # el conector deja la respuesta
        self._slot.escribir_mensaje(mensaje)

    def leer_mensaje(self):            # el conector recoge la petición
        return self._slot_out.leer_mensaje()

    def get_slot_in(self):
        return self._slot

    def get_slot_out(self):
        return self._slot_out