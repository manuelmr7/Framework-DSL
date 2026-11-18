from Tareas.Tarea import Tarea
from Tareas.Tipo import Tipo

class Correlator(Tarea):
    """
    Agrupa mensajes recibidos por una clave extraída mediante xpath (o id_correlacion).
    Cuando se han recibido todos los mensajes de un grupo (según la longitud especificada
    o cuando hay al menos un mensaje por cada entrada conectada), los libera hacia la salida.
    """
    def __init__(self, entradas, salidas, xpath):
        super().__init__(entradas, salidas, Tipo.ENRUTADORA)
        self._xpath = xpath
        self._mensajes_entrada = {}   # clave de correlación -> lista de mensajes

    def ejecutar(self):
        for entrada in self._lista_entradas:
            while not entrada.esta_vacio():
                mensaje = entrada.leer_mensaje()
                self.relacionar(mensaje)

        salida = self._lista_salidas[0]
        claves_a_enviar = []
        for clave, msgs in self._mensajes_entrada.items():
            longitud = msgs[0].get_longitud()
            if longitud is not None:
                if len(msgs) >= longitud:
                    claves_a_enviar.append(clave)
            elif len(msgs) >= len(self._lista_entradas):
                claves_a_enviar.append(clave)

        for clave in claves_a_enviar:
            for m in self._mensajes_entrada.pop(clave):
                salida.escribir_mensaje(m)

    def relacionar(self, mensaje):
        res = mensaje.get_cuerpo().xpath(self._xpath)
        if res:
            if hasattr(res[0], 'text') and res[0].text:
                clave = res[0].text
            else:
                clave = str(res[0])
        else:
            clave = mensaje.get_id_correlacion() or mensaje.get_id()

        if clave not in self._mensajes_entrada:
            self._mensajes_entrada[clave] = []
        self._mensajes_entrada[clave].append(mensaje)
        return clave
