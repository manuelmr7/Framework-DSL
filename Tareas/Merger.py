from Tareas.Tarea import Tarea
from Tareas.Tipo import Tipo

class Merger(Tarea):
    def __init__(self, entradas, salidas):
        super().__init__(entradas, salidas, Tipo.ENRUTADORA)

    def ejecutar(self):
        pass