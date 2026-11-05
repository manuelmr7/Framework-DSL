import copy
from Tareas.Tarea import Tarea
from Tareas.Tipo import Tipo

class ContextEnricher(Tarea):
    def __init__(self, entradas, salidas):
        super().__init__(entradas, salidas, Tipo.MODIFIER)

    def ejecutar(self):
        principal = self._lista_entradas[0]
        contexto = self._lista_entradas[1]
        salida = self._lista_salidas[0]

        while not principal.esta_vacio() and not contexto.esta_vacio():
            mensaje = principal.leer_mensaje()
            msg_contexto = contexto.leer_mensaje()

            raiz = mensaje.get_cuerpo().getroot()
            raiz.append(copy.deepcopy(msg_contexto.get_cuerpo().getroot()))

            salida.escribir_mensaje(mensaje)