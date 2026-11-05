from abc import ABC, abstractmethod


class Tarea(ABC):
    tipos = {}      # aquí se guardan todas las tareas
    clave = None    # cada subclase pondrá la suya

    def __init__(self, entradas, salidas, tipo):
        self.lista_entradas=list(entradas) #lista de slot
        self.lista_salidas=list(salidas) #lista de slot
        self.tipo=tipo;

    @abstractmethod
    def ejecutar(self):
        pass