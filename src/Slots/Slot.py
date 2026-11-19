from collections import deque

class Slot:
    """
    Cola FIFO de mensajes. Es el canal por el que se comunican tareas, puertos y conectores.
    Los mensajes se escriben por el final y se leen por el principio.
    leer_mensaje() saca el primero (o devuelve None si el slot está vacío);
    siguiente_mensaje() lo consulta sin sacarlo.
    """
    def __init__(self):
        self._lista_mensajes = deque()

    def escribir_mensaje(self, mensaje):
        self._lista_mensajes.append(mensaje)

    def leer_mensaje(self):
        # saca y devuelve el primer mensaje (FIFO)
        if self._lista_mensajes:
            return self._lista_mensajes.popleft()
        return None

    def siguiente_mensaje(self):
        # devuelve el primer mensaje sin sacarlo
        if self._lista_mensajes:
            return self._lista_mensajes[0]
        return None

    def get_longitud_mensaje(self):
        # número de mensajes que hay en el slot
        return len(self._lista_mensajes)

    def esta_vacio(self):
        return len(self._lista_mensajes) == 0
