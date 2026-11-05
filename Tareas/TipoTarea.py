from enum import Enum, auto

class TipoTarea(Enum):
    SPLITTER = auto()
    DISTRIBUIDOR = auto()
    REPLICATOR = auto()
    TRANSLATOR = auto()
    CORRELATOR = auto()
    CORRELATION_ID_SETTER = auto()
    CONTEXT_ENRICHER = auto()
    MERGER = auto()
    AGGREGATOR = auto()
    FILTER = auto()
    SLIMMER = auto()
    CHOPPER = auto()
    ASSEMBLER = auto()
    HEADER_PROMOTER = auto()
    RETURN_ADDRESS_SETTER = auto()
    THREADER = auto()