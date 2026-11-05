from Tareas.Tarea import Tarea
from Tareas.Tipo import Tipo

class Filter(Tarea):
    def __init__(self, entradas, salidas, xpath):
        super().__init__(entradas, salidas, Tipo.ENRUTADORA)
        self._xpath = xpath

    def ejecutar(self):
        pass