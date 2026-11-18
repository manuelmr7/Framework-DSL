from Tareas.Tarea import Tarea
from Tareas.Tipo import Tipo

class CorrelationIDSetter(Tarea):
    """
    Asigna un id_correlacion a los mensajes que pasan por ella si aún no tienen uno.
    Guarda un histórico en _mensajes_entrada agrupado por id_correlacion.
    """
    def __init__(self, entradas, salidas):
        super().__init__(entradas, salidas, Tipo.MODIFICADORA)
        self._mensajes_entrada = {}

    def ejecutar(self):
        entrada = self._lista_entradas[0]
        salida = self._lista_salidas[0]
        while not entrada.esta_vacio():
            mensaje = entrada.leer_mensaje()
            if mensaje.get_id_correlacion() is None:
                mensaje.set_id_correlacion(mensaje.get_id())
            self.relacionar(mensaje)
            salida.escribir_mensaje(mensaje)

    def relacionar(self, mensaje):
        id_corr = mensaje.get_id_correlacion()
        if id_corr not in self._mensajes_entrada:
            self._mensajes_entrada[id_corr] = []
        self._mensajes_entrada[id_corr].append(mensaje)
