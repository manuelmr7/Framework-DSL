# Tareas/Splitter.py
import copy
from lxml import etree
from Tareas.Tarea import Tarea
from Tareas.Tipo import Tipo
from Slots.Mensaje import Mensaje

class Splitter(Tarea):
    """
    Divide un mensaje en varios, uno por cada elemento que selecciona el xpath.
    Cada fragmento lleva en su cabecera el id del original (id_correlacion),
    su posición (id_secuencia) y el total de fragmentos (longitud).
    """
    def __init__(self, entradas, salidas, xpath):
        super().__init__(entradas, salidas, Tipo.ROUTER)  # pon el Tipo que le corresponda en tu diseño
        self._xpath = xpath

    def ejecutar(self):
        entrada = self._lista_entradas[0]
        salida = self._lista_salidas[0]
        while not entrada.esta_vacio():
            mensaje = entrada.leer_mensaje()
            fragmentos = mensaje.get_cuerpo().xpath(self._xpath)
            total = len(fragmentos)
            for i, fragmento in enumerate(fragmentos, start=1):
                cuerpo = etree.ElementTree(copy.deepcopy(fragmento))
                nuevo = Mensaje(cuerpo, f"{mensaje.get_id()}.{i}")
                nuevo.set_id_correlacion(mensaje.get_id())
                nuevo.set_id_secuencia(i)
                nuevo.set_longitud(total)
                salida.escribir_mensaje(nuevo)