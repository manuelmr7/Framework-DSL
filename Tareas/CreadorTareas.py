from Tareas.TipoTarea import TipoTarea
from Tareas.Tipo import Tipo
from Tareas.Splitter import Splitter
from Tareas.Distributor import Distributor
from Tareas.Replicator import Replicator
from Tareas.Translator import Translator
from Tareas.Correlator import Correlator
from Tareas.CorrelationIDSetter import CorrelationIDSetter
from Tareas.ContextSlimmer import ContextSlimmer
from Tareas.Merger import Merger
from Tareas.Aggregator import Aggregator
from Tareas.Filter import Filter
from Tareas.Slimmer import Slimmer
from Tareas.Chopper import Chopper
from Tareas.Assembler import Assembler
from Tareas.HeaderPromoter import HeaderPromoter
from Tareas.ReturnAddressSetter import ReturnAddressSetter
from Tareas.Threader import Threader


class CreadorTareas:
    _clases = {
        TipoTarea.SPLITTER: Splitter,
        TipoTarea.DISTRIBUIDOR: Distributor,
        TipoTarea.REPLICATOR: Replicator,
        TipoTarea.TRANSLATOR: Translator,
        TipoTarea.CORRELATOR: Correlator,
        TipoTarea.CORRELATION_ID_SETTER: CorrelationIDSetter,
        TipoTarea.CONTEXT_ENRICHER: ContextSlimmer,
        TipoTarea.MERGER: Merger,
        TipoTarea.AGGREGATOR: Aggregator,
        TipoTarea.FILTER: Filter,
        TipoTarea.SLIMMER: Slimmer,
        TipoTarea.CHOPPER: Chopper,
        TipoTarea.ASSEMBLER: Assembler,
        TipoTarea.HEADER_PROMOTER: HeaderPromoter,
        TipoTarea.RETURN_ADDRESS_SETTER: ReturnAddressSetter,
        TipoTarea.THREADER: Threader,

    }

    @classmethod
    def crear(cls, tipo, entradas, salidas, *configuracion):
        if tipo not in cls._clases:
            raise ValueError(f"Tipo de tarea desconocido: {tipo}")
        return cls._clases[tipo](entradas, salidas, *configuracion)