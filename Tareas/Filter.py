from Tareas.Tarea import Tarea
from Tareas.Tipo import Tipo

class Filter(Tarea):
    """
    Filtra mensajes según una condición xpath.
    Si el cuerpo cumple el xpath, el mensaje pasa a la salida; si no, se descarta.
    """
    def __init__(self, entradas, salidas, xpath):
        super().__init__(entradas, salidas, Tipo.ENRUTADORA)
        self._xpath = xpath

    def ejecutar(self):
        entrada = self._lista_entradas[0]
        salida = self._lista_salidas[0]
        while not entrada.esta_vacio():
            mensaje = entrada.leer_mensaje()
            if mensaje.get_cuerpo().xpath(self._xpath):
                salida.escribir_mensaje(mensaje)
