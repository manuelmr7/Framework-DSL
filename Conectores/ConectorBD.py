# Conectores/ConectorBD.py
import sqlite3
from lxml import etree
from Conectores.Conector import Conector
from Puertos.PuertoSOL import PuertoSOL
from Slots.Mensaje import Mensaje

class ConectorBD(Conector):
    """
    Conector con una base de datos (SQLite). Solo admite PuertoSOL.
    Lee la petición del puerto, extrae la consulta SQL de su cuerpo XML, la ejecuta
    y devuelve el resultado como XML en un mensaje nuevo que hereda la cabecera de la petición.
    """
    def __init__(self, configuracion_conector):
        super().__init__(configuracion_conector)
        self._conexion = sqlite3.connect(configuracion_conector)  # ruta del .db

    def _puerto_valido(self, puerto):
        return isinstance(puerto, PuertoSOL)

    def ejecutar(self):
        for puerto in self._puertos:
            peticion = puerto.leer_mensaje()
            if peticion is not None:
                sql = self._obtener_consulta_sql(peticion.get_cuerpo())
                doc = self._ejecutar_consulta(sql)
                respuesta = Mensaje(doc, Mensaje.siguiente_id())
                respuesta.copiar_cabecera_de(peticion)
                puerto.mensaje_slot(respuesta)

    def _obtener_consulta_sql(self, doc):
        # Formato supuesto: <consulta><sql>SELECT ...</sql></consulta>
        return doc.getroot().findtext("sql")

    def _ejecutar_consulta(self, sql):
        cursor = self._conexion.cursor()
        cursor.execute(sql)
        columnas = [c[0] for c in cursor.description] if cursor.description else []
        raiz = etree.Element("resultado")
        for fila in cursor.fetchall():
            elem = etree.SubElement(raiz, "fila")
            for nombre, valor in zip(columnas, fila):
                etree.SubElement(elem, nombre).text = str(valor)
        self._conexion.commit()
        return etree.ElementTree(raiz)