from collections import deque

class Slot:
    def __init__(self):
        self._lista_mensajes = deque()

    def escribir_mensaje(self, mensaje):
        self._lista_mensajes.append(mensaje)

    def leer_mensaje(self):
        # saca y devuelve el primer mensaje (FIFO)
        return self._lista_mensajes.popleft()

    def siguiente_mensaje(self):
        # devuelve el primer mensaje sin sacarlo
        return self._lista_mensajes[0]

    def get_longitud_mensaje(self):
        # número de mensajes que hay en el slot
        return len(self._lista_mensajes)

    def esta_vacio(self):
        return len(self._lista_mensajes) == 0