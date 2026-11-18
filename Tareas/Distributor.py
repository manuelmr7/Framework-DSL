from Tareas.Tarea import Tarea
from Tareas.Tipo import Tipo

class Distributor(Tarea):
    """
    Reparte cada mensaje a una salida según condiciones xpath.
    El xpath n corresponde a la salida n; el mensaje va a la primera que cumple
    y, si no cumple ninguna, se descarta.
    """
    def __init__(self, entradas, salidas, *lista_xpath):
        super().__init__(entradas, salidas, Tipo.ENRUTADORA)
        self._lista_xpath = list(lista_xpath)

    def ejecutar(self): #reparte cada mensaje a una salida según una condición xpath.
        entrada = self._lista_entradas[0]
        while not entrada.esta_vacio():
            mensaje = entrada.leer_mensaje()
            for i, xpath in enumerate(self._lista_xpath):
                if i < len(self._lista_salidas):
                    if mensaje.get_cuerpo().xpath(xpath):
                        self._lista_salidas[i].escribir_mensaje(mensaje)
                        break
