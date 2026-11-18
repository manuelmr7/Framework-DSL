# Conectores/ConectorBDMock.py
from Conectores.Conector import Conector
from Conectores.ConectorBD import ConectorBD

class ConectorBDMock(ConectorBD):
    """
    Doble de prueba de ConectorBD: no abre ninguna base de datos.
    Responde con mensajes preparados de antemano y cuenta las consultas recibidas
    (get_num_consultas()). Sirve para probar el resto del framework sin BD real.
    """
    def __init__(self, respuestas):
        Conector.__init__(self, "mock")   # salta el __init__ de ConectorBD para no abrir la BD
        self._respuestas = list(respuestas)
        self._num_consultas = 0

    def ejecutar(self):
        for puerto in self._puertos:
            peticion = puerto.leer_mensaje()
            if peticion is not None:
                self._num_consultas += 1
                respuesta = self._respuestas.pop(0)
                respuesta.copiar_cabecera_de(peticion)
                puerto.mensaje_slot(respuesta)

    def get_num_consultas(self):
        return self._num_consultas