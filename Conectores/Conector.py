# Conectores/Conector.py
from abc import ABC, abstractmethod

class Conector(ABC):
    """
    Clase abstracta. Puente entre un sistema externo (fichero, base de datos...) y el framework.
    Gestiona una lista de puertos: agregar_puerto() solo admite los que _puerto_valido()
    acepta y lanza ValueError con los demás. Los hijos implementan _puerto_valido() y ejecutar().
    El conector solo habla con los slots a través de sus puertos, nunca con las tareas.
    """
    def __init__(self, configuracion_conector):
        self._puertos = []
        self._configuracion_conector = configuracion_conector

    def agregar_puerto(self, puerto):
        if not self._puerto_valido(puerto):
            raise ValueError(
                f"{type(self).__name__} no admite puertos de tipo {type(puerto).__name__}")
        self._puertos.append(puerto)

    def get_puertos(self):
        return self._puertos

    @abstractmethod
    def _puerto_valido(self, puerto):
        pass

    @abstractmethod
    def ejecutar(self):
        pass