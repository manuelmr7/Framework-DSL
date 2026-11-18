import copy
from Tareas.Tarea import Tarea
from Tareas.Tipo import Tipo

class Replicator(Tarea):
    """
    Copia cada mensaje de la entrada a todas las salidas.
    Usa deepcopy para que cada salida reciba su propio objeto.
    """
    def __init__(self, entradas, salidas):
        super().__init__(entradas, salidas, Tipo.ENRUTADORA)

    def ejecutar(self):  # copia el mensaje a todas las salidas
        entrada = self._lista_entradas[0]
        mensaje = entrada.leer_mensaje()
        if mensaje is not None:
            for salida in self._lista_salidas:
                salida.escribir_mensaje(copy.deepcopy(mensaje))  # cada salida recibe su propio objeto