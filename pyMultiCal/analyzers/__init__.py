from collections import OrderedDict
import importlib
import glob
import os.path
import sys

from . import base_analyzer

this_path = os.path.normpath(os.path.dirname(__file__))
analyzer_modules = glob.glob(this_path + "/analyzer_*.py")
analyzers = OrderedDict()

analyzers["scikit-rf VNA"] = base_analyzer.Analyzer

sys.path.insert(0, this_path)
for analyzer in analyzer_modules:
    module_name = os.path.basename(analyzer)[:-3]
    module = importlib.import_module(module_name)
    if module.Analyzer.NAME in analyzers.keys():
        Warning("overwriting Analyzer {:s} in selection".format(module.Analyzer.NAME))
    analyzers[module.Analyzer.NAME] = module.Analyzer
sys.path.pop(0)
