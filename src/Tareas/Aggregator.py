import copy
from lxml import etree
from Tareas.Tarea import Tarea
from Tareas.Tipo import Tipo
from Slots.Mensaje import Mensaje

class Aggregator(Tarea):
    """
    Reconstruye un mensaje completo a partir de sus fragmentos.
    Agrupa por id_correlacion y, cuando tiene todos los fragmentos esperados (longitud),
    los ordena por id_secuencia y los envuelve en un nuevo documento XML con la etiqueta raíz indicada.
    """
    def __init__(self, entradas, salidas, raiz):
        super().__init__(entradas, salidas, Tipo.TRANSFORMADORA)
        self._raiz = raiz
        self._fragmentos = {}   # id_correlacion -> lista de fragmentos

    def ejecutar(self):
        entrada = self._lista_entradas[0]
        salida = self._lista_salidas[0]
        while not entrada.esta_vacio():
            mensaje = entrada.leer_mensaje()
            id_corr = mensaje.get_id_correlacion() or mensaje.get_id()
            if id_corr not in self._fragmentos:
                self._fragmentos[id_corr] = []
            self._fragmentos[id_corr].append(mensaje)

            total = mensaje.get_longitud()
            if total is not None and len(self._fragmentos[id_corr]) >= total:
                fragmentos = self._fragmentos.pop(id_corr)
                fragmentos.sort(key=lambda m: m.get_id_secuencia() or 0)
                raiz_elem = etree.Element(self._raiz)
                for f in fragmentos:
                    cuerpo_elem = f.get_cuerpo().getroot()
                    raiz_elem.append(copy.deepcopy(cuerpo_elem))
                doc = etree.ElementTree(raiz_elem)
                nuevo = Mensaje(doc, id_corr)
                nuevo.set_id_correlacion(id_corr)
                salida.escribir_mensaje(nuevo)
