# Tareas/ReturnAddressSetter.py
from Tareas.Tarea import Tarea
from Tareas.Tipo import Tipo

class ReturnAddressSetter(Tarea):
    def __init__(self, entradas, salidas):
        super().__init__(entradas, salidas, Tipo.MODIFICADORA)

    def ejecutar(self):
        pass