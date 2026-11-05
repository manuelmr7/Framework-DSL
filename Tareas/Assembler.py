from Tareas.Tarea import Tarea
from Tareas.Tipo import Tipo

class Assembler(Tarea):
    def __init__(self, entradas, salidas):
        super().__init__(entradas, salidas, Tipo.TRANSFORMADORA)
        self._fragmentos = {}   # id de secuencia -> lista de fragmentos

    def ejecutar(self):
        pass