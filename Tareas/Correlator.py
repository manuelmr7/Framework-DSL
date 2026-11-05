from Tareas.Tarea import Tarea
from Tareas.Tipo import Tipo

class Correlator(Tarea):
    def __init__(self, entradas, salidas, xpath):
        super().__init__(entradas, salidas, Tipo.ENRUTADORA)
        self._xpath = xpath
        self._mensajes_entrada = {}   # clave de correlación -> lista de mensajes

    def ejecutar(self):
        pass

    def relacionar(self, mensaje):
        pass