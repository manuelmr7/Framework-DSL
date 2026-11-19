from Tareas.TipoTarea import TipoTarea
from Tareas.Tipo import Tipo
from Tareas.Splitter import Splitter
from Tareas.Distributor import Distributor
from Tareas.Replicator import Replicator
from Tareas.Translator import Translator
from Tareas.Correlator import Correlator
from Tareas.CorrelationIDSetter import CorrelationIDSetter
from Tareas.ContextEnricher import ContextEnricher
from Tareas.Merger import Merger
from Tareas.Aggregator import Aggregator
from Tareas.Filter import Filter


class CreadorTareas:
    """
    Factory method: crea cualquier tarea desde una única clase y un único método.
    crear(tipo, entradas, salidas, *configuracion) busca en un diccionario la clase
    asociada al TipoTarea y la construye. *configuracion recoge los parámetros propios
    de cada tarea (xpath, ruta de un XSLT, etc.). La aplicación nunca instancia las tareas directamente.
    """
    _clases = {
        TipoTarea.SPLITTER: Splitter,
        TipoTarea.DISTRIBUIDOR: Distributor,
        TipoTarea.REPLICATOR: Replicator,
        TipoTarea.TRANSLATOR: Translator,
        TipoTarea.CORRELATOR: Correlator,
        TipoTarea.CORRELATION_ID_SETTER: CorrelationIDSetter,
        TipoTarea.CONTEXT_ENRICHER: ContextEnricher,
        TipoTarea.MERGER: Merger,
        TipoTarea.AGGREGATOR: Aggregator,
        TipoTarea.FILTER: Filter,

    }

    @classmethod
    def crear(cls, tipo, entradas, salidas, *configuracion):
        if tipo not in cls._clases:
            raise ValueError(f"Tipo de tarea desconocido: {tipo}")
        return cls._clases[tipo](entradas, salidas, *configuracion)