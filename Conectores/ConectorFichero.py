# Conectores/ConectorFichero.py
from lxml import etree
from Conectores.Conector import Conector
from Puertos.PuertoIN import PuertoIN
from Puertos.PuertoOUT import PuertoOUT
from Slots.Mensaje import Mensaje

class ConectorFichero(Conector):
    """
    Conector con un fichero XML (la ruta es la configuración del conector).
    Admite PuertoIN y PuertoOUT.
    - Con PuertoIN: lee el fichero, crea un Mensaje y lo deja en el slot.
    - Con PuertoOUT: lee un mensaje del slot y escribe su cuerpo en el fichero.
    """
    def __init__(self, configuracion_conector):
        super().__init__(configuracion_conector)
        self._ruta_fichero = configuracion_conector

    def _puerto_valido(self, puerto):
        return isinstance(puerto, (PuertoIN, PuertoOUT))

    def ejecutar(self):
        for puerto in self._puertos:
            if isinstance(puerto, PuertoIN):
                doc = self._leer_fichero()
                puerto.mensaje_slot(Mensaje(doc, Mensaje.siguiente_id()))
            elif isinstance(puerto, PuertoOUT):
                mensaje = puerto.leer_mensaje()
                if mensaje is not None:
                    self._escribir_fichero(mensaje.get_cuerpo(), self._ruta_fichero)

    def _leer_fichero(self):
        return etree.parse(self._ruta_fichero)

    def _escribir_fichero(self, doc, ruta):
        doc.write(ruta, encoding="utf-8", xml_declaration=True, pretty_print=True)