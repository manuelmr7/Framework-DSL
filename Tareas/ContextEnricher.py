import copy
from Tareas.Tarea import Tarea
from Tareas.Tipo import Tipo

class ContextEnricher(Tarea):
    """
    Añade a un mensaje datos que llegan en otro. Tiene dos entradas: la primera
    trae el mensaje principal y la segunda el de contexto. Los empareja por orden
    y copia el cuerpo del de contexto dentro de la raíz del principal.
    """
    def __init__(self, entradas, salidas):
        super().__init__(entradas, salidas, Tipo.MODIFIER)

    def ejecutar(self): #añade a un mensaje datos que llegan en otro.
        principal = self._lista_entradas[0]
        contexto = self._lista_entradas[1]
        salida = self._lista_salidas[0]

        while not principal.esta_vacio() and not contexto.esta_vacio():
            mensaje = principal.leer_mensaje()
            msg_contexto = contexto.leer_mensaje()

            raiz = mensaje.get_cuerpo().getroot()
            raiz.append(copy.deepcopy(msg_contexto.get_cuerpo().getroot()))

            salida.escribir_mensaje(mensaje)