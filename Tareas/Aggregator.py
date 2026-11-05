from Tareas.Tarea import Tarea
from Tareas.Tipo import Tipo

class Aggregator(Tarea):
    def __init__(self, entradas, salidas, raiz):
        super().__init__(entradas, salidas, Tipo.TRANSFORMADORA)
        self._raiz = raiz
        self._fragmentos = {}   # id de secuencia -> lista de fragmentos

    def ejecutar(self):
        pass