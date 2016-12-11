import sys
from .qt import _excepthook
sys.excepthook = _excepthook

try:
    import matplotlib
    matplotlib.use("Qt5Agg")
except ImportError:
    print("matplotlib not installed, continuing")
