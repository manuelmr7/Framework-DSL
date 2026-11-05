from lxml import etree
from Tareas.Tarea import Tarea
from Tareas.Tipo import Tipo


class Translator(Tarea):
    def __init__(self,entradas,salidas,ruta_archivo_xslt):
        super().__init__(entradas,salidas,Tipo.TRANSFORMADORA)
        self.ruta_archivo_xslt=ruta_archivo_xslt

    def ejecutar(self):
        xslt=etree.XSLT(etree.parse(self._ruta_archivo_xslt))
        entrada=self._lista_entradas[0]
        salida=self._lista_salidas[0]
        while not entrada.esta_vacio():
            mensaje=entrada.leer_mensaje()
            mensaje.set_cuerpo(xslt(mensaje.get_cuerpo()))
            salida.escribir_mensaje(mensaje)