from Tareas.Tarea import Tarea
from Tareas.Tipo import Tipo

class Distributor(Tarea):
    def __init__(self, entradas, salidas, *lista_xpath):
        super().__init__(entradas, salidas, Tipo.ENRUTADORA)
        self._lista_xpath = list(lista_xpath)

    def ejecutar(self):
        pass