from Tareas.Tarea import Tarea
from Tareas.Tipo import Tipo

class Merger(Tarea):
    def __init__(self, entradas, salidas):
        super().__init__(entradas, salidas, Tipo.ENRUTADORA)

    def ejecutar(self):
        salida=self._lista_salidas[0]
        for entrada in self._lista_entradas:
            while not entrada.esta_vacio():
                salida.escribir_mensaje(entrada.leer_mensaje())