import sys
from .qt import pyqt5_excepthook
sys.excepthook = pyqt5_excepthook

try:
    import matplotlib
    matplotlib.use("Qt5Agg")
except ImportError:
    print("matplotlib not installed, continuing")
