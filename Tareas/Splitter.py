# Tareas/Splitter.py
from Tareas.Tarea import Tarea
from Tareas.Tipo import Tipo

class Splitter(Tarea):
    """
    Divide un mensaje en varios, uno por cada elemento que selecciona el xpath.
    Cada fragmento lleva en su cabecera el id del original (id_correlacion),
    su posición (id_secuencia) y el total de fragmentos (longitud).
    """
    def __init__(self, entradas, salidas, xpath):
        super().__init__(entradas, salidas, Tipo.ROUTER)  # pon el Tipo que le corresponda en tu diseño
        self._xpath = xpath

    def ejecutar(self): #divide un mensaje en varios, uno por cada elemento que encuentre el xpath.
        pass