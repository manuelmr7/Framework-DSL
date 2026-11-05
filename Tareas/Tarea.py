from abc import ABC, abstractmethod


class Tarea(ABC):
    tipos = {}      # aquí se guardan todas las tareas
    clave = None    # cada subclase pondrá la suya

    def __init__(self, nombre, slot_entrada=None, slot_salida=None):
        self.nombre = nombre
        self.slot_entrada = slot_entrada
        self.slot_salida = slot_salida

    def __init_subclass__(cls, **kwargs):
        # Python llama a esto cada vez que defines una subclase de Tarea
        super().__init_subclass__(**kwargs)
        if "clave" in cls.__dict__ and cls.clave is not None:
            Tarea.tipos[cls.clave] = cls

    @classmethod
    def crear(cls, clave, **kwargs):
        if clave not in Tarea.tipos:
            raise ValueError(f"Tarea desconocida '{clave}'. Disponibles: {', '.join(Tarea.tipos)}")
        return Tarea.tipos[clave](**kwargs)

    @abstractmethod
    def ejecutar(self):
        pass