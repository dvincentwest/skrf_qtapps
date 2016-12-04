import sys
from .qt import custom_excepthook
sys.excepthook = custom_excepthook

try:
    import matplotlib
    matplotlib.use("Qt5Agg")
except ImportError:
    print("matplotlib not installed, continuing")
