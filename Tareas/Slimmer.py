# Tareas/Slimmer.py
from Tareas.Tarea import Tarea
from Tareas.Tipo import Tipo

class Slimmer(Tarea):
    def __init__(self, entradas, salidas, *lista_xpath):
        super().__init__(entradas, salidas, Tipo.MODIFICADORA)
        self._lista_xpath = list(lista_xpath)   # partes del cuerpo a eliminar

    def ejecutar(self):
        pass