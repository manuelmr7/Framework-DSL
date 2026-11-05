from Tareas.Tarea import Tarea
from Tareas.Tipo import Tipo

class CorrelationIDSetter(Tarea):
    def __init__(self, entradas, salidas):
        super().__init__(entradas, salidas, Tipo.MODIFICADORA)
        self._mensajes_entrada = {}

    def ejecutar(self):
        pass

    def relacionar(self, mensaje):
        pass