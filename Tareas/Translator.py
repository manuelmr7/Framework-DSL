from Tareas.Tarea import Tarea
from Tareas.Tipo import Tipo


class Translator(Tarea):
    def __init__(self,entradas,salidas,ruta_archivo_xslt):
        super().__init__(entradas,salidas,Tipo.TRANSFORMADORA)
        self.ruta_archivo_xslt=ruta_archivo_xslt

    def ejecutar(self):
        pass