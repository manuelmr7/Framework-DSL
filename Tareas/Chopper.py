# Tareas/Chopper.py
from Tareas.Tarea import Tarea
from Tareas.Tipo import Tipo

class Chopper(Tarea):
    def __init__(self, entradas, salidas):
        super().__init__(entradas, salidas, Tipo.TRANSFORMADORA)

    def ejecutar(self):
        pass