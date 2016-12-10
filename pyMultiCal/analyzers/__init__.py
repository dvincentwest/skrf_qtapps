from collections import OrderedDict
from . import analyzer_e8363C, analyzer_e8364C

analyzers = OrderedDict()
analyzers["E8363C"] = analyzer_e8363C.PNA
analyzers["E8364C"] = analyzer_e8364C.PNA