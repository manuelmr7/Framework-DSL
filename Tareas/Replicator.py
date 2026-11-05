import copy
from Tareas.Tarea import Tarea
from Tareas.Tipo import Tipo

class Replicator(Tarea):
    def __init__(self, entradas, salidas):
        super().__init__(entradas, salidas,Tipo.ENRUTADORA)

    def ejecutar(self):
        entrada=self._lista_entradas[0]
        while not entrada.esta_vacio():
            mensaje=entrada.leer_mensaje()
            for salida in self._lista_salidas:
                salida.escribir_mensaje(copy.deepcopy(mensaje)) #deepcopy necesario para que cada salida reciba su propio
                # objeto. Si compartieran el mismo, una tarea posterior que modifique el mensaje lo cambiaría también en
                # las otras ramas