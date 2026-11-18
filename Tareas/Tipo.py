from enum import Enum, auto
class Tipo(Enum):
    """
    Enum con la categoría de una tarea (por ejemplo ENRUTADORA).
    No decide qué clase se crea; eso lo hace TipoTarea.
    """
    ENRUTADORA=auto()
    TRANSFORMADORA=auto()
    MODIFICADORA=auto()